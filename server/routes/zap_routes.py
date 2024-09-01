from flask import jsonify, request, Blueprint
from middleware.api_access import api_access
from middleware.authorize import check_user_role
from middleware.issue_tokens import token_required
from models.zap import spider_target, is_spider_complete, start_zap_scan, get_zap_scan_results, get_zap_scan_status
from models.zap_scans import Zap_scan
from models.zap_alerts import Zap_alerts
import time

zap = Blueprint('zap', __name__)

@token_required
@zap.route('/scans', methods=['GET'])
def get_all_scans():
    scan_collection = Zap_scan()
    scans = scan_collection.find_scan()
    all_scans = []

    for scan in scans:
        # Convert ObjectId to string for easier JSON serialization
        scan['_id'] = str(scan['_id'])

        # Convert ObjectId in alert_ids to string
        scan['alert_ids'] = [str(alert_id) for alert_id in scan['alert_ids']]

        # Fetch the details of each alert
        alerts = []
        alert_collection = Zap_alerts()
        for alert_id in scan['alert_ids']:
            alert = alert_collection.fetch_alert_by_id(alert_id)
            if alert:
                alert['_id'] = str(alert['_id'])  # Convert ObjectId to string
                alerts.append(alert)

        scan['alerts'] = alerts
        all_scans.append(scan)

    return jsonify(all_scans)

@zap.route('/test-api-endpoint', methods=['POST'])
@token_required
def test_api_endpoint():
    data = request.json
    api_endpoint = data.get('api_endpoint')
    if not api_endpoint:
        return jsonify({'error': 'API endpoint is required'}), 400

    # Spider the target to discover all URLs
    spider_response = spider_target(api_endpoint)
    spider_id = spider_response.get('scan')

    # Wait for the spider to complete
    while True:
        spider_status = is_spider_complete(spider_id)
        if spider_status.get('status') == '100':  # Spider is complete
            break
        print("Spidering in progress...")  # Log spidering progress
        time.sleep(5)  # Wait for 5 seconds before checking again

    # Start the ZAP scan after spidering is complete
    scan_response = start_zap_scan(api_endpoint)
    scan_id = scan_response.get('scan')

    # Wait for the scan to complete
    while True:
        scan_status = get_zap_scan_status(scan_id)
        if scan_status.get('status') == '100':  # Scan is complete
            break
        print("Scanning in progress...")  # Log scan progress
        time.sleep(5)  # Wait for 5 seconds before checking again

    # Get the scan results
    scan_results = get_zap_scan_results()
    alerts = scan_results.get('alerts', [])

    alert_collection = Zap_alerts()
    # Store each alert in MongoDB
    stored_alert_ids = []
    for alert in alerts:
        alert_id = alert_collection.store_alert(alert)
        stored_alert_ids.append(alert_id)

    # Store scan metadata
    scan_metadata = {
        'scan_id': scan_id,
        'spider_id': spider_id,
        'alert_ids': stored_alert_ids,
        'timestamp': time.time()
    }
    scan_collection = Zap_scan()
    scan_collection.store_scan(scan_metadata)

    str_alerts = []
    for alert in stored_alert_ids:
        str_alerts.append(str(alert))
    return jsonify({'spider_id': spider_id, 'scan_id': scan_id, 'alert_ids': str_alerts})
