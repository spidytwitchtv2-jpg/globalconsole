# Extension Popup Preview

## Updated Popup Interface

The extension popup now includes credential management for easy reference.

```
┌─────────────────────────────────────────────┐
│  🔄 Console Interceptor                     │
├─────────────────────────────────────────────┤
│                                             │
│  Interceptor Status          [●─────] ON   │
│                                             │
│  Backend URL                                │
│  ┌─────────────────────────────────────┐   │
│  │ http://localhost:8002/api/console-  │   │
│  │ data                                │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  ┌───────────────────────────────────────┐ │
│  │ 📧 Account Credentials (Helper)      │ │
│  │                                       │ │
│  │  Email                                │ │
│  │  ┌─────────────────────────────────┐ │ │
│  │  │ Aktermamber.00.7@gmail.com      │ │ │
│  │  └─────────────────────────────────┘ │ │
│  │                                       │ │
│  │  Password                             │ │
│  │  ┌─────────────────────────────────┐ │ │
│  │  │ ••••••••                        │ │ │
│  │  └─────────────────────────────────┘ │ │
│  │                                       │ │
│  │  💡 These credentials are stored      │ │
│  │     locally and used as reference.    │ │
│  │     You can update them anytime.      │ │
│  └───────────────────────────────────────┘ │
│                                             │
│  ┌──────────────┐  ┌──────────────────┐   │
│  │ Save Settings│  │ Test Connection  │   │
│  └──────────────┘  └──────────────────┘   │
│                                             │
│  ✓ Settings saved successfully!            │
│                                             │
│  ┌───────────────────────────────────────┐ │
│  │ How it works:                         │ │
│  │ 1. Visit v2.mnitnetwork.com          │ │
│  │ 2. Extension intercepts API calls    │ │
│  │ 3. Data is forwarded to your backend │ │
│  │ 4. View data at your backend URL     │ │
│  └───────────────────────────────────────┘ │
│                                             │
│       0              0                      │
│   Intercepted    Forwarded                  │
│                                             │
└─────────────────────────────────────────────┘
```

## Features

### 1. Interceptor Toggle
- **ON**: Extension actively intercepts API calls
- **OFF**: Extension is disabled but remains installed

### 2. Backend URL Configuration
- Default: `http://localhost:8002/api/console-data`
- Can be changed to any URL (local or remote)
- Validated on save

### 3. Account Credentials Section (NEW)
- **Email field**: Pre-filled with default email
- **Password field**: Pre-filled with default password (masked)
- **Helper text**: Explains the purpose
- **Local storage**: Credentials stored only in browser
- **Editable**: Users can update credentials anytime

### 4. Action Buttons
- **Save Settings**: Saves all configuration
- **Test Connection**: Sends test data to backend

### 5. Status Message
- Shows success/error messages
- Auto-hides after 3 seconds
- Color-coded (green for success, red for error)

### 6. Statistics
- **Intercepted**: Total API calls intercepted
- **Forwarded**: Successfully forwarded to backend

## Use Cases for Credentials

### 1. Quick Reference
When logging into v2.mnitnetwork.com, users can:
- Click extension icon
- View saved credentials
- Copy/paste into login form

### 2. Credential Management
If credentials change:
- Update in extension popup
- Click "Save Settings"
- New credentials stored locally

### 3. Team Sharing
When sharing extension with team:
- Each member can set their own credentials
- No need to remember or search for login info
- Credentials stay private (local storage only)

## Security Notes

- Credentials stored in `chrome.storage.sync`
- Only accessible by the extension
- Not sent to any server automatically
- Users manually enter credentials on website
- Extension only stores for reference

## Data Flow

```
User opens popup
      ↓
Views saved credentials
      ↓
Manually logs into v2.mnitnetwork.com
      ↓
Extension intercepts API calls
      ↓
Data forwarded to backend
```

## Storage Structure

```javascript
chrome.storage.sync = {
  backendUrl: "http://localhost:8002/api/console-data",
  email: "Aktermamber.00.7@gmail.com",
  password: "Bd55555$",
  isEnabled: true,
  stats: {
    intercepted: 0,
    forwarded: 0
  }
}
```

## Popup Dimensions

- **Width**: 380px (increased from 350px)
- **Max Height**: 600px
- **Scrollable**: Yes (if content exceeds height)
- **Responsive**: Adapts to content

## Visual Design

- **Background**: Purple gradient (667eea → 764ba2)
- **Cards**: Frosted glass effect with backdrop blur
- **Inputs**: White background with focus effects
- **Buttons**: Green primary, translucent secondary
- **Text**: White with varying opacity for hierarchy
- **Icons**: Emoji for visual appeal

## Accessibility

- Clear labels for all inputs
- Placeholder text for guidance
- Helper text for context
- Color contrast meets WCAG standards
- Keyboard navigation supported
