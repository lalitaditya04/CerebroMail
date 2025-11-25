// ==================== MAIN APPLICATION ====================
// Initialization and OAuth callback handling

async function init() {
    // Test if chat routes are accessible
    try {
        const testRes = await fetch(`${API_BASE}/api/chat/test`);
        const testData = await testRes.json();
        console.log('🧪 Chat routes test:', testData);
    } catch (error) {
        console.error('❌ Chat routes not accessible:', error);
    }
    
    // Check Gmail authentication status on startup
    await checkGmailAuthStatus();
    
    await fetchPrompts();
    await fetchModelConfig();
    await loadMockInbox();
    render();
}

// Check for OAuth callback on page load
window.addEventListener('load', async () => {
    const urlParams = new URLSearchParams(window.location.search);
    const gmailAuth = urlParams.get('gmail_auth');
    
    if (gmailAuth === 'success') {
        showNotification('✅ Gmail connected successfully!');
        // Clean URL
        window.history.replaceState({}, document.title, '/');
        // Fetch emails
        await fetchRealGmailEmails();
    } else if (gmailAuth === 'failed' || gmailAuth === 'error') {
        showNotification('❌ Gmail authentication failed');
        window.history.replaceState({}, document.title, '/');
    }
});

// Start the application when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
