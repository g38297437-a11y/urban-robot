/**
 * Content Script - Runs on every webpage
 * Listens for right-click on password fields and decrypts from clipboard
 */

// Listen for right-click on password fields
document.addEventListener('contextmenu', async (event) => {
    const target = event.target;
    
    // Check if right-clicked on password field, input field, or textarea
    const isPasswordField = target.type === 'password';
    const isInputField = target.tagName === 'INPUT' && (target.type === 'text' || target.type === '');
    const isTextarea = target.tagName === 'TEXTAREA';
    
    if (isPasswordField || isInputField || isTextarea) {
        // Prevent default context menu
        event.preventDefault();
        
        console.log('🔐 Right-click detected on', target.tagName, target.type);
        
        // Send message to background script to decrypt
        try {
            const response = await chrome.runtime.sendMessage({
                action: 'decryptFromClipboard'
            });
            
            if (response && response.success) {
                // Paste decrypted password into the field
                target.value = response.masked;
                target.style.color = '#667eea';
                target.style.fontWeight = 'bold';
                
                // Trigger input event to notify the website
                target.dispatchEvent(new Event('input', { bubbles: true }));
                target.dispatchEvent(new Event('change', { bubbles: true }));
                
                // Sanitize clipboard
                chrome.runtime.sendMessage({
                    action: 'sanitizeClipboard'
                }).catch(err => {
                    console.log('Sanitization sent to background');
                });
                
                // Show visual feedback
                showNotification(`✓ Password decrypted and pasted (${response.length} chars)`);
            } else {
                showNotification(`❌ ${response?.error || 'Decryption failed'}`, 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            showNotification('❌ Could not decrypt. Is the clipboard activated?', 'error');
        }
    }
});

/**
 * Show notification on the webpage
 */
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        background: ${type === 'error' ? '#ef4444' : '#10b981'};
        color: white;
        border-radius: 8px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
        z-index: 999999;
        font-family: Arial, sans-serif;
        font-size: 14px;
        font-weight: 600;
        animation: slideIn 0.3s ease-out;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

console.log('🔐 Password Manager Extension: Ready - Right-click on password fields to decrypt');
