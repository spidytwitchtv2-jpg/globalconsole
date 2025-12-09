# Complete Installation & Setup Guide

## Overview

Your application has been successfully refactored into two components:

1. **Backend API** - Receives and serves console data from a local database
2. **Chrome Extension** - Intercepts API calls from v2.mnitnetwork.com and forwards to backend

## Quick Start (5 Minutes)

### Step 1: Start the Backend (2 min)

```bash
# Install dependencies (if not already installed)
pip install -r requirements.txt

# Start the server
python main.py
```

Server will start at: `http://localhost:8002`

### Step 2: Install Chrome Extension (2 min)

1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode" (toggle in top-right)
3. Click "Load unpacked"
4. Select the `chrome-extension` folder
5. Extension icon should appear in toolbar

### Step 3: Test the Setup (1 min)

1. Click the extension icon
2. Verify backend URL is: `http://localhost:8002/api/console-data`
3. Click "Test Connection" button
4. Should see "✓ Connection successful!"
5. Open `http://localhost:8002` in browser
6. Should see the test message displayed

## How to Use

### Automatic Data Capture

1. **Ensure backend is running**: `python main.py`

2. **Open extension popup** and verify:
   - Toggle is ON (enabled)
   - Backend URL is correct

3. **Visit v2.mnitnetwork.com** and log in with your credentials

4. **Navigate to console/dashboard** where the API calls happen

5. **Extension automatically intercepts** the API calls and forwards data

6. **View data** at `http://localhost:8002`
   - Data refreshes automatically every 5 seconds
   - All original features work (list/grid view, colors, animations)

### Manual Testing

Use the provided scripts to test without the external website:

```bash
# Send sample data
python post_data_example.py

# Or use the integration example
python integration_example.py
```

## Architecture

### Before Refactoring
```
Frontend → Login API → Token API → External Console API → Display
```

### After Refactoring
```
v2.mnitnetwork.com → Chrome Extension → Local Backend API → Database
                                              ↓
                                         Frontend Display
```

## File Structure

```
app/
├── main.py                      # Backend API (refactored)
├── static/index.html            # Frontend (login removed)
├── app.db                       # SQLite database (auto-created)
├── requirements.txt             # Python dependencies
│
├── chrome-extension/            # NEW: Chrome extension
│   ├── manifest.json           # Extension config
│   ├── background.js           # Background worker
│   ├── content.js              # Page interceptor
│   ├── popup.html              # Settings UI
│   ├── popup.js                # Settings logic
│   ├── icons/                  # Extension icons
│   └── README.md               # Extension docs
│
├── API_CHANGES.md              # Detailed API documentation
├── QUICKSTART.md               # Quick reference guide
├── INSTALLATION_GUIDE.md       # This file
├── post_data_example.py        # Test script
├── integration_example.py      # Integration template
└── test_refactoring.py         # Verification script
```

## API Endpoints

### POST /api/console-data
**Receive data from extension or external sources**

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

### GET /api/console-data
**Retrieve stored data (used by frontend)**

```bash
curl http://localhost:8002/api/console-data
```

## Chrome Extension Features

- ✅ Automatic API interception
- ✅ Configurable backend URL
- ✅ Enable/disable toggle
- ✅ Connection testing
- ✅ Statistics tracking
- ✅ Visual feedback (badge notifications)
- ✅ Modern, beautiful UI

## Configuration

### Change Backend Port

Edit `main.py`:
```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)  # Change port here
```

Then update extension popup with new URL: `http://localhost:8003/api/console-data`

### Remote Backend

If hosting backend on a remote server:

1. Deploy backend to your server (see DEPLOYMENT.md)
2. Update extension popup with remote URL: `https://your-domain.com/api/console-data`
3. Ensure CORS is configured in backend

## Troubleshooting

### Backend Issues

**Port already in use:**
```bash
# Find process using port 8002
netstat -ano | findstr :8002

# Kill the process or change port in main.py
```

**Dependencies missing:**
```bash
pip install -r requirements.txt
```

**Database errors:**
```bash
# Delete and recreate database
del app.db
python main.py
```

### Extension Issues

**Not intercepting data:**
1. Check extension is enabled (toggle ON in popup)
2. Reload the v2.mnitnetwork.com page
3. Check browser console (F12) for errors
4. Verify you're on the correct website

**Connection failed:**
1. Verify backend is running
2. Test connection using popup button
3. Check backend URL is correct
4. Check firewall/antivirus settings

**Extension not loading:**
1. Verify all files are present
2. Check icons exist in icons/ folder
3. Reload extension in chrome://extensions/
4. Check for errors in extension details

### Frontend Issues

**No data showing:**
1. Backend running? Check `http://localhost:8002`
2. Data posted? Run `python post_data_example.py`
3. Check browser console for errors

**Auto-refresh not working:**
1. Check browser console for errors
2. Verify backend is responding
3. Try manual refresh (F5)

## Production Deployment

### Backend Deployment

Follow existing guides:
- **Render.com**: See `RENDER_DEPLOYMENT.md`
- **Namecheap**: See `DEPLOYMENT.md`

### Extension Distribution

**For personal use:**
- Keep in developer mode
- Load unpacked extension

**For team use:**
1. Zip the chrome-extension folder
2. Share with team members
3. Each person loads unpacked extension

**For public distribution:**
1. Create Chrome Web Store developer account
2. Package extension as .zip
3. Submit to Chrome Web Store
4. Follow Chrome's review process

## Security Notes

- Extension only intercepts v2.mnitnetwork.com
- No data sent to third parties
- All data stays between extension and your backend
- Use HTTPS for remote backends
- Consider adding authentication for production

## What's Preserved

All original features still work:
- ✅ List view with animations
- ✅ Grid view with cards  
- ✅ Accordion view (grouped by app)
- ✅ Color-coded app names
- ✅ Copy to clipboard
- ✅ Auto-refresh every 5 seconds
- ✅ Responsive design
- ✅ All animations and transitions

## What's Changed

- ❌ No more external API login
- ❌ No more token management
- ❌ No hardcoded credentials
- ✅ Local database storage
- ✅ API-based data ingestion
- ✅ Chrome extension for capture

## Next Steps

1. ✅ Backend refactored and tested
2. ✅ Chrome extension created
3. ✅ Git committed and pushed
4. 🔄 Test with real v2.mnitnetwork.com data
5. 🔄 Deploy to production (optional)
6. 🔄 Share extension with team (optional)

## Support

For detailed information, check:
- `API_CHANGES.md` - Complete API documentation
- `QUICKSTART.md` - Quick reference
- `chrome-extension/README.md` - Extension details
- `DEPLOYMENT.md` - Production deployment

## Success Checklist

- [ ] Backend starts without errors
- [ ] Can access http://localhost:8002
- [ ] Extension loads in Chrome
- [ ] Test connection succeeds
- [ ] Sample data displays correctly
- [ ] Extension intercepts real API calls
- [ ] Data appears in frontend automatically

If all checked, you're ready to go! 🎉
