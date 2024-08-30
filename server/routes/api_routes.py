from models.api import Api
from flask import Blueprint, jsonify, request
from aws import api_gateway_client
from middleware.issue_tokens import token_required
from middleware.authorize import check_user_role
from middleware.api_access import api_access

api_bp = Blueprint('api', __name__)

@api_bp.route('/deploy-api', methods=['POST'])
@check_user_role(['Administrator', 'DevOps Engineer'])
@token_required
def deploy_api(current_user):
    try:
        data = request.json
        api_id = data.get('api_id')
        stage_name = data.get('stage_name')

        if not api_id or not stage_name:
            return jsonify({
                'message': 'API ID and Stage Name are required',
                'status': 400,
                'statusText': 'Bad Request',
                'mime-type': 'application/json'
            }), 400

        # Deploy the API to the specified stage
        response = api_gateway_client.create_deployment(
            restApiId=api_id,
            stageName=stage_name
        )

        return jsonify({
            'message': 'API deployed successfully',
            'deploymentId': response.get('id'),
            'status': 200,
            'statusText': 'OK',
            'mime-type': 'application/json'
        }), 200

    except Exception as e:
        return jsonify({
            'message': 'API deployment failed',
            'error': str(e),
            'status': 500,
            'statusText': 'Internal Server Error',
            'mime-type': 'application/json'
        }), 500

@api_bp.route('/check-new-apis', methods=['POST'])
@token_required
@api_access()
def check_new_apis(args, current_user):
    # current_user = g.current_user  # Access the user stored in g
    try:
        # Fetch all APIs from AWS API Gateway
        print('Fetching APIs from AWS...')
        response = api_gateway_client.get_rest_apis()
        aws_apis = response.get('items', [])
        # print('AWS APIs : ', aws_apis)

        # Initialize the API model
        api_collection = Api()

        # Get the list of APIs already stored in MongoDB
        stored_apis = api_collection.get_all_apis()
        # print('Stored APIs : ', stored_apis)
        stored_api_ids = {str(api['id']) for api in stored_apis}
        # print('Stored API IDs : ', stored_api_ids)

        # Find new APIs
        new_apis = []
        for aws_api in aws_apis:
            if aws_api['id'] not in stored_api_ids:  # Check if the API ID is new
                new_apis.append(aws_api)

        api_details = []
        for api in new_apis:
            stages_response = api_gateway_client.get_stages(restApiId=api['id'])
            stages = stages_response.get('item', [])

            stage_names = [stage['stageName'] for stage in stages]

            api_details.append({
                'id': api['id'],
                'name': api['name'],
                'description': api.get('description', 'No description provided'),
                'createdDate': api['createdDate'].strftime('%Y-%m-%d %H:%M:%S'),
                'version': api.get('version', 'N/A'),
                'stages': stage_names  # Include stages
            })

        if new_apis:
            # Add new APIs to MongoDB
            api_collection.insert_apis(api_details)

        # Convert any ObjectId in new_apis to a string before returning the response
        serialized_new_apis = []
        for api in api_details:
            if '_id' in api:
                api['_id'] = str(api['_id'])  # Convert ObjectId to string

            serialized_new_apis.append(api)

        # print('New APIs : ', serialized_new_apis)
        return jsonify({
            'message': 'APIs checked successfully',
            'newApis': serialized_new_apis,  # Return only the new APIs
            'status': 200,
            'statusText': 'OK',
            'mime-type': 'application/json'
        }), 200

    except Exception as e:
        return jsonify({
            'message': 'Failed to check new APIs',
            'error': str(e),
            'status': 500,
            'statusText': 'Internal Server Error',
            'mime-type': 'application/json'
        }), 500



@api_bp.route('/list-apis', methods=['GET'])
@check_user_role(['Administrator', 'DevOps Engineer', 'Developer', 'Tester'])
@token_required
def list_apis(current_user):
    try:
        # Fetch all APIs
        response = api_gateway_client.get_rest_apis()

        api_details = []
        for api in response.get('items', []):
            # Fetch stages for each API
            stages_response = api_gateway_client.get_stages(restApiId=api['id'])
            stages = stages_response.get('item', [])

            # Collect stage names
            stage_names = [stage['stageName'] for stage in stages]

            # Add API details along with stages
            api_details.append({
                'id': api['id'],
                'name': api['name'],
                'description': api.get('description', 'No description provided'),
                'createdDate': api['createdDate'].strftime('%Y-%m-%d %H:%M:%S'),
                'version': api.get('version', 'N/A'),
                'stages': stage_names  # Include stages
            })

        return jsonify({
            'message': 'APIs fetched successfully',
            'apis': api_details,
            'status': 200,
            'statusText': 'OK',
            'mime-type': 'application/json'
        }), 200

    except Exception as e:
        return jsonify({
            'message': 'Failed to fetch APIs',
            'error': str(e),
            'status': 500,
            'statusText': 'Internal Server Error',
            'mime-type': 'application/json'
        }), 500
