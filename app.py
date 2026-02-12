import random
import string
import gnupg
import os
import json
from flask import Flask, render_template, request, jsonify
import threading
import time

app = Flask(__name__)

# Initialize GPG with gnupg home
GPG_HOME = os.path.expanduser("~/.password_manager_web_gpg")
if not os.path.exists(GPG_HOME):
    os.makedirs(GPG_HOME, mode=0o700)

gpg = gnupg.GPG(gnupghome=GPG_HOME)

# In-memory storage for passwords
password_storage = {}


class PasswordManager:
    """Password manager operations"""
    
    @staticmethod
    def generate_random_password(length):
        """Generate random password with uppercase, lowercase, digits, and symbols"""
        characters = string.ascii_uppercase + string.ascii_lowercase + string.digits + "!@#"
        password = ''.join(random.choice(characters) for _ in range(length))
        return password
    
    @staticmethod
    def encrypt_password(password):
        """Encrypt password using GPG AES256"""
        encrypted_data = gpg.encrypt(
            password,
            recipients=None,
            symmetric='AES256',
            always_trust=True,
            passphrase='password_manager_default_key'
        )
        
        if not encrypted_data.ok:
            raise Exception(f"Encryption failed: {encrypted_data.status}")
        
        return str(encrypted_data)
    
    @staticmethod
    def decrypt_password(encrypted_str):
        """Decrypt password using GPG"""
        decrypted_data = gpg.decrypt(
            encrypted_str,
            always_trust=True,
            passphrase='password_manager_default_key'
        )
        
        if not decrypted_data.ok:
            raise Exception(f"Decryption failed: {decrypted_data.status}")
        
        return str(decrypted_data)
    
    @staticmethod
    def sanitize_clipboard_text():
        """Generate random 264-character strings for clipboard sanitization"""
        sanitized = []
        for _ in range(5):
            random_str = ''.join(
                random.choice(string.ascii_letters + string.digits + string.punctuation)
                for _ in range(264)
            )
            sanitized.append(random_str)
        return sanitized


@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')


@app.route('/api/generate-password', methods=['POST'])
def generate_password():
    """Generate a random password"""
    try:
        data = request.json
        length = int(data.get('length', 16))
        
        if length < 1:
            return jsonify({'error': 'Length must be at least 1'}), 400
        
        password = PasswordManager.generate_random_password(length)
        password_storage['current'] = password
        
        return jsonify({
            'success': True,
            'length': len(password),
            'masked': '*' * len(password)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/encrypt-password', methods=['POST'])
def encrypt_password():
    """Encrypt the current password"""
    try:
        if 'current' not in password_storage:
            return jsonify({'error': 'No password to encrypt. Generate one first.'}), 400
        
        password = password_storage['current']
        encrypted = PasswordManager.encrypt_password(password)
        password_storage['encrypted'] = encrypted
        
        # Return preview of encrypted password
        preview = encrypted[:50] + "..." if len(encrypted) > 50 else encrypted
        
        return jsonify({
            'success': True,
            'preview': preview,
            'length': len(encrypted)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/get-encrypted', methods=['GET'])
def get_encrypted():
    """Get the encrypted password for clipboard"""
    try:
        if 'encrypted' not in password_storage:
            return jsonify({'error': 'No encrypted password. Encrypt one first.'}), 400
        
        encrypted = password_storage['encrypted']
        return jsonify({
            'success': True,
            'data': encrypted
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/decrypt-from-clipboard', methods=['POST'])
def decrypt_from_clipboard():
    """Decrypt password from clipboard data"""
    try:
        data = request.json
        encrypted_str = data.get('data', '')
        
        if not encrypted_str:
            return jsonify({'error': 'No encrypted data provided'}), 400
        
        decrypted = PasswordManager.decrypt_password(encrypted_str)
        password_storage['current'] = decrypted
        
        return jsonify({
            'success': True,
            'length': len(decrypted),
            'masked': '*' * len(decrypted),
            'message': 'Password decrypted! Clipboard being sanitized...'
        })
    except Exception as e:
        return jsonify({'error': f'Decryption failed: {str(e)}'}), 500


@app.route('/api/sanitize-clipboard', methods=['POST'])
def sanitize_clipboard():
    """Generate sanitization strings"""
    try:
        sanitized = PasswordManager.sanitize_clipboard_text()
        return jsonify({
            'success': True,
            'sanitized_strings': sanitized,
            'message': 'Clipboard sanitized with 5 random 264-character strings'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/copy-to-clipboard', methods=['GET'])
def copy_to_clipboard():
    """Get encrypted password ready for clipboard copy"""
    try:
        if 'encrypted' not in password_storage:
            return jsonify({'error': 'No encrypted password. Encrypt one first.'}), 400
        
        encrypted = password_storage['encrypted']
        return jsonify({
            'success': True,
            'data': encrypted,
            'message': 'Encrypted password ready to copy. Use "Copy to Clipboard" button.'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/status', methods=['GET'])
def status():
    """Get current storage status"""
    return jsonify({
        'has_password': 'current' in password_storage,
        'has_encrypted': 'encrypted' in password_storage,
        'password_length': len(password_storage.get('current', ''))
    })


if __name__ == '__main__':
    print("\n" + "="*60)
    print("Password Manager Web Application")
    print("="*60)
    print("\nStarting Flask server...")
    print("Open your browser and navigate to: http://localhost:5000")
    print("\nFeatures:")
    print("✓ Generate random passwords")
    print("✓ Encrypt with GPG AES256")
    print("✓ Copy to clipboard")
    print("✓ Decrypt from clipboard")
    print("✓ Auto sanitize clipboard with 5 random strings")
    print("\n" + "="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
