# Console Data Interceptor - Chrome Extension

A Chrome extension that intercepts API calls from v2.mnitnetwork.com and forwards the console data to your local backend.

## Features

- 🔄 Automatically intercepts console API calls
- 📡 Forwards data to your backend in real-time
- ⚙️ Configurable backend URL
- 🎛️ Enable/disable toggle
- 📊 Statistics tracking
- 🧪 Connection testing
- ✨ Beautiful modern UI

## Installation

### Step 1: Generate Icons

1. Open `icons/create_icons.html` in your browser
2. Download all three icon files (icon16.png, icon48.png, icon128.png)
3. Save them in the `icons` folder

### Step 2: Load Extension in Chrome

1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode" (toggle in top-right corner)
3. Click "Load unpacked"
4. Select the `chrome-extension` folder
5. The extension should now appear in your extensions list

### Step 3: Configure Extension

1. Click the extension icon in Chrome toolbar
2. Enter your backend URL (default: `http://localhost:8002/api/console-data`)
3. Click "Save Settings"
4. Click "Test Connection" to verify it works

## Usage

### Automatic Mode (Recommended)

1. Make sure your backend is running:
   ```bash
   cd ..
   python main.py
   ```

2. Open the extension popup and ensure it's enabled (toggle should be ON)

3. Visit https://v2.mnitnetwork.com and log in

4. The extension will automatically intercept API calls and forward data to your backend

5. View the data at http://localhost:8002

### Manual Testing

Use the "Test Connection" button in the popup to send a test message to your backend.

## Configuration

### Backend URL

The extension needs to know where to send the intercepted data. You can configure this in the popup:

- **Local development**: `http://localhost:8002/api/console-data`
- **Remote server**: `https://your-domain.com/api/console-data`
- **Custom port**: `http://localhost:3000/api/console-data`

### Account Credentials (Helper)

The popup includes email and password fields pre-filled with the default credentials:
- **Email**: `Aktermamber.00.7@gmail.com`
- **Password**: `Bd55555$`

These are stored locally in the extension and serve as a reference. You can:
- Update them if your credentials change
- Use them as a reminder when logging into v2.mnitnetwork.com
- Access them anytime from the extension popup

**Note**: These credentials are only stored locally in your browser and are not sent anywhere except when you manually log into the website.

### Enable/Disable

Use the toggle switch in the popup to enable or disable the interceptor without uninstalling the extension.

## How It Works

1. **Content Script** (`content.js`): Injected into v2.mnitnetwork.com pages
   - Intercepts `fetch()` and `XMLHttpRequest` calls
   - Detects calls to `/dashboard/getconsole` endpoint
   - Captures the response data

2. **Background Script** (`background.js`): Runs in the background
   - Receives intercepted data from content script
   - Forwards data to your backend via POST request
   - Manages settings and statistics
   - Updates extension badge with status

3. **Popup** (`popup.html/js`): User interface
   - Configure backend URL
   - Enable/disable interceptor
   - Test connection
   - View statistics

## Troubleshooting

### Extension not intercepting data

1. **Check if extension is enabled**: Open popup and verify toggle is ON
2. **Reload the page**: Refresh v2.mnitnetwork.com after enabling extension
3. **Check console**: Open DevTools (F12) and look for interceptor messages
4. **Verify URL**: Make sure you're on v2.mnitnetwork.com

### Backend not receiving data

1. **Test connection**: Use "Test Connection" button in popup
2. **Check backend URL**: Verify the URL is correct and backend is running
3. **CORS issues**: Make sure your backend allows requests from the extension
4. **Check network**: Open DevTools → Network tab to see if POST requests are being made

### Extension not loading

1. **Check manifest**: Ensure manifest.json is valid
2. **Icons missing**: Generate icons using `icons/create_icons.html`
3. **Reload extension**: Go to chrome://extensions/ and click reload button
4. **Check errors**: Look for errors in chrome://extensions/ page

## Development

### File Structure

```
chrome-extension/
├── manifest.json          # Extension configuration
├── background.js          # Background service worker
├── content.js            # Content script (injected into pages)
├── popup.html            # Popup UI
├── popup.js              # Popup logic
├── icons/                # Extension icons
│   ├── icon16.png
│   ├── icon48.png
│   ├── icon128.png
│   └── create_icons.html # Icon generator
└── README.md             # This file
```

### Modifying the Extension

1. Make your changes to the files
2. Go to `chrome://extensions/`
3. Click the reload button on the extension card
4. Test your changes

### Debugging

- **Content script**: Open DevTools on v2.mnitnetwork.com page
- **Background script**: Click "service worker" link in chrome://extensions/
- **Popup**: Right-click extension icon → Inspect popup

## API Format

The extension forwards data in this format:

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
  "message": "Console data retrieved successfully"
}
```

## Security Notes

- The extension only intercepts data from v2.mnitnetwork.com
- Data is sent directly to your configured backend
- No data is stored or sent to third parties
- All communication happens over HTTP/HTTPS

## License

This extension is part of the Console App project.

## Support

For issues or questions, check the main project documentation in the parent directory.
