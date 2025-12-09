# Architecture Overview

## Before Refactoring

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND (Browser)                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │   List   │  │   Grid   │  │ Accordion│  │  Modals  │       │
│  │   View   │  │   View   │  │   View   │  │  & Copy  │       │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP Requests
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    BACKEND (FastAPI Server)                      │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  POST /api/login                                           │ │
│  │  - Sends credentials to external API                      │ │
│  │  - Receives session token                                 │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              │                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  GET /api/refresh-token                                    │ │
│  │  - Uses session to get auth token from external API       │ │
│  │  - Caches token for 5 seconds                             │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              │                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  GET /api/console-data                                     │ │
│  │  - Uses auth token to fetch data from external API        │ │
│  │  - Processes and returns data                             │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ External API Calls
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              EXTERNAL API (v2.mnitnetwork.com)                   │
│  - Authentication endpoint                                       │
│  - Token refresh endpoint                                        │
│  - Console data endpoint                                         │
└─────────────────────────────────────────────────────────────────┘
```

## After Refactoring

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND (Browser)                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │   List   │  │   Grid   │  │ Accordion│  │  Modals  │       │
│  │   View   │  │   View   │  │   View   │  │  & Copy  │       │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │
│                                                                   │
│  ✓ All rendering logic preserved                                │
│  ✓ Color assignment preserved                                   │
│  ✓ Auto-refresh every 5 seconds                                 │
│  ✗ No login logic                                               │
│  ✗ No token management                                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ GET /api/console-data
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    BACKEND (FastAPI Server)                      │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  GET /api/console-data                                     │ │
│  │  - Retrieves data from local SQLite database              │ │
│  │  - Returns data in same format as before                  │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              ▲                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  POST /api/console-data                                    │ │
│  │  - Receives data from external sources                    │ │
│  │  - Processes and stores in database                       │ │
│  │  - Assigns colors to app names                            │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              ▲                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  SQLite Database (app.db)                                  │ │
│  │  - messages table                                          │ │
│  │  - Stores: app_name, carrier, sms, time, color            │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │ POST data
                              │
┌─────────────────────────────────────────────────────────────────┐
│                    DATA SOURCES (Your Choice)                    │
│                                                                   │
│  Option 1: Manual Script (post_data_example.py)                 │
│  Option 2: Scheduled Task (integration_example.py)              │
│  Option 3: External System (your custom integration)            │
│  Option 4: Original External API (if still accessible)          │
└─────────────────────────────────────────────────────────────────┘
```

## Key Differences

### Data Flow

**Before:**
```
Frontend → Backend → External API → Backend → Frontend
(Every request goes to external API)
```

**After:**
```
Data Source → Backend → Database
Frontend → Backend → Database → Frontend
(Frontend reads from local database)
```

### Components

| Component | Before | After | Status |
|-----------|--------|-------|--------|
| Frontend Views | ✓ | ✓ | Preserved |
| Color Assignment | ✓ | ✓ | Preserved |
| Auto-refresh | ✓ | ✓ | Preserved |
| Animations | ✓ | ✓ | Preserved |
| Login System | ✓ | ✗ | Removed |
| Token Management | ✓ | ✗ | Removed |
| External API Calls | ✓ | ✗ | Removed |
| Local Database | ✗ | ✓ | Added |
| POST API Endpoint | ✗ | ✓ | Added |

## Database Schema

```sql
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    app_name VARCHAR NOT NULL,
    carrier VARCHAR NOT NULL,
    sms TEXT NOT NULL,
    time VARCHAR NOT NULL,
    color VARCHAR,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_app_name ON messages(app_name);
```

## API Contract

### POST /api/console-data

**Request:**
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
        "color": "#1877f2"  // Optional, auto-assigned if not provided
      }
    ]
  },
  "message": "Optional message"  // Optional
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

## Benefits of New Architecture

1. **Independence**: No dependency on external API availability
2. **Performance**: Faster response times (local database vs external API)
3. **Control**: You control when and how data is updated
4. **Security**: No hardcoded credentials in the application
5. **Flexibility**: Can receive data from multiple sources
6. **Reliability**: Works offline, no network issues
7. **Simplicity**: Fewer moving parts, easier to maintain

## Migration Path

1. **Phase 1**: Deploy refactored application
2. **Phase 2**: Set up data posting mechanism (script/integration)
3. **Phase 3**: Test with sample data
4. **Phase 4**: Connect to real data source
5. **Phase 5**: Monitor and optimize

## Deployment Considerations

- Database file (`app.db`) should be backed up regularly
- Consider using PostgreSQL for production instead of SQLite
- Set up monitoring for the POST endpoint
- Implement rate limiting if needed
- Add authentication to POST endpoint if required
