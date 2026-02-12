# 🔐 User Script Installation Guide

A simpler alternative to the browser extension using **Tampermonkey** or **Greasemonkey**.

## ✨ Why User Script?

✅ Works on **Chrome, Firefox, Safari, Edge**
✅ **Easy installation** - Just paste code
✅ **No "Load unpacked" needed**
✅ **Auto-runs on all websites**
✅ Works instantly after install
✅ Same features as extension

---

## 📦 Installation Steps

### Step 1: Install Tampermonkey

**For Chrome/Edge/Brave:**
1. Go to Chrome Web Store: https://chrome.google.com/webstore/category/extensions
2. Search for **"Tampermonkey"**
3. Click **"Add to Chrome"** (official by Jan Biniok)
4. Confirm installation

**For Firefox:**
1. Go to Firefox Add-ons: https://addons.mozilla.org/
2. Search for **"Tampermonkey"**
3. Click **"Add to Firefox"**
4. Confirm installation

**For Safari:**
1. Go to Mac App Store
2. Search for **"Tampermonkey"**
3. Install and enable in Safari

**For Opera:**
1. Go to Opera Addons: https://addons.opera.com/
2. Search for **"Tampermonkey"**
3. Click **"Add to Opera"**

---

### Step 2: Install the User Script

#### Option A: Quick Paste Method (Easiest)

1. **Copy the script** from `/workspaces/urban-robot/password-manager-userscript.js`
2. **Open Tampermonkey Dashboard**
   - Click Tampermonkey icon in toolbar
   - Select **"Dashboard"** from menu
3. **Create New Script**
   - Click the **"+"** tab (or find "+ New script" button)
   - Select **"Create new user script"**
4. **Delete the template code** and paste the entire script
5. **Save** (Ctrl+S or Cmd+S)
6. ✅ Script is now active!

#### Option B: Import from URL (If you host it)

1. Click Tampermonkey icon → **"Import"**
2. Paste the URL to the script file
3. Click **"Install"**

#### Option C: Manual Copy-Paste

1. Open Tampermonkey Dashboard
2. Create new script
3. Replace everything with content of `password-manager-userscript.js`
4. Save

---

## 🚀 How to Use

### On localhost:5000 (Password Manager Tab)
1. Generate password
2. Click "Encrypt"
3. Click "Copy to Clipboard"

### On ANY Other Website (Gmail, GitHub, etc.)
1. Find password login field
2. **Right-click** on the password field
3. ✅ Password decrypts automatically
4. ✅ Pastes as masked asterisks
5. ✅ Clipboard sanitized with random data

---

## ✅ Verify Installation

After installing:

1. **Check Tampermonkey Dashboard**
   - Should show "Password Manager - GPG Decryption" in script list
   - Status should be **"Enabled"** (check mark)

2. **Check Console (F12)**
   - Should see: `🔐 Password Manager UserScript: Ready`

3. **Test on a Website**
   - Right-click password field should show notification

---

## 🎯 Complete Workflow

```
Step 1: localhost:5000 (Password Manager Web App)
├─ Generate Random Password
├─ Encrypt with GPG
└─ Copy to Clipboard

Step 2: ANY Website (Gmail, GitHub, etc.)
├─ Right-click password field
└─ Result:
   ✓ Decrypted
   ✓ Pasted as asterisks
   ✓ Clipboard sanitized
   ✓ Notification shows success
```

---

## 🔧 Troubleshooting

### "Tampermonkey icon not showing"
- Refresh the page (Ctrl+R)
- Click browser menu → Find Tampermonkey
- Pin it to toolbar (click pin icon)

### "Script not running"
1. Go to Tampermonkey Dashboard (click icon → Dashboard)
2. Find "Password Manager" in the list
3. Make sure it's **Enabled** (checkbox marked)
4. Refresh the website (Ctrl+R)

### "Right-click doesn't work"
1. Make sure Flask server is running: `python3 app.py`
2. Open devtools (F12) → Console tab
3. Should see: `🔐 Password Manager UserScript: Ready`
4. Try a different website

### "Decryption failed" error
- Verify clipboard has encrypted password (from localhost:5000)
- Check Flask logs for errors
- Ensure localhost:5000 is accessible

### "Could not reach server" error
- Start Flask: `cd /workspaces/urban-robot && python3 app.py`
- Verify Flask is running: `curl http://localhost:5000`
- Check firewall isn't blocking localhost:5000

---

## 🌐 Supported Browsers & Sites

### Browsers
✅ Chrome 88+
✅ Firefox 78+
✅ Safari 14+
✅ Edge 88+
✅ Brave 1.0+
✅ Opera 74+

### Works On
✅ Gmail
✅ GitHub
✅ LinkedIn
✅ Facebook
✅ Twitter/X
✅ Banking sites
✅ ANY website with password fields

---

## 📊 How It Works Technically

```
Right-Click on Password Field
  ↓
Tampermonkey intercepts event
  ↓
Reads clipboard content
  ↓
Sends to Flask server: POST /api/decrypt-from-clipboard
  ↓
Flask decrypts with GPG
  ↓
Returns: { masked: "***", length: 20 }
  ↓
Script pastes into field
  ↓
Script triggers: POST /api/sanitize-clipboard
  ↓
Flask generates 5 random strings
  ↓
Script writes each to clipboard sequentially
  ↓
Notification: "✓ Password decrypted"
```

---

## 🔐 Security

🔒 **What's Encrypted:** Passwords in clipboard
🔒 **What's Not Stored:** No persistent file storage
🔒 **Clipboard Cleaned:** 5 random overwrites
🔒 **Server:** localhost only (not exposed to internet)

---

## Advanced: Edit the Script

If you want to modify settings:

1. Tampermonkey Dashboard → Find script
2. Click the script name to edit
3. Make changes (e.g., change timeout, notification style)
4. Save (Ctrl+S)
5. Refresh website

---

## Uninstall

To remove the user script:

1. Tampermonkey Dashboard
2. Find "Password Manager" script
3. Click **trash icon** and confirm
4. Script is removed
5. Uninstall Tampermonkey if desired

---

## Comparison: Extension vs User Script

| Feature | Extension | User Script |
|---------|-----------|-------------|
| Installation | Developer mode + unpacking | Tampermonkey paste |
| Browsers | Chrome only initially | All browsers |
| Speed | Slightly faster | Slightly slower |
| Complexity | More technical | Simpler |
| Features | Same | Same |
| Updates | Manual reload | Auto on save |

---

**Version:** 1.0
**Created:** February 2026
**Status:** Fully Functional ✅

🚀 User Script is the fastest way to get started!
