# Data Flow Diagram

## Complete System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    v2.mnitnetwork.com                            │
│                                                                   │
│  User logs in → Navigates to console → API call triggered       │
│                                                                   │
│  GET /api/v1/mnitnetworkcom/dashboard/getconsole                │
│                          ↓                                        │
│                   Response with data                             │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              │ ① Intercepted by
                              │    Chrome Extension
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│              Chrome Extension (Content Script)                   │
│                                                                   │
│  • Intercepts fetch/XHR requests                                │
│  • Detects /dashboard/getconsole endpoint                       │
│  • Captures response data                                        │
│  • Sends to background script                                    │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              │ ② Forwards data
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│           Chrome Extension (Background Worker)                   │
│                                                                   │
│  • Receives data from content script                            │
│  • Checks if interceptor is enabled                             │
│  • Forwards to configured backend URL                           │
│  • Updates badge with status                                     │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              │ ③ POST request
                              │    with JSON payload
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Local Backend API                             │
│                  (http://localhost:8002)                         │
│                                                                   │
│  POST /api/console-data                                         │
│  • Receives intercepted data                                     │
│  • Processes messages                                            │
│  • Assigns colors to app names                                   │
│  • Stores in SQLite database                                     │
│                          ↓                                        │
│                   ┌──────────────┐                              │
│                   │   app.db     │                              │
│                   │  (SQLite)    │                              │
│                   └──────────────┘                              │
│                          ↓                                        │
│  GET /api/console-data                                          │
│  • Retrieves messages from database                             │
│  • Returns formatted JSON                                        │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              │ ④ Frontend fetches
                              │    every 5 seconds
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Frontend (Browser)                            │
│                  (http://localhost:8002)                         │
│                                                                   │
│  • Auto-refresh every 5 seconds                                 │
│  • Fetches data from GET /api/console-data                      │
│  • Renders in list/grid/accordion view                          │
│  • Shows animations for new messages                            │
│  • Provides copy-to-clipboard functionality                     │
└─────────────────────────────────────────────────────────────────┘
```

## Data Format

### Intercepted from v2.mnitnetwork.com

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

### Stored in Database

```
messages table:
┌────┬──────────┬───────────┬─────────────────────┬──────────────┬──────────┬─────────────────────┐
│ id │ app_name │  carrier  │         sms         │     time     │  color   │     created_at      │
├────┼──────────┼───────────┼─────────────────────┼──────────────┼──────────┼─────────────────────┤
│ 1  │ Facebook │ 236724XXX │ Your code is 123456 │ 2 minutes ago│ #1877f2  │ 2024-12-09 10:30:00 │
└────┴──────────┴───────────┴─────────────────────┴──────────────┴──────────┴─────────────────────┘
```

### Served to Frontend

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

## Extension Components

### 1. Content Script (content.js)
- **Runs on**: v2.mnitnetwork.com pages
- **Purpose**: Intercept API calls
- **Method**: Overrides fetch() and XMLHttpRequest
- **Triggers**: When /dashboard/getconsole is called

### 2. Background Worker (background.js)
- **Runs**: In background (service worker)
- **Purpose**: Forward data to backend
- **Method**: Receives messages from content script
- **Action**: POST to configured backend URL

### 3. Popup UI (popup.html/js)
- **Runs**: When extension icon clicked
- **Purpose**: Configuration and testing
- **Features**:
  - Backend URL input
  - Enable/disable toggle
  - Test connection button
  - Statistics display

## User Interactions

### Setup Flow
```
1. User installs extension
   ↓
2. User clicks extension icon
   ↓
3. User enters backend URL
   ↓
4. User clicks "Save Settings"
   ↓
5. User clicks "Test Connection"
   ↓
6. Extension confirms connection
```

### Runtime Flow
```
1. User visits v2.mnitnetwork.com
   ↓
2. User logs in
   ↓
3. User navigates to console
   ↓
4. Page makes API call
   ↓
5. Extension intercepts automatically
   ↓
6. Data forwarded to backend
   ↓
7. Badge shows ✓ (success) or ✗ (error)
   ↓
8. User opens http://localhost:8002
   ↓
9. Sees data displayed with all features
```

## Error Handling

### Extension Side
```
API Call → Intercept → Forward to Backend
                ↓
            If fails:
            • Show ✗ badge
            • Log error to console
            • Continue intercepting
```

### Backend Side
```
Receive Data → Validate → Store in DB
                ↓
            If fails:
            • Return error response
            • Log error
            • Keep old data
```

### Frontend Side
```
Fetch Data → Display
     ↓
  If fails:
  • Keep showing old data
  • Log error to console
  • Retry on next interval
```

## Benefits of This Architecture

1. **Decoupled**: Extension and backend are independent
2. **Flexible**: Backend URL can be changed anytime
3. **Reliable**: Data persists in local database
4. **Fast**: No external API dependencies
5. **Secure**: Data stays on your infrastructure
6. **Scalable**: Can handle multiple data sources
7. **Maintainable**: Clear separation of concerns

## Alternative Data Sources

Besides the Chrome extension, you can also post data from:

1. **Python Script**: `python post_data_example.py`
2. **Cron Job**: Scheduled data fetching
3. **Webhook**: External service posts to your API
4. **Manual**: curl/Postman for testing
5. **Another App**: Any app can POST to the API

All sources use the same endpoint: `POST /api/console-data`
