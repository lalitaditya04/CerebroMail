// ==================== DRAFT MANAGEMENT ====================

function updateDraftInstruction(value) {
    if (!window.emailDetailState) window.emailDetailState = {};
    window.emailDetailState.draftInstruction = value;
}

function createNewDraft(emailId) {
    if (!state.emailDrafts[emailId]) {
        state.emailDrafts[emailId] = [];
    }
    
    const newDraft = {
        id: Date.now().toString(),
        title: `Draft ${state.emailDrafts[emailId].length + 1}`,
        content: '',
        timestamp: Date.now()
    };
    
    state.emailDrafts[emailId].unshift(newDraft);
    
    if (!window.emailDetailState) window.emailDetailState = {};
    window.emailDetailState.activeDraftId = newDraft.id;
    
    showNotification('📝 New draft created');
    render();
    
    // Focus on title input
    setTimeout(() => {
        const titleInput = document.getElementById(`draft-title-${emailId}`);
        if (titleInput) titleInput.select();
    }, 100);
}

function selectDraft(emailId, draftId) {
    if (!window.emailDetailState) window.emailDetailState = {};
    window.emailDetailState.activeDraftId = draftId;
    render();
}

function updateDraftTitle(emailId, draftId, title) {
    if (!state.emailDrafts[emailId]) return;
    
    const draft = state.emailDrafts[emailId].find(d => d.id === draftId);
    if (draft) {
        draft.title = title || 'Untitled Draft';
        saveDraftsToStorage(emailId);
    }
}

let autoSaveTimeout = null;
function autoSaveDraft(emailId, draftId, content) {
    if (!state.emailDrafts[emailId] || !draftId) return;
    
    const draft = state.emailDrafts[emailId].find(d => d.id === draftId);
    if (!draft) return;
    
    draft.content = content;
    draft.timestamp = Date.now();
    
    // Debounce save to avoid excessive saves
    clearTimeout(autoSaveTimeout);
    autoSaveTimeout = setTimeout(() => {
        saveDraftsToStorage(emailId);
    }, 500);
}

function deleteDraft(emailId, draftId) {
    if (!confirm('Delete this draft? This action cannot be undone.')) return;
    
    if (!state.emailDrafts[emailId]) return;
    
    state.emailDrafts[emailId] = state.emailDrafts[emailId].filter(d => d.id !== draftId);
    
    // Select first draft if available
    if (state.emailDrafts[emailId].length > 0) {
        if (!window.emailDetailState) window.emailDetailState = {};
        window.emailDetailState.activeDraftId = state.emailDrafts[emailId][0].id;
    } else {
        if (window.emailDetailState) {
            window.emailDetailState.activeDraftId = null;
        }
    }
    
    saveDraftsToStorage(emailId);
    showNotification('🗑️ Draft deleted');
    render();
}

async function generateDraftWithAI(emailId) {
    const currentEmails = getCurrentEmails();
    const email = currentEmails.find(e => e.id === emailId);
    if (!email) return;
    
    const instruction = window.emailDetailState?.draftInstruction || '';
    
    try {
        showNotification('✨ AI is generating draft...');
        const draftContent = await generateDraft(email, instruction);
        
        // Create new draft with AI content
        if (!state.emailDrafts[emailId]) {
            state.emailDrafts[emailId] = [];
        }
        
        const aiDraft = {
            id: Date.now().toString(),
            title: `AI Draft ${state.emailDrafts[emailId].length + 1}`,
            content: draftContent,
            timestamp: Date.now()
        };
        
        state.emailDrafts[emailId].unshift(aiDraft);
        
        if (!window.emailDetailState) window.emailDetailState = {};
        window.emailDetailState.activeDraftId = aiDraft.id;
        
        saveDraftsToStorage(emailId);
        showNotification('✅ AI draft generated!');
        render();
    } catch (error) {
        console.error('Draft generation failed:', error);
        showNotification('❌ Failed to generate draft');
    }
}

function saveDraftsToStorage(emailId) {
    try {
        localStorage.setItem(`drafts_${emailId}`, JSON.stringify(state.emailDrafts[emailId]));
    } catch (error) {
        console.error('Failed to save drafts:', error);
    }
}

function loadDraftsFromStorage(emailId) {
    try {
        const saved = localStorage.getItem(`drafts_${emailId}`);
        if (saved) {
            state.emailDrafts[emailId] = JSON.parse(saved);
        }
    } catch (error) {
        console.error('Failed to load drafts:', error);
    }
}

function saveDraftContent(emailId, draft) {
    saveDraft(emailId, draft);
}
