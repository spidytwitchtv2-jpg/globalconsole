"""
Integration Example: How to fetch data from external API and post to local API

This example shows how to:
1. Fetch data from the original external API (if you still have access)
2. Transform it to the expected format
3. Post it to your local API

You can run this script periodically (e.g., via cron job) to keep your local database updated.
"""
import requests
import json
from datetime import datetime

# Configuration
LOCAL_API_URL = "http://localhost:8002/api/console-data"
EXTERNAL_API_URL = "https://v2.mnitnetwork.com/api/v1/mnitnetworkcom/dashboard/getconsole"

# If you still have access to the external API, use these credentials
EXTERNAL_EMAIL = "your-email@example.com"
EXTERNAL_PASSWORD = "your-password"

def fetch_from_external_api(token):
    """
    Fetch data from external API (if you still have access)
    """
    headers = {
        'accept': '*/*',
        'content-type': 'application/json',
        'mhitauth': token,
    }
    
    try:
        response = requests.get(EXTERNAL_API_URL, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"External API error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching from external API: {e}")
        return None

def transform_data(external_data):
    """
    Transform external API response to match local API format
    The external API already returns data in the correct format,
    so we just need to ensure it has the required structure.
    """
    if not external_data:
        return None
    
    # The external API response should already have meta and data
    # Just ensure it's in the right format
    return {
        "meta": external_data.get("meta", {"status": "success"}),
        "data": external_data.get("data", {"messages": []}),
        "message": external_data.get("message", "Data fetched successfully")
    }

def post_to_local_api(payload):
    """
    Post transformed data to local API
    """
    try:
        response = requests.post(
            LOCAL_API_URL,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Successfully posted {result.get('count', 0)} messages to local API")
            return True
        else:
            print(f"✗ Error posting to local API: {response.status_code}")
            print(f"Details: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Exception posting to local API: {e}")
        return False

def create_sample_data():
    """
    Create sample data for testing (when you don't have external API access)
    """
    return {
        "meta": {
            "status": "success",
            "timestamp": datetime.utcnow().isoformat()
        },
        "data": {
            "messages": [
                {
                    "app_name": "Facebook",
                    "carrier": "236724001",
                    "sms": "Your Facebook verification code is 123456",
                    "time": "2 minutes ago",
                    "color": "#1877f2"
                },
                {
                    "app_name": "Google",
                    "carrier": "236725002",
                    "sms": "Your Google verification code is 789012",
                    "time": "5 minutes ago",
                    "color": "#4285f4"
                },
                {
                    "app_name": "WhatsApp",
                    "carrier": "236726003",
                    "sms": "Your WhatsApp code is 345678",
                    "time": "10 minutes ago",
                    "color": "#25d366"
                },
                {
                    "app_name": "Instagram",
                    "carrier": "236727004",
                    "sms": "Your Instagram code is 901234",
                    "time": "15 minutes ago",
                    "color": "#e4405f"
                },
                {
                    "app_name": "Twitter",
                    "carrier": "236728005",
                    "sms": "Your Twitter verification code is 567890",
                    "time": "20 minutes ago",
                    "color": "#1da1f2"
                }
            ]
        },
        "message": "Sample data for testing"
    }

def main():
    """
    Main integration function
    """
    print("=" * 60)
    print("CONSOLE DATA INTEGRATION")
    print("=" * 60)
    
    # Option 1: Use sample data (for testing)
    print("\nUsing sample data for demonstration...")
    payload = create_sample_data()
    
    # Option 2: Fetch from external API (uncomment if you have access)
    # print("\nFetching from external API...")
    # external_data = fetch_from_external_api(YOUR_TOKEN)
    # payload = transform_data(external_data)
    
    if payload:
        print(f"\nPayload preview:")
        print(f"- Messages count: {len(payload['data']['messages'])}")
        print(f"- First message: {payload['data']['messages'][0]['app_name']}")
        
        print("\nPosting to local API...")
        success = post_to_local_api(payload)
        
        if success:
            print("\n✓ Integration successful!")
            print("View the data at: http://localhost:8002")
        else:
            print("\n✗ Integration failed!")
    else:
        print("\n✗ No data to post!")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
