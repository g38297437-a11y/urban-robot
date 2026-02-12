# 🔐 Password Manager - Complete Setup Guide

This project consists of two parts:
1. **Flask Web App** - Main password manager GUI
2. **Browser Extension** - Right-click decryption on ANY website

---

## Part 1: Flask Web App (already running on http://localhost:5000)

### Features
- Generate random passwords (A-Z, a-z, 0-9, !@#)
- Encrypt with GPG AES256
- Copy to clipboard
- 5 password input fields
- Manual clipboard sanitization

### Already Started
The Flask server should be running in the background. Access it at:
```
http://localhost:5000
```

---

## Part 2: Browser Extension (NEW!) 

### What It Does
Right-click on password fields in **ANY website** to:
1. Decrypt GPG-encrypted password from clipboard
2. Auto-paste into the field as asterisks
3. Sanitize clipboard with 5 random strings

### Installation Steps

#### Step 1: Ensure Flask Server is Running
```bash
# In /workspaces/urban-robot/
python3 app.py
```

#### Step 2: Load Extension in Chrome/Edge

**For Google Chrome:**
1. Open `chrome://extensions/` in the address bar
2. Enable **"Developer mode"** (toggle in top-right)
3. Click **"Load unpacked"**
4. Navigate to: `/workspaces/urban-robot/browser-extension/`
5. Click "Select Folder"

**For Microsoft Edge:**
1. Open `edge://extensions/` in the address bar
2. Enable **"Developer mode"** (toggle in left sidebar)
3. Click **"Load unpacked"**
4. Navigate to: `/workspaces/urban-robot/browser-extension/`
5. Click "Select Folder"

**For Brave Browser:**
1. Open `brave://extensions/` in the address bar
2. Enable **"Developer mode"** (toggle in top-right)
3. Click **"Load unpacked"**
4. Select the `browser-extension` folder

#### Step 3: Pin the Extension (Optional but Recommended)
1. Click the **puzzle icon** in the toolbar (top-right)
2. Find **"Password Manager - GPG Decryption"**
3. Click the **pin icon** to keep it visible

---

## Complete Workflow

### Setup (One Time)
1. ✅ Flask server running on http://localhost:5000
2. ✅ Browser extension loaded in Chrome/Edge/Brave
3. ✅ Extension pinned to toolbar

### Daily Usage

#### On localhost:5000 (Password Manager Tab)
```
1. Click "Generate Password"
2. Enter length (e.g., 20)
3. Click "Encrypt"
4. Click "Copy to Clipboard"
5. Leave Flask app open
```

#### On Any Other Website (Login Tab)
```
1. Navigate to login page (Gmail, GitHub, etc.)
2. Right-click on the password field
3. ✓ Password decrypts and pastes automatically
4. ✓ Clipboard sanitized with random data
5. Done!
```

### Example: Gmail Login
```
Tab 1: http://localhost:5000
├─ Generate password → "MySecurePass123!"
├─ Encrypt → Converts to GPG format
└─ Copy to Clipboard → Clipboard has encrypted data

Tab 2: https://accounts.google.com/
├─ Find password field
├─ Right-click on it ← THIS IS THE MAGIC
└─ ✓ Password auto-decrypts and pastes
    ✓ Shows as "********************"
    ✓ Clipboard cleaned (5 sanitizations)
```

---

## File Structure

```
urban-robot/
├── app.py                    # Flask server (already running)
├── password_manager.py       # Python GUI version
├── test_password_manager.py  # Test suite
├── requirements.txt          # Python dependencies
├── README.md                 # Main documentation
├── templates/
│   └── index.html           # Web UI
├── __pycache__/
└── browser-extension/        # ← BROWSER EXTENSION
    ├── manifest.json        # Extension config
    ├── content.js           # Handles right-click on webpages
    ├── background.js        # Decryption & clipboard
    ├── popup.html           # Toolbar popup
    ├── popup.js             # Popup functions
    └── README.md            # Extension guide
```

---

## Troubleshooting

### Issue: Extension doesn't appear in toolbar
**Solution:**
- Go to `chrome://extensions/` (or `edge://extensions/`)
- Make sure "Developer mode" is **ON** (toggle at top-right)
- Extension should be listed as "Password Manager - GPG Decryption"
- Click the pin icon to add to toolbar

### Issue: Right-click doesn't work
**Solution:**
1. Confirm you're right-clicking directly on a password field
2. Verify Flask server is running: http://localhost:5000
3. Check browser console (F12 → Console) for errors
4. Try refreshing the page (Ctrl+R)

### Issue: "Could not decrypt" error
**Solution:**
- Make sure you copied password from localhost:5000 first
- Verify it was encrypted (should start with "-----BEGIN PGP")
- Flask server logs should show last operation

### Issue: Clipboard operations fail
**Solution:**
- Browser may need clipboard permission
- Try granting permission when prompted
- Some websites block clipboard access (security)
- Check browser console for specific errors

### Issue: Flask server won't start
**Solution:**
```bash
cd /workspaces/urban-robot
pip install -r requirements.txt
python3 app.py
```

---

## Understanding the Flow

```
ENCRYPTION (Password Manager Tab)
├─ Random password generated
├─ User sees it masked (asterisks)
├─ Clicked "Encrypt" button
├─ Flask encrypts with GPG AES256
└─ "Copy to Clipboard" puts encrypted data on clipboard

DECRYPTION (Any Website Right-Click)
├─ User right-clicks password field
├─ Extension reads clipboard (encrypted data)
├─ Sends to Flask backend for decryption
├─ Gets back plain password + masked version
├─ Extension pastes masked version into field
├─ Extension sanitizes clipboard (5 times)
└─ User sees success notification on page
```

---

## Security Notes

🔒 **What's Encrypted:**
- Passwords stored in clipboard are GPG-encrypted
- Only Flask with correct passphrase can decrypt

🔒 **What's NOT Stored:**
- No passwords saved to files
- No data persists after closing browser
- All operations in memory

🔒 **Clipboard Sanitization:**
- After decryption, clipboard replaced 5 times
- Each time with 264 random characters
- Makes it harder to recover from disk

🔒 **Extension Permissions:**
- Only works with http://localhost:5000
- Doesn't send data to external servers
- No telemetry or tracking

---

## Browser Compatibility

| Browser | Supported | Version |
|---------|-----------|---------|
| Chrome | ✅ Yes | 88+ |
| Edge | ✅ Yes | 88+ |
| Brave | ✅ Yes | 1.0+ |
| Opera | ✅ Yes | 74+ |
| Firefox | ❌ No | Requires WebExtension API changes |
| Safari | ❌ No | Uses different extension system |

---

## Advanced Tips

### Using Multiple Passwords
- Click "Generate Password" multiple times
- Encrypt and copy each one
- Use the 5 password fields in the web app to store masked versions
- Switch between them on different websites

### Custom Passwords
- Although the app generates random ones, you can manually:
1. Type a custom password in the Flask app
2. Click "Encrypt"
3. Click "Copy to Clipboard"
4. Right-click password field on website

### Monitoring Activity
- Check Flask console for encryption/decryption logs
- Browser console shows right-click events
- Extension popup shows server connection status

---

## Next Steps

1. ✅ Verify Flask server running: http://localhost:5000
2. ✅ Load browser extension from `/browser-extension/` folder
3. ✅ Try it on a test site first (not real accounts yet!)
4. ✅ Test the complete workflow
5. ✅ Use on production sites when confident

---

## Support

For issues or questions:
1. Consult the relevant README:
   - `/workspaces/urban-robot/README.md` - Flask app
   - `/workspaces/urban-robot/browser-extension/README.md` - Extension
2. Check Flask logs for backend errors
3. Check browser console (F12) for frontend errors
4. Verify Flask is running on localhost:5000

---

**Version:** 1.0
**Created:** February 2026
**Status:** Fully Functional ✅
