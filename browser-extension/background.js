/**
 * Background Service Worker
 * Handles decryption and clipboard operations
 */

const API_URL = 'http://localhost:5000';

// Listen for messages from content scripts
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'decryptFromClipboard') {
        handleDecryption(sendResponse);
    } else if (request.action === 'sanitizeClipboard') {
        handleSanitization();
    }
    
    // Return true to indicate async response
    return true;
});

/**
 * Handle decryption from clipboard
 */
async function handleDecryption(sendResponse) {
    try {
        // Read clipboard
        const clipboardText = await navigator.clipboard.readText();
        
        console.log('📋 Clipboard read, sending to server for decryption...');
        
        // Send to Flask backend
        const response = await fetch(`${API_URL}/api/decrypt-from-clipboard`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ data: clipboardText })
        });
        
        const result = await response.json();
        
        if (result.success) {
            console.log('✓ Decryption successful');
            sendResponse({
                success: true,
                masked: result.masked,
                length: result.length
            });
        } else {
            sendResponse({
                success: false,
                error: result.error || 'Decryption failed'
            });
        }
    } catch (error) {
        console.error('❌ Decryption error:', error);
        sendResponse({
            success: false,
            error: error.message
        });
    }
}

/**
 * Handle clipboard sanitization
 */
async function handleSanitization() {
    try {
        // Get sanitization strings from server
        const response = await fetch(`${API_URL}/api/sanitize-clipboard`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const result = await response.json();
        
        if (result.success) {
            // Write each sanitization string to clipboard sequentially
            const strings = result.sanitized_strings;
            
            for (let i = 0; i < strings.length; i++) {
                await navigator.clipboard.writeText(strings[i]);
                console.log(`✓ Clipboard sanitized (${i + 1}/5)`);
                
                // Small delay between writes
                if (i < strings.length - 1) {
                    await sleep(100);
                }
            }
            
            console.log('✓ Clipboard sanitization complete');
        }
    } catch (error) {
        console.debug('Sanitization background process completed');
    }
}

/**
 * Sleep utility
 */
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

console.log('🔐 Password Manager Background Service Worker loaded');
