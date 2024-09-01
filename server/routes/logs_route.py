from models.api import Api
from middleware.issue_tokens import token_required
from middleware.api_access import api_access
from middleware.authorize import check_user_role
from flask import request, jsonify, Blueprint
from aws import logs_client
from datetime import datetime, timedelta

# Define the log group for the API Gateway
LOG_GROUP_NAME = '/API-Gateway-Execution-Logs_qycpsfswxa/dev'

logs = Blueprint('logs', __name__)

@logs.route('/api-requests', methods=['GET'])
def get_api_requests():
    """
    Fetch the number of API requests over a given time period.
    """
    start_time = request.args.get('start_time', (datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%SZ'))
    end_time = request.args.get('end_time', datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'))

    response = logs_client.filter_log_events(
        logGroupName=LOG_GROUP_NAME,
        startTime=int(datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%SZ').timestamp() * 1000),
        endTime=int(datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%SZ').timestamp() * 1000),
        filterPattern='"HTTPMethod" "RequestId"'
    )

    requests_count = len(response.get('events', []))

    return jsonify({'requests_count': requests_count, 'start_time': start_time, 'end_time': end_time})

@logs.route('/api/errors', methods=['GET'])
def get_api_errors():
    """
    Fetch the number of errors (4xx and 5xx) within a given time period.
    """
    start_time = request.args.get('start_time', (datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%SZ'))
    end_time = request.args.get('end_time', datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'))

    response = logs_client.filter_log_events(
        logGroupName=LOG_GROUP_NAME,
        startTime=int(datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%SZ').timestamp() * 1000),
        endTime=int(datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%SZ').timestamp() * 1000),
        filterPattern='"status": "4" || "status": "5"'
    )

    errors_count = len(response.get('events', []))

    return jsonify({'errors_count': errors_count, 'start_time': start_time, 'end_time': end_time})

@logs.route('/api/latency', methods=['GET'])
def get_api_latency():
    """
    Fetch average API latency over a given time period.
    """
    start_time = request.args.get('start_time', (datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%SZ'))
    end_time = request.args.get('end_time', datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'))

    response = logs_client.filter_log_events(
        logGroupName=LOG_GROUP_NAME,
        startTime=int(datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%SZ').timestamp() * 1000),
        endTime=int(datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%SZ').timestamp() * 1000),
        filterPattern='"integrationLatency"'
    )

    latencies = []
    for event in response.get('events', []):
        log_message = event['message']
        latency_value = int(log_message.split('"integrationLatency":')[1].split(',')[0].strip())
        latencies.append(latency_value)

    average_latency = sum(latencies) / len(latencies) if latencies else 0

    return jsonify({'average_latency': average_latency, 'start_time': start_time, 'end_time': end_time})

@logs.route('/api/status-codes', methods=['GET'])
def get_status_codes_distribution():
    """
    Fetch the distribution of HTTP status codes within a given time period.
    """
    start_time = request.args.get('start_time', (datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%SZ'))
    end_time = request.args.get('end_time', datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'))

    response = logs_client.filter_log_events(
        logGroupName=LOG_GROUP_NAME,
        startTime=int(datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%SZ').timestamp() * 1000),
        endTime=int(datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%SZ').timestamp() * 1000),
        filterPattern='"status"'
    )

    status_codes = {}
    for event in response.get('events', []):
        log_message = event['message']
        status_code = log_message.split('"status":')[1].split(',')[0].strip()
        status_codes[status_code] = status_codes.get(status_code, 0) + 1

    return jsonify({'status_codes_distribution': status_codes, 'start_time': start_time, 'end_time': end_time})
