// ==================== API CALLS ====================

async function fetchEmails() {
    const res = await fetch(`${API_BASE}/api/emails`);
    const data = await res.json();
    state.emails = data.emails;
    state.lastAutoProcessed = data.lastAutoProcessed;
    render();
}

async function loadMockInbox() {
    const res = await fetch(`${API_BASE}/api/emails/load-mock`, { method: 'POST' });
    const data = await res.json();
    state.emails = data.emails;
    state.selectedEmailId = null;
    state.connectedToGmail = false;
    render();
    
    // Auto-process first 5 emails on initial load
    setTimeout(async () => {
        showNotification('🤖 Auto-processing first 5 emails...');
        await processInbox(5);
    }, 500);
}

async function fetchPrompts() {
    const res = await fetch(`${API_BASE}/api/prompts`);
    state.prompts = await res.json();
}

async function savePrompts(prompts) {
    const res = await fetch(`${API_BASE}/api/prompts`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(prompts)
    });
    state.prompts = await res.json();
}

async function processInbox(count = 4) {
    const currentEmails = state.inboxTab === 'gmail' ? state.gmailEmails : state.emails;
    
    // Filter only unprocessed emails
    const unprocessedEmails = currentEmails.filter(e => e.category === 'Unprocessed');
    
    if (unprocessedEmails.length === 0) {
        showNotification('✅ All emails are already processed!');
        return;
    }

    // Take specified number of unprocessed emails
    const emailsToProcess = unprocessedEmails.slice(0, count);
    const processCount = emailsToProcess.length;

    state.isProcessing = true;
    state.loadingProgress = 0;
    render();

    try {
        let processed = 0;
        for (const email of emailsToProcess) {
            await processIndividualEmail(email.id);
            processed++;
            state.loadingProgress = Math.round((processed / processCount) * 100);
            render();
        }
        
        state.lastAutoProcessed = Date.now();
        showNotification(`✅ Processed ${processCount} email${processCount > 1 ? 's' : ''} successfully!`);
    } catch (error) {
        console.error('Processing failed:', error);
        showNotification('❌ Processing failed. Check console for details.');
    }

    state.isProcessing = false;
    render();
}

async function processIndividualEmail(emailId) {
    const currentEmails = state.inboxTab === 'gmail' ? state.gmailEmails : state.emails;
    const email = currentEmails.find(e => e.id === emailId);
    if (!email) return;
    
    // Show processing notification
    showNotification('🤖 AI is processing this email...');
    
    // Update UI to show processing
    email.category = 'Processing...';
    render();
    
    try {
        const res = await fetch(`${API_BASE}/api/process-new-email`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email })
        });
        const data = await res.json();
        
        if (data.success) {
            // Update email with processed data in the correct array
            if (state.inboxTab === 'gmail') {
                const emailIndex = state.gmailEmails.findIndex(e => e.id === emailId);
                if (emailIndex !== -1) {
                    state.gmailEmails[emailIndex] = data.email;
                }
            } else {
                const emailIndex = state.emails.findIndex(e => e.id === emailId);
                if (emailIndex !== -1) {
                    state.emails[emailIndex] = data.email;
                }
            }
            
            const category = data.email.category;
            const actionsCount = data.email.actionItems?.length || 0;
            showNotification(`✅ Email processed! Category: ${category}${actionsCount > 0 ? `, ${actionsCount} actions found` : ''}`);
            render();
        }
    } catch (error) {
        console.error('Processing failed:', error);
        email.category = 'Unprocessed';
        showNotification('❌ Failed to process email');
        render();
    }
}

async function generateSummary(email) {
    try {
        showNotification('✨ Generating summary...');
        
        const res = await fetch(`${API_BASE}/api/summarize`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email })
        });
        
        if (!res.ok) {
            throw new Error(`API error: ${res.status}`);
        }
        
        const data = await res.json();
        
        if (!data.summary) {
            throw new Error('No summary received from API');
        }
        
        // Update email in the correct state array
        updateCurrentEmail(email.id, { summary: data.summary });
        
        showNotification('✅ Summary generated!');
        render();
        return data.summary;
    } catch (error) {
        console.error('Summary generation error:', error);
        showNotification('❌ Failed to generate summary');
        return null;
    }
}

async function generateDraft(email, instruction = '') {
    const res = await fetch(`${API_BASE}/api/generate-draft`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, instruction })
    });
    const data = await res.json();
    
    // Update email in state
    updateCurrentEmail(email.id, { draftReply: data.draft });
    render();
    return data.draft;
}

async function extractActions(email) {
    const res = await fetch(`${API_BASE}/api/extract-actions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email })
    });
    const data = await res.json();
    
    updateCurrentEmail(email.id, { actionItems: data.actionItems });
    render();
    return data.actionItems;
}

async function chatWithEmail(email, history, message) {
    try {
        const res = await fetch(`${API_BASE}/api/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, history, message })
        });
        
        if (!res.ok) {
            throw new Error(`API error: ${res.status}`);
        }
        
        const data = await res.json();
        
        if (!data.response) {
            throw new Error('No response from AI');
        }
        
        return data.response;
    } catch (error) {
        console.error('Chat API error:', error);
        throw error;
    }
}

async function saveDraft(emailId, draft) {
    await fetch(`${API_BASE}/api/save-draft`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ emailId, draft })
    });
    
    updateCurrentEmail(emailId, { draftReply: draft });
}

async function runCustomAnalyzer(email, prompt) {
    const res = await fetch(`${API_BASE}/api/custom-analyzer`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, prompt })
    });
    const data = await res.json();
    return data.result;
}

// Gmail API calls
async function handleConnectGmail() {
    try {
        // Check if already authenticated
        const statusRes = await fetch(`${API_BASE}/api/gmail/auth/status`);
        const statusData = await statusRes.json();
        
        if (statusData.authenticated) {
            // Store user info
            state.currentUser = {
                email: statusData.email,
                name: statusData.name,
                picture: statusData.picture
            };
            state.connectedToGmail = true;
            // Already authenticated, fetch emails
            await fetchRealGmailEmails();
            return;
        }
        
        // Start OAuth flow
        const authRes = await fetch(`${API_BASE}/api/gmail/auth/start`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                redirect_uri: `${window.location.origin}/api/gmail/auth/callback`
            })
        });
        
        const authData = await authRes.json();
        
        if (!authData.success) {
            if (authData.error.includes('credentials.json')) {
                alert('Gmail OAuth Setup Required!\n\n' + 
                      'Please follow these steps:\n' +
                      '1. Go to https://console.cloud.google.com/apis/credentials\n' +
                      '2. Create OAuth 2.0 credentials\n' +
                      '3. Download credentials.json\n' +
                      '4. Place it in the project root directory\n' +
                      '5. Try connecting again');
            } else {
                alert('Authentication error: ' + authData.error);
            }
            return;
        }
        
        // Open OAuth popup
        showNotification('🔐 Opening Gmail authentication...');
        window.location.href = authData.auth_url;
        
    } catch (error) {
        console.error('Gmail connection error:', error);
        alert('Failed to connect to Gmail. Using demo mode instead.');
        // Fallback to mock data
        const res = await fetch(`${API_BASE}/api/emails/load-gmail`, { method: 'POST' });
        const data = await res.json();
        state.emails = data.emails;
        state.selectedEmailId = null;
        state.connectedToGmail = false;
        render();
    }
}

async function fetchRealGmailEmails() {
    try {
        showNotification('📧 Fetching emails from Gmail...');
        
        const res = await fetch(`${API_BASE}/api/gmail/emails/fetch`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                max_results: 20,
                query: ''  // Empty = all emails, or use 'is:unread' for unread only
            })
        });
        
        const data = await res.json();
        
        if (data.success) {
            state.gmailEmails = data.emails;
            state.selectedEmailId = null;
            state.connectedToGmail = true;
            state.inboxTab = 'gmail';
            
            // Update user info from response
            if (data.user) {
                state.currentUser = data.user;
            }
            
            showNotification(`✅ Loaded ${data.count} emails from Gmail!`);
            render();
        } else {
            throw new Error(data.error);
        }
        
    } catch (error) {
        console.error('Error fetching Gmail emails:', error);
        showNotification('❌ Failed to fetch Gmail emails');
    }
}

async function loadGmailInbox() {
    try {
        const res = await fetch(`${API_BASE}/gmail/emails`);
        if (res.status === 401) {
            state.connectedToGmail = false;
            render();
            return;
        }
        const data = await res.json();
        state.gmailEmails = data.emails || [];
        state.connectedToGmail = true;
        state.currentUser = data.user || null;
        render();
    } catch (error) {
        console.error('Error loading Gmail:', error);
        state.connectedToGmail = false;
    }
}

async function disconnectGmail() {
    if (!confirm('Disconnect from Gmail? You will need to reconnect to access Gmail emails.')) {
        return;
    }
    
    try {
        await fetch(`${API_BASE}/api/gmail/auth/logout`, { method: 'POST' });
        state.connectedToGmail = false;
        state.gmailEmails = [];
        state.inboxTab = 'mock';
        state.selectedEmailId = null;
        showNotification('👋 Disconnected from Gmail');
        render();
    } catch (error) {
        console.error('Logout error:', error);
        // Force disconnect even if request fails
        state.connectedToGmail = false;
        state.gmailEmails = [];
        state.inboxTab = 'mock';
        render();
    }
}

async function simulateNewEmail() {
    try {
        // Simulate new email arrival
        const res = await fetch(`${API_BASE}/api/emails/simulate-new`, {
            method: 'POST'
        });
        const data = await res.json();
        
        if (data.success) {
            // Show notification
            showNotification(`📧 New email from ${data.email.sender}!`);
            
            // Auto-process the new email after a short delay
            setTimeout(async () => {
                await autoProcessNewEmail(data.email);
            }, 1000);
        }
    } catch (error) {
        console.error('Failed to simulate email:', error);
        alert('Failed to simulate new email');
    }
}

async function autoProcessNewEmail(email) {
    try {
        // Show processing notification
        showNotification('🤖 AI is analyzing the new email...');
        
        const res = await fetch(`${API_BASE}/api/process-new-email`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email })
        });
        const data = await res.json();
        
        if (data.success) {
            // Update email in state
            const emailIndex = state.emails.findIndex(e => e.id === email.id);
            if (emailIndex !== -1) {
                state.emails[emailIndex] = data.email;
            } else {
                state.emails.unshift(data.email); // Add to beginning
            }
            
            // Show completion notification
            const category = data.email.category;
            const actionsCount = data.email.actionItems?.length || 0;
            showNotification(`✅ Email categorized as ${category}${actionsCount > 0 ? ` with ${actionsCount} actions` : ''}!`);
            
            render();
        }
    } catch (error) {
        console.error('Failed to process new email:', error);
        showNotification('❌ Failed to process email');
    }
}

async function checkGmailAuthStatus() {
    try {
        const res = await fetch(`${API_BASE}/api/gmail/auth/status`);
        const data = await res.json();
        
        if (data.authenticated) {
            console.log('✅ Gmail authenticated:', data.email);
            state.connectedToGmail = true;
            state.currentUser = {
                email: data.email,
                name: data.name,
                picture: data.picture
            };
            
            // Auto-load Gmail emails if on Gmail tab
            if (state.inboxTab === 'gmail') {
                await loadGmailInbox();
            }
        } else {
            console.log('ℹ️ Gmail not authenticated');
            state.connectedToGmail = false;
            state.currentUser = null;
        }
    } catch (error) {
        console.error('Error checking Gmail auth:', error);
        state.connectedToGmail = false;
    }
}

async function fetchModelConfig() {
    try {
        const res = await fetch(`${API_BASE}/api/model-config`);
        window.modelConfig = await res.json();
    } catch (error) {
        console.error('Failed to fetch model config:', error);
    }
}

async function handleModelChange(modelName) {
    try {
        showNotification('🔄 Switching AI model...');
        const res = await fetch(`${API_BASE}/api/model-config`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ model_name: modelName })
        });
        const data = await res.json();
        
        if (data.success) {
            window.modelConfig.current_model = modelName;
            showNotification(`✅ ${data.message}`);
            render();
        } else {
            showNotification(`❌ Failed to switch model: ${data.error}`);
        }
    } catch (error) {
        console.error('Failed to update model:', error);
        showNotification('❌ Failed to switch model');
    }
}
