import urllib.request
import os
import json
from dotenv import load_dotenv

load_dotenv()

def makeRequest(method: str, **params) -> dict:
    token = os.getenv('TOKEN')
    base_uri = os.getenv('TELEGRAM_BASE_URI')
    
    # Проверяем что переменные загружены
    if not token or not base_uri:
        print("Error: TOKEN or TELEGRAM_BASE_URI not found in .env file")
        return {}
    
    url = f"{base_uri}/bot{token}/{method}"
    
    if method in ['getMe', 'getUpdates'] and params:
        query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        url = f"{url}?{query_string}"
        request_data = None
    else:
        request_data = json.dumps(params, ensure_ascii=False).encode('utf-8') if params else None
    
    request = urllib.request.Request(
        url=url,
        data=request_data,
        headers={"Content-Type": "application/json; charset=utf-8"} if request_data else {}
    )

    try:
        with urllib.request.urlopen(request) as response:
            response_body = response.read().decode("utf-8")
            response_json = json.loads(response_body)
            return response_json["result"] if response_json["ok"] else {}
    except Exception as e:
        print(f"Error: {e}")
        return {}

def getUpdates(offset: int) -> list:
    result = makeRequest('getUpdates', offset=offset, timeout=30)
    return result if result else []

def sendMessage(chat_id: int, text: str) -> dict:
    return makeRequest('sendMessage', chat_id=chat_id, text=text)

def getMe() -> dict:
    return makeRequest('getMe')