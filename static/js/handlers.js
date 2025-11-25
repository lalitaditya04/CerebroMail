// ==================== UI INTERACTION HANDLERS ====================

function changeView(view) {
    state.view = view;
    render();
}

function switchInboxTab(tab) {
    state.inboxTab = tab;
    state.selectedEmailId = null;
    render();
}

function selectEmail(id) {
    state.selectedEmailId = id;
    window.emailDetailState = { activeTab: 'content' };
    
    // Load drafts from storage for this email
    loadDraftsFromStorage(id);
    
    // Load chat history from storage
    loadChatHistory(id);
    
    render();
    
    // Scroll to top of email list
    setTimeout(() => {
        const emailListContainer = document.querySelector('.flex-1.overflow-y-auto');
        if (emailListContainer) {
            emailListContainer.scrollTop = 0;
        }
    }, 0);
}

function changeEmailTab(emailId, tab) {
    if (!window.emailDetailState) window.emailDetailState = {};
    window.emailDetailState.activeTab = tab;
    render();
}

async function handleGenerateSummary(emailId) {
    const currentEmails = getCurrentEmails();
    const email = currentEmails.find(e => e.id === emailId);
    if (!email) return;
    
    await generateSummary(email);
}

async function handleExtractActions(emailId) {
    const currentEmails = getCurrentEmails();
    const email = currentEmails.find(e => e.id === emailId);
    if (!email) return;
    
    // Show loading state
    const originalActions = email.actionItems;
    email.actionItems = [{ task: 'Extracting actions...', isCompleted: false }];
    render();
    
    try {
        const res = await fetch(`${API_BASE}/api/extract-actions`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email })
        });
        const data = await res.json();
        
        // Update email in state
        updateCurrentEmail(emailId, { actionItems: data.actionItems });
    } catch (error) {
        console.error('Action extraction failed:', error);
        email.actionItems = originalActions;
        alert('Failed to extract actions. Please try again.');
    }
    
    render();
}

function updatePromptField(field, value) {
    if (!window.tempPrompts) window.tempPrompts = {};
    window.tempPrompts[field] = value;
}

function addAnalyzer() {
    if (!window.tempPrompts.customAnalyzers) {
        window.tempPrompts.customAnalyzers = [];
    }
    window.tempPrompts.customAnalyzers.push({
        id: Date.now().toString(),
        name: 'New Analyzer',
        prompt: 'Analyze the email for...'
    });
    render();
}

function removeAnalyzer(id) {
    if (!window.tempPrompts.customAnalyzers) return;
    window.tempPrompts.customAnalyzers = window.tempPrompts.customAnalyzers.filter(a => a.id !== id);
    render();
}

function updateAnalyzer(id, field, value) {
    if (!window.tempPrompts.customAnalyzers) return;
    const analyzer = window.tempPrompts.customAnalyzers.find(a => a.id === id);
    if (analyzer) {
        analyzer[field] = value;
    }
}

async function savePromptsConfig() {
    await savePrompts(window.tempPrompts);
    state.prompts = window.tempPrompts;
    changeView('inbox');
}

function attachEventListeners() {
    // Any additional event listeners can be attached here
}
