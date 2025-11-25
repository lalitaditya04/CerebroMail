// ==================== CHAT FUNCTIONALITY ====================

// Chat state management
if (!window.chatState) {
    window.chatState = {};
}

function updateChatInput(emailId, value) {
   if (!window.chatState[emailId]) return;
   window.chatState[emailId].input = value;
   
   // Update button state dynamically
   const sendBtn = document.getElementById(`send-btn-${emailId}`);
   if (sendBtn) {
      const canSend = value.trim().length > 0 && !window.chatState[emailId].isChatting;
      if (canSend) {
         sendBtn.className = 'flex-shrink-0 p-3 rounded-xl transition-all duration-200 bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white shadow-md hover:shadow-lg transform hover:scale-105 cursor-pointer';
         sendBtn.disabled = false;
      } else {
         sendBtn.className = 'flex-shrink-0 p-3 rounded-xl transition-all duration-200 bg-slate-200 text-slate-400 cursor-not-allowed';
         sendBtn.disabled = true;
      }
   }
}

function handleChatSendClick(emailId) {
   const chatData = window.chatState[emailId];
   if (!chatData) return;
   
   const canSend = chatData.input.trim().length > 0 && !chatData.isChatting;
   if (canSend) {
      handleChatSend(emailId);
   }
}

async function handleChatSend(emailId) {
const currentEmails = getCurrentEmails();
const email = currentEmails.find(e => e.id === emailId);
if (!email || !window.chatState[emailId]) {
console.error('Email or chat state not found:', emailId);
return;
}

const chatData = window.chatState[emailId];
const message = chatData.input.trim();
if (!message) return;

// Prevent multiple sends
if (chatData.isChatting) return;

// Add user message
chatData.messages.push({
role: 'user',
text: message,
timestamp: Date.now()
});
chatData.input = '';
chatData.isChatting = true;
render();

try {
// Get response
const history = chatData.messages.map(m => ({ role: m.role, text: m.text }));
const response = await chatWithEmail(email, history.slice(0, -1), message);

chatData.messages.push({
   role: 'model',
   text: response,
   timestamp: Date.now()
});

// Save chat history
await saveChatHistory(emailId, chatData.messages);
} catch (error) {
console.error('Chat error:', error);
chatData.messages.push({
   role: 'model',
   text: 'Sorry, I encountered an error processing your message. Please try again.',
   timestamp: Date.now()
});
showNotification('❌ Chat error: ' + error.message);
} finally {
chatData.isChatting = false;
render();

// Scroll to bottom
setTimeout(() => {
   const chatContainer = document.getElementById(`chat-messages-${emailId}`);
   if (chatContainer) {
         chatContainer.scrollTop = chatContainer.scrollHeight;
   }
}, 100);
}
}

async function handleQuickAction(emailId, action) {
if (!window.chatState[emailId]) return;
window.chatState[emailId].input = action;
await handleChatSend(emailId);
}

async function saveChatHistory(emailId, messages) {
try {
   console.log('💾 Saving chat history...');
   console.log('Email ID:', emailId);
   console.log('Messages count:', messages.length);
   console.log('User email:', state.currentUser?.email);
   console.log('Inbox tab:', state.inboxTab);
   
   const payload = {
      email_id: emailId,
      messages: messages,
      user_email: state.currentUser?.email || null
   };
   
   console.log('Payload:', JSON.stringify(payload, null, 2));
   
   const response = await fetch(`${API_BASE}/api/chat/save`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
   });
   
   console.log('Response status:', response.status);
   
   if (response.ok) {
      const data = await response.json();
      console.log('✅ Chat saved successfully:', data);
      
      // Trigger re-render to show saved badge
      render();
   } else {
      const errorText = await response.text();
      console.error('❌ Failed to save chat:', response.status, errorText);
      showNotification('⚠️ Chat not saved - check console');
   }
} catch (error) {
   console.error('❌ Error saving chat:', error);
   showNotification('❌ Failed to save chat history');
}
}

async function loadChatHistory(emailId) {
try {
   console.log('📖 Loading chat history...');
   console.log('Email ID:', emailId);
   
   const res = await fetch(`${API_BASE}/api/chat/load/${emailId}`, {
         method: 'GET',
         headers: { 'Content-Type': 'application/json' }
      });
      
      if (res.ok) {
         const data = await res.json();
         console.log('Loaded chat data:', data);
         
         if (data.messages && data.messages.length > 0) {
               if (!window.chatState) window.chatState = {};
               window.chatState[emailId] = {
                  messages: data.messages,
                  input: '',
                  isChatting: false
               };
               console.log('✅ Chat history loaded:', data.messages.length, 'messages');
         } else {
               console.log('No chat history found for this email');
         }
      }
   } catch (error) {
      console.error('❌ Error loading chat:', error);
   }
}

async function testChatSave(emailId) {
   console.log('🧪 Testing chat save manually...');
   const testMessages = [
      { role: 'model', text: 'Test greeting', timestamp: Date.now() },
      { role: 'user', text: 'Test user message', timestamp: Date.now() },
      { role: 'model', text: 'Test AI response', timestamp: Date.now() }
   ];
   
   await saveChatHistory(emailId, testMessages);
   
   // Try to load it back
   setTimeout(async () => {
      await loadChatHistory(emailId);
      alert('Check console for test results!');
   }, 1000);
}
