import requests
from config import ZAP_BASE_URL, ZAP_API_KEY

def spider_target(api_endpoint):
    spider_url = f'{ZAP_BASE_URL}/JSON/spider/action/scan/?apikey={ZAP_API_KEY}&url={api_endpoint}'
    response = requests.get(spider_url)
    return response.json()

def is_spider_complete(spider_id):
    spider_status_url = f'{ZAP_BASE_URL}/JSON/spider/view/status/?apikey={ZAP_API_KEY}&scanId={spider_id}'
    response = requests.get(spider_status_url)
    return response.json()

def start_zap_scan(api_endpoint):
    scan_url = f'{ZAP_BASE_URL}/JSON/ascan/action/scan/?apikey={ZAP_API_KEY}&url={api_endpoint}'
    response = requests.get(scan_url)
    return response.json()

def get_zap_scan_status(scan_id):
    status_url = f'{ZAP_BASE_URL}/JSON/ascan/view/status/?apikey={ZAP_API_KEY}&scanId={scan_id}'
    response = requests.get(status_url)
    return response.json()

def get_zap_scan_results():
    results_url = f'{ZAP_BASE_URL}/JSON/core/view/alerts/?apikey={ZAP_API_KEY}&baseurl=&start=&count='
    response = requests.get(results_url)
    return response.json()


