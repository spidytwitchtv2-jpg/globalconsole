# Chrome Extension Changelog

## Version 1.1.0 - Credential Management Update

### Added
- **Email field** in popup for credential reference
  - Pre-filled with: `Aktermamber.00.7@gmail.com`
  - Editable by user
  - Validated on save
  
- **Password field** in popup for credential reference
  - Pre-filled with: `Bd55555$`
  - Masked input for security
  - Editable by user
  
- **Credentials section** with visual styling
  - Frosted glass card design
  - Section header with emoji icon
  - Helper text explaining purpose
  - Integrated into popup layout

- **Credential storage** in chrome.storage.sync
  - Persists across browser sessions
  - Syncs across devices (if Chrome sync enabled)
  - Accessible from background script

- **Email validation** on save
  - Checks for @ symbol
  - Shows error message if invalid

### Changed
- **Popup width** increased from 350px to 380px
  - Better accommodates credential fields
  - Improved visual balance
  
- **Popup scrolling** enhanced
  - Max height: 600px
  - Custom scrollbar styling
  - Smooth scroll behavior

- **Background script** updated
  - Stores email and password
  - Provides GET_CREDENTIALS message handler
  - Logs credential updates (password masked)

### Documentation
- Updated README.md with credential management section
- Created POPUP_PREVIEW.md with visual interface guide
- Added security notes about credential storage

## Version 1.0.0 - Initial Release

### Features
- Network request interception for v2.mnitnetwork.com
- Automatic data forwarding to backend API
- Configurable backend URL
- Enable/disable toggle
- Connection testing
- Statistics tracking (intercepted/forwarded)
- Visual feedback with badge notifications
- Modern gradient UI design

### Components
- **manifest.json**: Extension configuration
- **background.js**: Service worker for data forwarding
- **content.js**: Page script for API interception
- **popup.html**: User interface
- **popup.js**: Popup logic and settings management
- **icons/**: Extension icons (16px, 48px, 128px)

### Documentation
- README.md: Complete usage guide
- FLOW_DIAGRAM.md: Visual architecture diagram
- Icon generator scripts (HTML and Python)

---

## Upgrade Guide

### From 1.0.0 to 1.1.0

No action required! The extension will automatically:
1. Load default credentials on first open
2. Store them in chrome.storage.sync
3. Display them in the popup

If you want to update credentials:
1. Click extension icon
2. Edit email/password fields
3. Click "Save Settings"

### Storage Migration

The extension automatically handles storage:
- Existing settings (backendUrl, isEnabled) preserved
- New fields (email, password) added with defaults
- No data loss or conflicts

---

## Future Enhancements

### Planned Features
- [ ] Show/hide password toggle
- [ ] Copy credentials to clipboard
- [ ] Multiple account profiles
- [ ] Auto-fill credentials on login page
- [ ] Credential import/export
- [ ] Encrypted credential storage
- [ ] Session management
- [ ] Activity log viewer

### Under Consideration
- [ ] Dark/light theme toggle
- [ ] Custom color schemes
- [ ] Notification preferences
- [ ] Advanced filtering options
- [ ] Data export functionality
- [ ] Backup/restore settings

---

## Bug Fixes

### Version 1.1.0
- None (new feature release)

### Version 1.0.0
- Initial stable release

---

## Breaking Changes

### Version 1.1.0
- None (backward compatible)

### Version 1.0.0
- Initial release (no previous versions)

---

## Security Updates

### Version 1.1.0
- Credentials stored in chrome.storage.sync (encrypted by Chrome)
- Password field uses type="password" for masking
- Email validation prevents invalid formats
- No credentials sent to external servers

### Version 1.0.0
- HTTPS enforcement for remote backends
- Content Security Policy in manifest
- Limited host permissions
- No external dependencies

---

## Performance Improvements

### Version 1.1.0
- Optimized popup rendering with scrollbar
- Efficient storage access patterns
- Minimal memory footprint increase

### Version 1.0.0
- Lightweight service worker
- Efficient message passing
- Minimal CPU usage
- Fast API interception

---

## Known Issues

### Version 1.1.0
- None reported

### Version 1.0.0
- None reported

---

## Support

For issues, questions, or feature requests:
1. Check the README.md documentation
2. Review POPUP_PREVIEW.md for UI guidance
3. Consult FLOW_DIAGRAM.md for architecture
4. Check parent directory documentation

---

## Credits

Developed as part of the Console App project.

## License

Part of the Console App project license.
