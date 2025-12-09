# API Refactoring Documentation

## Overview
The application has been refactored from an external API-based system to a local database-driven API system.

## What Changed

### Before (Old Flow)
1. Frontend calls `/api/login` with credentials
2. Backend logs into external API → receives session
3. Frontend calls `/api/refresh-token` 
4. Backend uses session to get token from external API
5. Frontend calls `/api/console-data`
6. Backend fetches data from external API using token
7. Data is processed and returned to frontend

### After (New Flow)
1. External system/script posts data to `/api/console-data` (POST)
2. Backend stores data in local SQLite database
3. Frontend calls `/api/console-data` (GET)
4. Backend retrieves data from local database
5. Data is returned to frontend with same format

## API Endpoints

### POST /api/console-data
**Purpose:** Receive and store console data from external sources

**Request Body:**
```json
{
  "meta": {
    "status": "success",
    "timestamp": "2024-12-09T10:30:00"
  },
  "data": {
    "messages": [
      {
        "app_name": "Facebook",
        "carrier": "236724XXX",
        "sms": "Your verification code is 123456",
        "time": "2 minutes ago",
        "color": "#1877f2"
      }
    ]
  },
  "message": "Optional message"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Data stored successfully",
  "count": 1
}
```

### GET /api/console-data
**Purpose:** Retrieve console data from local database

**Response:**
```json
{
  "meta": {
    "status": "success",
    "timestamp": "2024-12-09T10:30:00"
  },
  "data": {
    "messages": [
      {
        "app_name": "Facebook",
        "carrier": "236724XXX",
        "sms": "Your verification code is 123456",
        "time": "2 minutes ago",
        "color": "#1877f2"
      }
    ]
  }
}
```

## Database Schema

### Messages Table
- `id`: Integer (Primary Key)
- `app_name`: String (indexed)
- `carrier`: String
- `sms`: Text
- `time`: String
- `color`: String
- `created_at`: DateTime

## Frontend Changes

### Removed
- Login functionality
- Token refresh logic
- External API authentication

### Kept
- All rendering logic (list, accordion, grid views)
- Color assignment for app names
- Auto-refresh every 5 seconds
- Copy to clipboard functionality
- All animations and UI features

## How to Use

### 1. Start the Application
```bash
python main.py
```
or
```bash
uvicorn main:app --host 0.0.0.0 --port 8002
```

### 2. Post Data to API
Use the provided example script:
```bash
python post_data_example.py
```

Or use curl:
```bash
curl -X POST http://localhost:8002/api/console-data \
  -H "Content-Type: application/json" \
  -d '{
    "meta": {"status": "success"},
    "data": {
      "messages": [
        {
          "app_name": "Facebook",
          "carrier": "236724XXX",
          "sms": "Your code is 123456",
          "time": "2 minutes ago"
        }
      ]
    }
  }'
```

### 3. View Data
Open browser: `http://localhost:8002`

## Integration Guide

To integrate with your existing system:

1. **Identify where you currently fetch console data**
2. **Instead of calling the external API, call your local API:**
   ```python
   import requests
   
   payload = {
       "meta": {"status": "success"},
       "data": {"messages": your_messages_list}
   }
   
   requests.post("http://localhost:8002/api/console-data", json=payload)
   ```

3. **The frontend will automatically display the data**

## Benefits

1. **No External Dependencies**: No need for external API credentials
2. **Faster Response**: Data served from local database
3. **Better Control**: You control when and how data is updated
4. **Same UI**: All rendering logic remains unchanged
5. **Flexible**: Can receive data from any source that posts to the API

## Migration Notes

- The database is automatically created on first run
- Old data is replaced when new data is posted
- Color assignment logic is preserved
- All frontend features work exactly the same way
