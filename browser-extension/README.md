# 🔐 Password Manager Browser Extension

A Chrome/Edge browser extension that adds right-click decryption functionality to password fields across ANY website.

## Features

✅ **Right-Click on Password Fields** - Right-click on any password field to decrypt and paste
✅ **GPG Decryption** - Decrypts GPG-encrypted passwords from clipboard
✅ **Auto-Fill** - Automatically pastes decrypted password into the field
✅ **Clipboard Sanitization** - Replaces clipboard with 5 random 264-character strings
✅ **Works Anywhere** - Functions on any website with password fields
✅ **Smart Notifications** - Shows success/error messages on the webpage

## Installation Instructions

### For Chrome/Edge (Chromium-based browsers)

1. **Ensure Flask Server is Running**
   ```bash
   cd /workspaces/urban-robot
   python3 app.py
   ```
   The server must be running on http://localhost:5000

2. **Install Extension in Chrome/Edge**
   - Open Chrome and go to: `chrome://extensions/`
   - Or Edge: `edge://extensions/`
   - Enable **"Developer mode"** (toggle in top-right corner)
   - Click **"Load unpacked"**
   - Navigate to `/workspaces/urban-robot/browser-extension/` and select it
   - The extension should now appear in your extensions list

3. **Pin the Extension** (Optional)
   - Click the puzzle icon in the toolbar
   - Find "Password Manager - GPG Decryption"
   - Click the pin icon to keep it visible

## How to Use

### Step 1: Generate Password in Web App
1. Go to http://localhost:5000 in a tab
2. Click "Generate Password" and choose length
3. Click "Encrypt"
4. Click "Copy to Clipboard"

### Step 2: Use on Any Website
1. Open another tab with any website (Gmail, GitHub, etc.)
2. Click on the password login field
3. **Right-click** on the password field
4. The encrypted password automatically:
   - ✅ Decrypts
   - ✅ Pastes into the field (shown as asterisks)
   - ✅ Sanitizes clipboard with 5 random strings

### Example Workflow

```
Tab 1: localhost:5000 (Password Manager)
├─ Generate random password
├─ Encrypt it
└─ Copy to clipboard ← GPG-encrypted password

Tab 2: account.google.com (Gmail login)
├─ Right-click password field
└─ ✓ Decrypted password pasted! ✓ Clipboard sanitized!
```

## What Gets Decrypted

The extension detects and works with:
- ✅ `<input type="password">`
- ✅ `<input type="text">` (when used for passwords)
- ✅ `<textarea>` fields

## Security Features

🔒 **AES256 Encryption** - All passwords encrypted with GPG
🔒 **Masked Display** - Passwords shown as asterisks (*)
🔒 **Clipboard Sanitization** - Automatic cleanup with random data (5 times)
🔒 **No Data Storage** - Nothing saved to disk
🔒 **localhost Only** - Works only on local Flask server (http://localhost:5000)

## Troubleshooting

**Extension doesn't show in toolbar:**
- Go to chrome://extensions/
- Check if "Developer mode" is enabled
- Click "Load unpacked" and select the browser-extension folder

**Right-click doesn't work:**
- Make sure you're right-clicking directly on the password field
- Ensure the Flask server is running on localhost:5000
- Check the browser console for errors (F12 → Console tab)

**"Could not decrypt" error:**
- Verify the clipboard contains a valid GPG-encrypted password
- Make sure it was encrypted using the same passphrase
- Check Flask server logs for errors

**Server connection failed:**
- Ensure Flask app is running: `python3 app.py` in `/workspaces/urban-robot/`
- Check that you can access http://localhost:5000 in your browser
- Verify no firewall is blocking localhost:5000

## File Structure

```
browser-extension/
├── manifest.json      # Extension configuration
├── content.js        # Runs on every webpage (detects right-clicks)
├── background.js     # Handles decryption & clipboard ops
├── popup.html        # Toolbar popup UI
├── popup.js          # Popup functionality
└── README.md         # This file
```

## Technical Details

- **Manifest V3** - Modern Chrome extension format
- **Content Scripts** - Inject into all webpages
- **Background Service Worker** - Handles crypto operations
- **Clipboard API** - Direct clipboard read/write
- **Flask Backend** - Provides GPG encryption/decryption

## API Endpoints Used

The extension communicates with these Flask endpoints:
- `POST /api/decrypt-from-clipboard` - Decrypt GPG-encrypted password
- `POST /api/sanitize-clipboard` - Generate sanitization strings
- `GET /api/status` - Check server status

## Keyboard Shortcuts

Currently **none** - All functionality available via right-click menu.

Future enhancement: Could add keyboard shortcut to trigger clipboard paste.

## Permissions Explained

- `clipboard-read` - Read encrypted password from clipboard
- `clipboard-write` - Write sanitization strings to clipboard
- `scripting` - Inject content script on webpages
- `activeTab` - Interact with current tab
- `<all_urls>` - Work on any website

## Known Limitations

⚠️ Some websites with Content Security Policy (CSP) may block clipboard operations
⚠️ Password masking uses input field value - some sites may override this
⚠️ Only works with plain text/password input fields, not password managers' custom inputs

## Updates & Support

To update the extension:
1. Modify files in `/workspaces/urban-robot/browser-extension/`
2. Go to chrome://extensions/
3. Click the refresh icon on the Password Manager extension

---

**Created:** February 2026
**Version:** 1.0
**Compatibility:** Chrome 88+, Edge 88+, Brave, Opera

🔐 **Security Note:** This extension only works with the local Flask server. Never expose your password decryption to untrusted servers!
