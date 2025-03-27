import os

API_KEY = os.getenv('API_KEY', '')
API_HOST = os.getenv('API_HOST', 'http://10.109.200.53:8088')
OUTPUT_LOG_SWITCH = os.getenv('OUTPUT_LOG_SWITCH', 'false').lower() == 'true'
