import requests
from celery_app import app

@app.task
def call_api():
    url = "//////" 
    try:
        response = requests.get(url)
        response.raise_for_status()
        print(f"API call successful: {response.status_code}")
        return response.json()
    except requests.RequestException as e:
        print(f"API call failed: {str(e)}")
        return None