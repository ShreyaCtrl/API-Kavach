from flask import Flask, jsonify, Blueprint
from datetime import datetime, timedelta
import random

logs = Blueprint('logs', __name__)
def generate_dummy_data(log_group, metric_name, num_points=10):
    now = datetime.utcnow()
    data = {
        "logGroup": log_group,
        "metrics": {
            metric_name: []
        }
    }
    for i in range(num_points):
        timestamp = now - timedelta(hours=num_points - i)
        value = random.randint(50, 200)  # Random value for demonstration
        data["metrics"][metric_name].append({
            "timestamp": timestamp.isoformat() + "Z",
            "count": value
        })
    return data

@logs.route('/api-requests', methods=['GET'])
def get_api_requests():
    data = {
        "/aws/apigateway/welcome": generate_dummy_data('/aws/apigateway/welcome', 'requests'),
        "/aws/lambda/stupid-test-api": generate_dummy_data('/aws/lambda/stupid-test-api', 'requests'),
        "/aws/lambda/test-function": generate_dummy_data('/aws/lambda/test-function', 'requests'),
        "/aws/lambda/test-fxn": generate_dummy_data('/aws/lambda/test-fxn', 'requests'),
        "API-Gateway-Execution-Logs_qycpsfswxa/dev": generate_dummy_data('API-Gateway-Execution-Logs_qycpsfswxa/dev', 'requests')
    }
    return jsonify(data)

@logs.route('/api-errors', methods=['GET'])
def get_api_errors():
    data = {
        "/aws/apigateway/welcome": generate_dummy_data('/aws/apigateway/welcome', 'errors'),
        "/aws/lambda/stupid-test-api": generate_dummy_data('/aws/lambda/stupid-test-api', 'errors'),
        "/aws/lambda/test-function": generate_dummy_data('/aws/lambda/test-function', 'errors'),
        "/aws/lambda/test-fxn": generate_dummy_data('/aws/lambda/test-fxn', 'errors'),
        "API-Gateway-Execution-Logs_qycpsfswxa/dev": generate_dummy_data('API-Gateway-Execution-Logs_qycpsfswxa/dev', 'errors')
    }
    return jsonify(data)

@logs.route('/api-latency', methods=['GET'])
def get_api_latency():
    data = {
        "/aws/apigateway/welcome": generate_dummy_data('/aws/apigateway/welcome', 'latency'),
        "/aws/lambda/stupid-test-api": generate_dummy_data('/aws/lambda/stupid-test-api', 'latency'),
        "/aws/lambda/test-function": generate_dummy_data('/aws/lambda/test-function', 'latency'),
        "/aws/lambda/test-fxn": generate_dummy_data('/aws/lambda/test-fxn', 'latency'),
        "API-Gateway-Execution-Logs_qycpsfswxa/dev": generate_dummy_data('API-Gateway-Execution-Logs_qycpsfswxa/dev', 'latency')
    }
    # Add average latency to each log group
    for log_group_data in data.values():
        for entry in log_group_data["metrics"]["latency"]:
            entry["averageLatency"] = random.randint(100, 300)  # Random average latency value
    return jsonify(data)

@logs.route('/api-status-codes', methods=['GET'])
def get_api_status_codes():
    statuses = [200, 400, 500]
    data = {
        "/aws/apigateway/welcome": generate_dummy_data('/aws/apigateway/welcome', 'statusCodes'),
        "/aws/lambda/stupid-test-api": generate_dummy_data('/aws/lambda/stupid-test-api', 'statusCodes'),
        "/aws/lambda/test-function": generate_dummy_data('/aws/lambda/test-function', 'statusCodes'),
        "/aws/lambda/test-fxn": generate_dummy_data('/aws/lambda/test-fxn', 'statusCodes'),
        "API-Gateway-Execution-Logs_qycpsfswxa/dev": generate_dummy_data('API-Gateway-Execution-Logs_qycpsfswxa/dev', 'statusCodes')
    }
    # Add random status codes and counts to each log group
    for log_group_data in data.values():
        for entry in log_group_data["metrics"]["statusCodes"]:
            entry["statusCode"] = random.choice(statuses)
            entry["count"] = random.randint(0, 20)  # Random count for each status code
    return jsonify(data)
