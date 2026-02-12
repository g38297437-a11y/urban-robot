# Password Manager with GPG Encryption

A Python-based password manager GUI that provides secure password generation, GPG encryption, and clipboard management with right-click decryption.

## Features

✅ **Random Password Generation** - Generate passwords with:
   - Capital letters (A-Z)
   - Lowercase letters (a-z)
   - Numbers (0-9)
   - Symbols (!@#)
   - User-specified length

✅ **Password Masking** - Passwords display as asterisks (*) for security

✅ **GPG Encryption** - Encrypt passwords using AES256 symmetric encryption

✅ **Clipboard Management** - Copy encrypted passwords to clipboard

✅ **Right-Click Decryption** - Right-click on a password field to:
   - Decrypt the GPG key from clipboard
   - Paste the original password (masked as stars)
   - Automatically sanitize clipboard with 5 random 264-character strings

## Requirements

- Python 3.6+
- tkinter (usually comes with Python)
- pyperclip
- python-gnupg
- GPG command-line tool

## Installation

1. Clone or navigate to this directory
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure GPG is installed:
   ```bash
   # On Ubuntu/Debian
   sudo apt-get install gnupg
   
   # On macOS
   brew install gnupg
   ```

## Usage

Run the application:
```bash
python3 password_manager.py
```

### Step-by-step workflow:

1. **Generate Password**: 
   - Click "Create Random" button
   - Enter desired password length
   - Password appears as stars in the field

2. **Encrypt Password**:
   - Click "Encrypt" button
   - Password is encrypted with GPG AES256

3. **Copy to Clipboard**:
   - Click "Clipboard" button
   - Encrypted password is copied to clipboard

4. **Decrypt and Paste**:
   - Right-click on any password field
   - Decrypted password appears as stars
   - Clipboard is sanitized with 5 random 264-character strings

## Security Notes

- The application uses AES256 symmetric encryption
- Passwords are masked (displayed as asterisks) when shown
- Clipboard is automatically sanitized after decryption
- A dedicated GPG home directory is created at `~/.password_manager_gpg/`
- The application uses a fixed passphrase for simplicity (can be customized in production)

## Important

This is a demonstration password manager. For production use:
- Use environment variables for passphrases
- Implement proper key management
- Add database persistence
- Enable password recovery mechanisms
- Consider additional security measures

## Troubleshooting

**"Decryption failed" error**: 
- Ensure the clipboard contains a properly encrypted password
- Make sure GPG is properly installed

**GUI doesn't appear**: 
- Ensure you have X11 or Wayland display environment
- On headless systems, use SSH X forwarding or VNC

**Clipboard operations fail**: 
- Install xclip (Linux): `sudo apt-get install xclip`
- On macOS and Windows, pyperclip should work automatically
