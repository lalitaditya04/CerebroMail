// ==================== RENDERING FUNCTIONS ====================

function render() {
   const app = document.getElementById('app');
   app.innerHTML = `
      ${renderSidebar()}
      ${state.view === 'prompts' ? renderPromptManager() : 
         state.view === 'tasks' ? renderToDoList() : 
         renderInbox()}
   `;
   attachEventListeners();
}

function renderSidebar() {
   return `
      <div class="w-20 bg-slate-900 flex flex-col items-center py-6 gap-6 text-slate-400 z-20">
         <button onclick="changeView('inbox')" 
               class="p-3 rounded-xl transition-all ${state.view === 'inbox' ? 'bg-blue-600 text-white shadow-lg' : 'hover:bg-slate-800 hover:text-white'}"
               title="Inbox">
               <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
               </svg>
         </button>
         <button onclick="changeView('tasks')" 
               class="p-3 rounded-xl transition-all ${state.view === 'tasks' ? 'bg-blue-600 text-white shadow-lg' : 'hover:bg-slate-800 hover:text-white'}"
               title="To-Do List">
               <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
               </svg>
         </button>
         <div class="w-8 h-0.5 bg-slate-800 rounded-full my-2"></div>
         <button onclick="changeView('prompts')" 
               class="p-3 rounded-xl transition-all ${state.view === 'prompts' ? 'bg-blue-600 text-white shadow-lg' : 'hover:bg-slate-800 hover:text-white'}"
               title="Agent Brain">
               <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
               </svg>
         </button>
      </div>
   `;
}

function renderInbox() {
   const currentEmails = state.inboxTab === 'gmail' ? state.gmailEmails : state.emails;
   const selectedEmail = currentEmails.find(e => e.id === state.selectedEmailId);
   
   return `
      <div class="flex flex-1 overflow-hidden">
         <!-- Email List Column -->
         <div class="w-96 flex flex-col border-r border-slate-200 bg-white">
               ${renderInboxHeader()}
               <div class="flex-1 overflow-y-auto">
                  ${renderEmailList()}
               </div>
         </div>

         <!-- Detail Column -->
         <div class="flex-1 bg-slate-50 relative">
               ${selectedEmail ? renderEmailDetail(selectedEmail) : renderEmptyState()}
         </div>
      </div>
   `;
}

function renderInboxHeader() {
   const currentEmails = state.inboxTab === 'gmail' ? state.gmailEmails : state.emails;
   
   return `
      <div class="p-4 border-b border-slate-200 bg-slate-50">
         <div class="flex justify-between items-center mb-3">
               <h2 class="text-lg font-bold text-slate-800">Inbox</h2>
         </div>
         
         <!-- Tabs for Mock / Gmail -->
         <div class="flex gap-2 mb-3">
               <button onclick="switchInboxTab('mock')" 
                  class="flex-1 py-2 px-3 rounded-lg text-sm font-medium transition-all ${
                     state.inboxTab === 'mock' 
                     ? 'bg-blue-600 text-white shadow-sm' 
                     : 'bg-white text-slate-600 hover:bg-slate-100 border border-slate-200'
                  }">
                  📧 Mock Inbox
               </button>
               <button onclick="switchInboxTab('gmail')" 
                  class="flex-1 py-2 px-3 rounded-lg text-sm font-medium transition-all ${
                     state.inboxTab === 'gmail' 
                     ? 'bg-green-600 text-white shadow-sm' 
                     : 'bg-white text-slate-600 hover:bg-slate-100 border border-slate-200'
                  }">
                  <svg class="w-3 h-3 inline-block mr-1" viewBox="0 0 24 24" fill="currentColor">
                     <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                     <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                     <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                     <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                  </svg>
                  Gmail ${state.connectedToGmail ? `(${state.gmailEmails.length})` : ''}
               </button>
         </div>
         
         <!-- Action Buttons based on active tab -->
         <div class="flex flex-col gap-2 mb-2">
               ${state.inboxTab === 'mock' ? `
                  <button onclick="loadMockInbox()"
                     class="text-xs font-medium text-slate-600 hover:text-blue-600 bg-white border border-slate-200 px-3 py-2 rounded-lg shadow-sm transition-colors">
                     Reset with Mock Data
                  </button>
                  
                  <button onclick="simulateNewEmail()"
                     class="text-xs font-medium text-white bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 px-3 py-2 rounded-lg shadow-sm transition-all flex items-center justify-center gap-2">
                     <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                           <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                     </svg>
                     Simulate New Email
                  </button>
               ` : `
                  ${!state.connectedToGmail ? `
                     <button onclick="handleConnectGmail()"
                           class="text-xs font-medium text-white bg-gradient-to-r from-green-600 to-blue-600 hover:from-green-700 hover:to-blue-700 px-4 py-2.5 rounded-lg shadow-sm transition-all flex items-center justify-center gap-2">
                           <svg class="w-4 h-4" viewBox="0 0 24 24" fill="currentColor">
                              <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                              <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                              <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                              <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                           </svg>
                           Connect to Gmail
                     </button>
                  ` : `
                     <button onclick="fetchRealGmailEmails()"
                           class="text-xs font-medium text-white bg-gradient-to-r from-green-600 to-blue-600 hover:from-green-700 hover:to-blue-700 px-3 py-2 rounded-lg shadow-sm transition-all flex items-center justify-center gap-2">
                           <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
                           </svg>
                           Refresh Gmail
                     </button>
                     <button onclick="disconnectGmail()"
                           class="text-xs font-medium text-red-600 hover:text-red-700 bg-red-50 border border-red-200 px-3 py-2 rounded-lg shadow-sm transition-colors">
                           Disconnect Gmail
                     </button>
                  `}
               `}
         </div>

         <button onclick="processInbox()" ${state.isProcessing || currentEmails.length === 0 ? 'disabled' : ''}
               class="w-full py-2 rounded-lg text-sm font-medium flex items-center justify-center gap-2 transition-all shadow-sm mt-2 ${
                  state.isProcessing 
                  ? 'bg-slate-200 text-slate-500 cursor-wait' 
                  : 'bg-blue-600 text-white hover:bg-blue-700'
               }">
               ${state.isProcessing ? `Processing ${state.loadingProgress}%...` : 'Process Emails '}
         </button>
         ${state.lastAutoProcessed > 0 ? `
               <p class="text-[10px] text-center text-slate-400 mt-2">
                  Last processed: ${new Date(state.lastAutoProcessed).toLocaleTimeString()}
               </p>
         ` : ''}
      </div>
   `;
}

function renderEmailList() {
   const currentEmails = state.inboxTab === 'gmail' ? state.gmailEmails : state.emails;
   
   if (currentEmails.length === 0) {
      return `
         <div class="flex flex-col items-center justify-center p-8 text-center text-slate-400">
               <svg class="w-16 h-16 mb-4 opacity-20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
               </svg>
               ${state.inboxTab === 'gmail' 
                  ? '<p class="text-sm font-medium">No Gmail emails loaded</p><p class="text-xs mt-1">Click "Connect to Gmail" to load your emails</p>' 
                  : '<p class="text-sm font-medium">No emails loaded</p><p class="text-xs mt-1">Click "Reset with Mock Data" to load sample emails</p>'}
         </div>
      `;
   }

   return currentEmails.map(email => {
      const categoryColors = {
         'Important': 'bg-red-50 text-red-700 border-red-200',
         'Newsletter': 'bg-blue-50 text-blue-700 border-blue-200',
         'Spam': 'bg-gray-50 text-gray-700 border-gray-200',
         'To-Do': 'bg-amber-50 text-amber-700 border-amber-200',
         'Project': 'bg-purple-50 text-purple-700 border-purple-200',
         'Unprocessed': 'bg-slate-50 text-slate-600 border-slate-200'
      };

      const isSelected = state.selectedEmailId === email.id;
      const categoryColor = categoryColors[email.category] || categoryColors['Unprocessed'];
      
      // Truncate body for preview
      const bodyPreview = email.body.length > 120 ? email.body.substring(0, 120) + '...' : email.body;
      
      return `
         <div onclick="selectEmail('${email.id}')" 
               class="relative border-b border-slate-100 cursor-pointer transition-all hover:bg-slate-50 ${
                  isSelected ? 'bg-blue-50' : 'bg-white'
               }">
               ${isSelected ? '<div class="absolute left-0 top-0 bottom-0 w-1 bg-blue-600"></div>' : ''}
               
               <div class="p-4 ${isSelected ? 'pl-5' : ''}">
                  <!-- Header Row -->
                  <div class="flex items-start justify-between gap-3 mb-2">
                     <div class="flex items-center gap-2 min-w-0 flex-1">
                           <div class="w-8 h-8 rounded-full ${state.inboxTab === 'gmail' ? 'bg-gradient-to-br from-green-500 to-blue-500' : 'bg-gradient-to-br from-blue-500 to-purple-500'} flex items-center justify-center text-white font-bold text-xs flex-shrink-0">
                              ${email.sender.charAt(0).toUpperCase()}
                           </div>
                           <div class="min-w-0 flex-1">
                              <p class="text-sm font-semibold ${isSelected ? 'text-blue-900' : 'text-slate-800'} truncate">
                                 ${email.sender}
                              </p>
                              <p class="text-xs text-slate-500">
                                 ${new Date(email.timestamp).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
                              </p>
                           </div>
                     </div>
                  </div>
                  
                  <!-- Subject -->
                  <h4 class="text-sm font-semibold text-slate-900 mb-1.5 truncate">
                     ${email.subject}
                  </h4>
                  
                  <!-- Body Preview -->
                  <p class="text-xs text-slate-600 mb-3 line-clamp-2">
                     ${bodyPreview}
                  </p>
                  
                  <!-- Tags Row -->
                  <div class="flex items-center gap-2 flex-wrap">
                     <span class="inline-flex items-center text-[11px] font-medium px-2.5 py-0.5 rounded-full border ${categoryColor}">
                           ${email.category}
                     </span>
                     ${email.actionItems && email.actionItems.length > 0 ? `
                           <span class="inline-flex items-center text-[11px] font-medium px-2.5 py-0.5 rounded-full bg-green-50 text-green-700 border border-green-200">
                              <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                 <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
                              </svg>
                              ${email.actionItems.length}
                           </span>
                     ` : ''}
                     ${email.draftReply ? `
                           <span class="inline-flex items-center text-[11px] font-medium px-2.5 py-0.5 rounded-full bg-purple-50 text-purple-700 border border-purple-200">
                              <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                 <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                              </svg>
                              Draft
                           </span>
                     ` : ''}
                  </div>
               </div>
         </div>
      `;
   }).join('');
}

function renderEmailDetail(email) {
   const currentTab = window.emailDetailState?.activeTab || 'content';
   
   return `
      <div class="flex flex-col h-full bg-white">
         <!-- Header -->
         <div class="p-6 border-b border-slate-200">
               <div class="flex justify-between items-start mb-2">
                  <h1 class="text-xl font-bold text-slate-900 flex-1">${email.subject}</h1>
                  <div class="flex items-center gap-2">
                     ${email.category === 'Unprocessed' ? `
                           <button onclick="processIndividualEmail('${email.id}')" 
                              class="text-xs bg-gradient-to-r from-blue-600 to-purple-600 text-white px-4 py-2 rounded-lg font-medium hover:from-blue-700 hover:to-purple-700 transition-all shadow-sm flex items-center gap-2">
                              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                 <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
                              </svg>
                              Process This Email
                           </button>
                     ` : `
                           <span class="text-xs bg-green-100 text-green-700 px-3 py-1 rounded-full border border-green-200 font-medium">
                              ✓ Processed
                           </span>
                     `}
                     <span class="text-sm text-slate-500 whitespace-nowrap">${new Date(email.timestamp).toLocaleString()}</span>
                  </div>
               </div>
               <div class="flex items-center gap-2 mb-4">
                  <div class="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center text-white font-bold text-xs">
                     ${email.sender[0].toUpperCase()}
                  </div>
                  <div>
                     <p class="text-sm font-medium text-slate-900">${email.sender}</p>
                     <p class="text-xs text-slate-500">to me</p>
                  </div>
               </div>

               <!-- Tabs -->
               <div class="flex gap-6 text-sm font-medium border-b border-slate-100">
                  <button onclick="changeEmailTab('${email.id}', 'content')"
                     class="pb-2 transition-colors ${currentTab === 'content' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-slate-500 hover:text-slate-700'}">
                     Email Content
                  </button>
                  <button onclick="changeEmailTab('${email.id}', 'draft')"
                     class="pb-2 transition-colors ${currentTab === 'draft' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-slate-500 hover:text-slate-700'}">
                     Draft Reply ${email.draftReply ? '•' : ''}
                  </button>
                  <button onclick="changeEmailTab('${email.id}', 'chat')"
                     class="pb-2 transition-colors ${currentTab === 'chat' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-slate-500 hover:text-slate-700'}">
                     Agent Chat
                  </button>
               </div>
         </div>

         <!-- Body Content -->
         <div class="flex-1 overflow-hidden ${currentTab === 'chat' ? '' : 'overflow-y-auto p-6 bg-slate-50'}" id="email-detail-content">
               ${renderEmailDetailContent(email, currentTab)}
         </div>
      </div>
   `;
}

function renderEmailDetailContent(email, tab) {
   if (tab === 'content') {
      return renderContentTab(email);
   } else if (tab === 'draft') {
      return renderDraftTab(email);
   } else if (tab === 'chat') {
      return renderChatTab(email);
   }
}

function renderEmptyState() {
   return `
      <div class="flex flex-col items-center justify-center h-full text-slate-400">
         <div class="w-24 h-24 bg-slate-200 rounded-full flex items-center justify-center mb-4">
               <svg class="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
               </svg>
         </div>
         <p class="text-lg font-medium text-slate-500">Select an email to begin</p>
         <p class="text-sm max-w-xs text-center mt-2">
               Configure the "Agent Brain" to change how emails are categorized and processed.
         </p>
      </div>
   `;
}
