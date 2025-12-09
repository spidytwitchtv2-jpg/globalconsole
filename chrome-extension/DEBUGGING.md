# Extension Debugging Guide

## How to Debug the Extension

### Step 1: Check Extension is Loaded

1. Go to `chrome://extensions/`
2. Find "Console Data Interceptor"
3. Verify it's enabled (toggle should be ON)
4. Note the extension ID

### Step 2: Open the Target Website

1. Navigate to: `https://v2.mnitnetwork.com/dashboard/console`
2. Open DevTools (F12)
3. Go to Console tab

### Step 3: Look for Interceptor Logs

You should see colored logs like:

```
[Interceptor] Content script loaded
[Interceptor] URL: https://v2.mnitnetwork.com/dashboard/console
[Interceptor] Target API: https://v2.mnitnetwork.com/api/v1/mnitnetworkcom/dashboard/getconsole
[Interceptor] ✓ Fetch and XHR interceptors installed
[Interceptor] ✓ Page loaded, interceptors ready
[Interceptor] ✓ Performance observer installed
```

### Step 4: Monitor API Calls

When the page makes the getconsole API call, you should see:

```
[Interceptor] Fetch call: https://v2.mnitnetwork.com/api/v1/mnitnetworkcom/dashboard/getconsole
[Interceptor] ✓ MATCHED getconsole API!
[Interceptor] ✓ Data intercepted: {meta: {...}, data: {...}}
[Interceptor] ✓ Forwarded to backend: {success: true, result: {...}}
```

### Step 5: Check Background Script

1. Go to `chrome://extensions/`
2. Find "Console Data Interceptor"
3. Click "service worker" link
4. Check console for logs:

```
✓ Received API_RESPONSE from content script
✓ Intercepted API response: {...}
✓ Forwarding to backend: https://globalconsole-sthc.onrender.com/api/console-data
→ Sending POST to: https://globalconsole-sthc.onrender.com/api/console-data
← Backend response status: 200
✓ Backend success response: {status: "success", ...}
✓ Successfully forwarded to backend
```

### Step 6: Check Network Tab

1. In DevTools, go to Network tab
2. Filter by "getconsole"
3. You should see the API call
4. Check if it returns data

## Troubleshooting

### Issue: No Interceptor Logs

**Possible causes:**
- Extension not loaded
- Content script not injected
- Wrong page URL

**Solutions:**
1. Reload extension: `chrome://extensions/` → Click reload button
2. Hard refresh page: Ctrl+Shift+R
3. Check URL matches: `https://v2.mnitnetwork.com/*`
4. Check manifest.json content_scripts matches

### Issue: Logs Show But No "MATCHED" Message

**Possible causes:**
- API call uses different URL
- API call happens before script loads
- API call is in iframe

**Solutions:**
1. Check actual API URL in Network tab
2. Reload page after extension loads
3. Check if page uses iframes (manifest has `all_frames: true`)

### Issue: "MATCHED" But No "Forwarded to Backend"

**Possible causes:**
- Background script error
- CORS issue
- Backend not responding

**Solutions:**
1. Check background script console (service worker)
2. Look for error messages
3. Test backend manually:
   ```bash
   curl -X POST https://globalconsole-sthc.onrender.com/api/console-data \
     -H "Content-Type: application/json" \
     -d '{"meta":{},"data":{"messages":[]}}'
   ```

### Issue: Backend Returns Error

**Possible causes:**
- Backend down
- CORS not configured
- Invalid payload format

**Solutions:**
1. Check backend is running: `https://globalconsole-sthc.onrender.com/`
2. Check CORS settings in main.py
3. Verify payload format matches expected structure

## Manual Testing

### Test 1: Check Content Script Injection

```javascript
// Run in console on v2.mnitnetwork.com page
console.log('Original fetch:', window.fetch.toString().includes('Interceptor'));
// Should return: true
```

### Test 2: Trigger Manual API Call

```javascript
// Run in console on v2.mnitnetwork.com page
fetch('https://v2.mnitnetwork.com/api/v1/mnitnetworkcom/dashboard/getconsole', {
  headers: {
    'mhitauth': 'YOUR_TOKEN_HERE'
  }
}).then(r => r.json()).then(console.log);
```

### Test 3: Check Background Script

```javascript
// Run in background script console (service worker)
chrome.storage.sync.get(['isEnabled'], (result) => {
  console.log('Interceptor enabled:', result.isEnabled);
});
```

### Test 4: Send Test Message

```javascript
// Run in content script console
chrome.runtime.sendMessage({
  type: 'API_RESPONSE',
  data: {
    meta: { status: 'success' },
    data: { messages: [{ app_name: 'Test', carrier: '123', sms: 'Test', time: 'now' }] }
  }
}, (response) => {
  console.log('Response:', response);
});
```

## Common Issues

### 1. Extension Not Intercepting

**Symptoms:**
- No logs in console
- API calls work but not intercepted

**Fix:**
1. Reload extension
2. Hard refresh page
3. Check extension is enabled
4. Check URL matches pattern

### 2. CORS Error

**Symptoms:**
- "CORS policy" error in console
- Backend returns 403 or 401

**Fix:**
1. Check backend CORS settings
2. Verify backend URL is correct
3. Check host_permissions in manifest.json

### 3. Service Worker Inactive

**Symptoms:**
- Background script not running
- No logs in service worker console

**Fix:**
1. Click "service worker" link to wake it up
2. Reload extension
3. Check for errors in service worker console

### 4. Data Not Appearing in Backend

**Symptoms:**
- Extension logs show success
- But data not in backend UI

**Fix:**
1. Check backend logs
2. Verify database is updating
3. Check frontend is fetching data
4. Hard refresh backend UI

## Performance Monitoring

The extension includes a PerformanceObserver that monitors all network requests:

```javascript
// Check performance entries
performance.getEntriesByType('resource')
  .filter(e => e.name.includes('getconsole'))
  .forEach(e => console.log(e));
```

## Log Color Guide

- 🟢 Green (`#4CAF50`): Success messages
- 🔴 Red (`#f44336`): Error messages
- 🔵 Blue (`#2196F3`): Info messages
- ⚪ Gray (`#9E9E9E`): Debug messages
- 🟠 Orange (`#FF9800`): Warning/monitoring messages

## Extension States

### State 1: Loaded
```
[Interceptor] Content script loaded
[Interceptor] ✓ Fetch and XHR interceptors installed
```

### State 2: Ready
```
[Interceptor] ✓ Page loaded, interceptors ready
[Interceptor] ✓ Performance observer installed
```

### State 3: Monitoring
```
[Interceptor] Fetch call: https://...
[Interceptor] XHR send: https://...
```

### State 4: Intercepted
```
[Interceptor] ✓ MATCHED getconsole API!
[Interceptor] ✓ Data intercepted: {...}
```

### State 5: Forwarded
```
[Interceptor] ✓ Forwarded to backend: {success: true}
```

## Backend Verification

### Check Backend is Running

```bash
curl https://globalconsole-sthc.onrender.com/
```

Should return:
```json
{
  "message": "Console App API",
  "status": "running",
  "endpoints": {...}
}
```

### Check Backend Receives Data

```bash
curl -X POST https://globalconsole-sthc.onrender.com/api/console-data \
  -H "Content-Type: application/json" \
  -d '{
    "meta": {"status": "success"},
    "data": {
      "messages": [{
        "app_name": "Test",
        "carrier": "123456XXX",
        "sms": "Test message",
        "time": "just now"
      }]
    }
  }'
```

Should return:
```json
{
  "status": "success",
  "message": "Data stored successfully",
  "count": 1
}
```

### Check Data in UI

1. Open: `https://globalconsole-sthc.onrender.com/`
2. Should see test message
3. Check console for any errors

## Support

If issues persist:

1. Export extension logs:
   - Right-click in console → Save as...
   
2. Export background script logs:
   - Open service worker console
   - Right-click → Save as...

3. Check backend logs:
   - Go to Render.com dashboard
   - View logs for deployment

4. Create issue with:
   - Extension logs
   - Background script logs
   - Backend logs
   - Steps to reproduce
