"""
Example script to post console data to the API.
This demonstrates the expected payload format.
"""
import requests
import json
from datetime import datetime

# API endpoint
API_URL = "http://localhost:8002/api/console-data"

# Sample payload matching the external API response format
sample_payload = {
    "meta": {
        "status": "success",
        "timestamp": datetime.utcnow().isoformat()
    },
    "data": {
        "messages": [
            {
                "app_name": "Facebook",
                "carrier": "236724XXX",
                "sms": "Your verification code is 123456",
                "time": "2 minutes ago",
                "color": "#1877f2"
            },
            {
                "app_name": "Google",
                "carrier": "236725XXX",
                "sms": "Your Google verification code is 789012",
                "time": "5 minutes ago",
                "color": "#4285f4"
            },
            {
                "app_name": "WhatsApp",
                "carrier": "236726XXX",
                "sms": "Your WhatsApp code is 345678",
                "time": "10 minutes ago",
                "color": "#25d366"
            }
        ]
    },
    "message": "Console data retrieved successfully"
}

def post_console_data(payload):
    """Post console data to the API"""
    try:
        response = requests.post(
            API_URL,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print("✓ Data posted successfully!")
            print(f"Response: {response.json()}")
        else:
            print(f"✗ Error: {response.status_code}")
            print(f"Details: {response.text}")
            
    except Exception as e:
        print(f"✗ Exception occurred: {str(e)}")

if __name__ == "__main__":
    print("Posting sample console data to API...")
    print(f"Payload: {json.dumps(sample_payload, indent=2)}")
    print("-" * 50)
    post_console_data(sample_payload)
