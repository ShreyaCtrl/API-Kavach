from models.api import Api
from flask import Blueprint, jsonify, request
from aws import api_gateway_client
from middleware.issue_tokens import token_required
from middleware.authorize import check_user_role

api = Blueprint('api', __name__)

@api.route('/list-apis', methods=['GET'])
@check_user_role(['Administrator', 'DevOps Engineer'])
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

@api.route('/deploy-api', methods=['POST'])
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