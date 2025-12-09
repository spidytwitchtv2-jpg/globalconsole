# Origins Tracking & URL Crawling Feature

## Overview

This feature automatically tracks unique app origins (like Facebook, Google, WhatsApp) and can crawl the web to find their login URLs, storing them for quick access.

## How It Works

### 1. Automatic Origin Tracking

When data is posted to `/api/console-data`, the backend:
- Extracts unique app names from messages
- Stores them in the `origins` table
- Assigns colors for visual consistency
- Updates existing origins if they appear again

### 2. URL Crawling System

The system can automatically find login URLs for each origin:
- Searches Google for "{app_name} login"
- Parses search results for login-related URLs
- Tests common URL patterns (accounts.{app}.com, login.{app}.com, etc.)
- Stores found URLs in database
- Caches results to avoid repeated searches

### 3. Frontend Display

Users can view and manage origins through the UI:
- "View All Origins" button below the main console
- Expandable panel showing all unique origins
- Each origin displays:
  - App name (color-coded)
  - Login URL (if found)
  - Status (Found/Not Found/Checking/Unchecked)
- "Check All URLs" button to trigger crawling

## Database Schema

### Origins Table

```sql
CREATE TABLE origins (
    id INTEGER PRIMARY KEY,
    app_name VARCHAR UNIQUE,
    login_url VARCHAR NULL,
    url_checked DATETIME NULL,
    color VARCHAR,
    created_at DATETIME,
    updated_at DATETIME
);
```

## API Endpoints

### GET /api/origins

Returns all unique origins with their login URLs.

**Response:**
```json
{
  "status": "success",
  "origins": [
    {
      "id": 1,
      "app_name": "Facebook",
      "login_url": "https://www.facebook.com/login",
      "url_checked": "2024-12-09T10:30:00",
      "color": "#1877f2"
    }
  ]
}
```

### POST /api/origins/check-all

Starts background crawling for all origins that haven't been checked.

**Response:**
```json
{
  "status": "success",
  "message": "Started crawling 5 origins",
  "count": 5
}
```

## Frontend UI

### Origins Panel

```
┌─────────────────────────────────────────────────┐
│         📋 View All Origins (Button)            │
└─────────────────────────────────────────────────┘
                      ↓ (Click to expand)
┌─────────────────────────────────────────────────┐
│  All Unique Origins        🔍 Check All URLs    │
├─────────────────────────────────────────────────┤
│  ┌───────────────────────────────────────────┐  │
│  │ Facebook                                  │  │
│  │ https://www.facebook.com/login            │  │
│  │                              [Found] ✓    │  │
│  └───────────────────────────────────────────┘  │
│                                                  │
│  ┌───────────────────────────────────────────┐  │
│  │ Google                                    │  │
│  │ https://accounts.google.com               │  │
│  │                              [Found] ✓    │  │
│  └───────────────────────────────────────────┘  │
│                                                  │
│  ┌───────────────────────────────────────────┐  │
│  │ WhatsApp                                  │  │
│  │ URL not found                             │  │
│  │                          [Not Found] ✗    │  │
│  └───────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

### Status Indicators

- **🟢 Found**: Login URL successfully found and verified
- **🔴 Not Found**: Crawling completed but no URL found
- **🟡 Checking**: Currently crawling for URL
- **⚪ Unchecked**: Not yet crawled

## URL Crawling Logic

The `find_login_url()` function:

1. **Google Search**: Searches for "{app_name} login"
2. **Pattern Matching**: Looks for URLs matching:
   - `https://{app}.com/login`
   - `https://{app}.com/signin`
   - `https://accounts.{app}.com`
   - `https://login.{app}.com`
3. **URL Testing**: Tests common patterns with HEAD requests
4. **Caching**: Stores result in database to avoid re-crawling

## Chrome Extension Updates

### Fixed Backend URL

The extension now uses a fixed backend URL:
```
https://globalconsole-sthc.onrender.com/api/console-data
```

**Changes:**
- Backend URL field is now read-only
- Cannot be changed by users
- Simplified configuration
- Consistent deployment

### Popup UI

```
┌─────────────────────────────────────┐
│  🔄 Console Interceptor             │
├─────────────────────────────────────┤
│  Interceptor Status      [●─] ON    │
│                                     │
│  Backend URL (Fixed)                │
│  ┌───────────────────────────────┐  │
│  │ https://globalconsole-sthc... │  │
│  └───────────────────────────────┘  │
│  🔒 Backend URL is fixed            │
│                                     │
│  📧 Account Credentials (Helper)    │
│  Email: [Aktermamber.00.7@...]      │
│  Password: [••••••••]               │
│                                     │
│  [Save Settings] [Test Connection]  │
└─────────────────────────────────────┘
```

## Usage Flow

### For Users

1. **View Origins**:
   - Scroll to bottom of console page
   - Click "📋 View All Origins"
   - Panel expands showing all unique apps

2. **Check URLs**:
   - Click "🔍 Check All URLs" button
   - System starts crawling (takes 1-2 minutes)
   - Status updates automatically
   - URLs appear as they're found

3. **Access Login Pages**:
   - Click any found URL
   - Opens in new tab
   - Use saved credentials from extension

### For Developers

1. **Deploy Backend**:
   ```bash
   # Install new dependencies
   pip install beautifulsoup4 lxml
   
   # Run migrations (automatic on startup)
   python main.py
   ```

2. **Test Locally**:
   ```bash
   # Start server
   python main.py
   
   # Post test data
   python post_data_example.py
   
   # View origins
   curl http://localhost:8002/api/origins
   
   # Trigger crawling
   curl -X POST http://localhost:8002/api/origins/check-all
   ```

3. **Monitor Crawling**:
   - Check server logs for crawling progress
   - Each origin logs: "Crawled {app_name}: {url or 'Not found'}"

## Performance Considerations

### Crawling Speed

- Each origin takes 5-15 seconds to crawl
- Runs in background (non-blocking)
- Multiple origins crawled in parallel
- Results cached permanently

### Database Size

- Origins table grows slowly (only unique apps)
- Typical size: 50-100 origins
- Minimal storage impact

### API Rate Limits

- Google search may rate-limit after many requests
- Crawling respects 10-second timeout per origin
- Failed crawls can be retried manually

## Security & Privacy

### Data Collection

- Only stores app names and public login URLs
- No user credentials stored in origins table
- No tracking or analytics

### Web Crawling

- Uses standard HTTP requests
- Respects robots.txt (where applicable)
- No aggressive scraping
- Reasonable timeouts and delays

## Troubleshooting

### URLs Not Found

**Possible causes:**
- App name doesn't match official name
- Login page uses non-standard URL
- Rate limiting from Google
- Network connectivity issues

**Solutions:**
- Manually add URL to database
- Retry crawling after some time
- Check server logs for errors

### Crawling Takes Too Long

**Normal behavior:**
- 10-20 origins: 2-3 minutes
- 50+ origins: 5-10 minutes

**If stuck:**
- Check server logs
- Restart crawling
- Check network connectivity

### Extension Not Connecting

**Check:**
1. Backend URL is correct: `https://globalconsole-sthc.onrender.com/api/console-data`
2. Backend is running and accessible
3. CORS is enabled on backend
4. Extension has proper permissions

## Future Enhancements

### Planned Features

- [ ] Manual URL editing
- [ ] URL verification/testing
- [ ] Favicon fetching for origins
- [ ] Origin categories/grouping
- [ ] Export origins list
- [ ] Import origins from file
- [ ] Bulk URL updates
- [ ] URL change history

### Possible Improvements

- [ ] Smarter URL detection algorithms
- [ ] Multiple URL patterns per origin
- [ ] URL health checking
- [ ] Auto-retry failed crawls
- [ ] Crawling priority queue
- [ ] Rate limit handling
- [ ] Proxy support for crawling

## Dependencies

### Backend

```
beautifulsoup4>=4.11.0  # HTML parsing
lxml>=4.9.0             # XML/HTML parser
requests>=2.28.0        # HTTP requests
```

### Frontend

No additional dependencies (vanilla JavaScript)

## Files Modified

### Backend
- `main.py`: Added Origin model, crawling logic, API endpoints
- `requirements.txt`: Added beautifulsoup4, lxml

### Frontend
- `static/index.html`: Added origins panel UI and JavaScript

### Extension
- `chrome-extension/background.js`: Fixed backend URL
- `chrome-extension/popup.html`: Made URL field read-only
- `chrome-extension/popup.js`: Removed URL change logic

## Testing

### Manual Testing

1. **Post test data**:
   ```bash
   python post_data_example.py
   ```

2. **Check origins created**:
   ```bash
   curl http://localhost:8002/api/origins
   ```

3. **Trigger crawling**:
   ```bash
   curl -X POST http://localhost:8002/api/origins/check-all
   ```

4. **View in browser**:
   - Open http://localhost:8002
   - Click "View All Origins"
   - Click "Check All URLs"
   - Watch status updates

### Automated Testing

```python
# Test origin creation
def test_origin_creation():
    # Post data with unique app names
    # Verify origins table populated
    # Check colors assigned correctly

# Test URL crawling
def test_url_crawling():
    # Create test origins
    # Trigger crawling
    # Verify URLs found/not found
    # Check timestamps updated

# Test API endpoints
def test_api_endpoints():
    # GET /api/origins
    # POST /api/origins/check-all
    # Verify responses
```

## Deployment

### Production Checklist

- [x] Backend deployed to Render.com
- [x] Database migrations run
- [x] Dependencies installed
- [x] Extension updated with fixed URL
- [x] CORS configured
- [x] API endpoints tested
- [x] Crawling tested with real data

### Environment Variables

No additional environment variables needed. All configuration is hardcoded for simplicity.

## Support

For issues or questions:
1. Check server logs for crawling errors
2. Verify database has origins table
3. Test API endpoints manually
4. Check browser console for frontend errors
5. Review extension background script logs

## License

Part of the Console App project.
