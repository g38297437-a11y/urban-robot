/**
 * Popup Script
 * Handles the extension popup UI
 */

const API_URL = 'http://localhost:5000';

// Check server status on load
document.addEventListener('DOMContentLoaded', () => {
    checkServerStatus();
});

/**
 * Open the Password Manager web app
 */
function openPasswordManager() {
    chrome.tabs.create({ url: API_URL });
}

/**
 * Check server status
 */
async function checkStatus() {
    const statusBox = document.getElementById('statusBox');
    statusBox.style.display = 'block';
    statusBox.className = 'status';
    statusBox.textContent = '⏳ Checking...';
    
    try {
        const response = await fetch(`${API_URL}/api/status`);
        if (response.ok) {
            const data = await response.json();
            statusBox.className = 'status success';
            statusBox.innerHTML = `
                ✓ <strong>Server Connected</strong><br>
                Password stored: ${data.has_password ? 'Yes' : 'No'}<br>
                Encrypted: ${data.has_encrypted ? 'Yes' : 'No'}
            `;
        } else {
            throw new Error('Server not responding');
        }
    } catch (error) {
        statusBox.className = 'status error';
        statusBox.textContent = `❌ Server Error: ${error.message}`;
    }
}

/**
 * Check server status on load
 */
async function checkServerStatus() {
    const serverStatus = document.getElementById('serverStatus');
    
    try {
        const response = await fetch(`${API_URL}/api/status`, {
            method: 'GET'
        });
        
        if (response.ok) {
            serverStatus.style.color = '#10b981';
            serverStatus.textContent = '✓ Connected (localhost:5000)';
        } else {
            serverStatus.style.color = '#ef4444';
            serverStatus.textContent = '✗ Server not responding';
        }
    } catch (error) {
        serverStatus.style.color = '#ef4444';
        serverStatus.textContent = `✗ Cannot reach localhost:5000`;
    }
}
