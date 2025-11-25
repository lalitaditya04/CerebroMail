// ==================== STATE MANAGEMENT ====================

const state = {
    view: 'inbox', // 'inbox', 'prompts', 'tasks'
    inboxTab: 'mock', // 'mock' or 'gmail'
    emails: [],
    gmailEmails: [],
    selectedEmailId: null,
    prompts: {},
    isProcessing: false,
    loadingProgress: 0,
    connectedToGmail: false,
    lastAutoProcessed: 0,
    emailsAddedToTasks: new Set(), // Track which emails are added to task list
    currentUser: null, // Store current user info
    emailDrafts: {} // Store multiple drafts per email: { emailId: [{ id, content, timestamp, title }] }
};

// API base URL
const API_BASE = window.location.origin;

// ==================== HELPER FUNCTIONS ====================

function getCurrentEmails() {
    return state.inboxTab === 'gmail' ? state.gmailEmails : state.emails;
}

// Helper function to update email in current array
function updateCurrentEmail(emailId, updates) {
    if (state.inboxTab === 'gmail') {
        const index = state.gmailEmails.findIndex(e => e.id === emailId);
        if (index !== -1) {
            state.gmailEmails[index] = { ...state.gmailEmails[index], ...updates };
        }
    } else {
        const index = state.emails.findIndex(e => e.id === emailId);
        if (index !== -1) {
            state.emails[index] = { ...state.emails[index], ...updates };
        }
    }
}

function showNotification(message) {
    // Get or create notification container
    let container = document.getElementById('notification-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'notification-container';
        container.className = 'fixed top-4 right-4 z-50 flex flex-col gap-2';
        document.body.appendChild(container);
    }
    
    // Create notification element
    const notification = document.createElement('div');
    notification.className = 'bg-white border-2 border-blue-500 shadow-lg rounded-lg px-4 py-3 transition-all duration-300 ease-out opacity-0 transform translate-x-4';
    notification.innerHTML = `
        <div class="flex items-center gap-2">
            <span class="text-sm font-medium text-slate-800">${message}</span>
            <button onclick="this.parentElement.parentElement.remove()" class="text-slate-400 hover:text-slate-600 ml-2">✕</button>
        </div>
    `;
    
    // Add to container (new notifications at top)
    container.insertBefore(notification, container.firstChild);
    
    // Trigger animation after DOM insertion
    setTimeout(() => {
        notification.style.opacity = '1';
        notification.style.transform = 'translateX(0)';
    }, 10);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        notification.style.opacity = '0';
        notification.style.transform = 'translateX(4rem)';
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
                // Remove container if empty
                if (container.children.length === 0) {
                    container.remove();
                }
            }
        }, 300);
    }, 5000);
}

function updateEmail(updatedEmail) {
    // Try to update in mock emails
    let index = state.emails.findIndex(e => e.id === updatedEmail.id);
    if (index !== -1) {
        state.emails[index] = updatedEmail;
        render();
        return;
    }
    
    // Try to update in Gmail emails
    index = state.gmailEmails.findIndex(e => e.id === updatedEmail.id);
    if (index !== -1) {
        state.gmailEmails[index] = updatedEmail;
        render();
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { state, API_BASE, getCurrentEmails, updateCurrentEmail, showNotification, updateEmail };
}
