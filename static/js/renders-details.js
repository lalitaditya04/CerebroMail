// This file contains the detailed rendering functions for email content, drafts, chat, prompts, and tasks

function renderContentTab(email) {
   return `
      <div class="max-w-3xl mx-auto space-y-6">
         <!-- Summary Section -->
         <div class="bg-indigo-50 p-6 rounded-xl border border-indigo-100">
               <div class="flex justify-between items-center mb-3">
                  <h3 class="text-sm font-bold text-indigo-900 uppercase tracking-wide flex items-center gap-2">
                     ✨ AI Summary
                  </h3>
                  ${!email.summary ? `
                     <button onclick="handleGenerateSummary('${email.id}')"
                           class="text-xs bg-white text-indigo-600 px-3 py-1 rounded-full border border-indigo-200 hover:bg-indigo-50 font-medium transition-colors">
                           Generate Summary
                     </button>
                  ` : ''}
               </div>
               ${email.summary ? `
                  <p class="text-sm text-indigo-800 leading-relaxed">${email.summary}</p>
               ` : `
                  <p class="text-sm text-indigo-400 italic">No summary generated yet.</p>
               `}
         </div>

         <!-- Custom Analysis -->
         ${email.customAnalysis && Object.keys(email.customAnalysis).length > 0 ? `
               <div class="bg-emerald-50 p-6 rounded-xl border border-emerald-100 space-y-3">
                  <h3 class="text-sm font-bold text-emerald-900 uppercase tracking-wide">Analysis</h3>
                  ${Object.entries(email.customAnalysis).map(([key, value]) => `
                     <div>
                           <span class="text-xs font-bold text-emerald-700 uppercase">${key}: </span>
                           <span class="text-sm text-emerald-900">${value}</span>
                     </div>
                  `).join('')}
               </div>
         ` : ''}

         <!-- Main Body -->
         <div class="bg-white p-8 rounded-xl shadow-sm border border-slate-200">
               <div class="prose prose-slate max-w-none">
                  <div class="text-slate-900 leading-relaxed" style="word-wrap: break-word; overflow-wrap: anywhere; white-space: pre-wrap;">
                     ${email.body.replace(/((https?:\/\/[^\s]+)|(\S+@\S+\.\S+))/g, '<a href="$1" target="_blank" class="text-blue-600 hover:underline break-all">$1</a>')}
                  </div>
               </div>
         </div>

         <!-- Action Items -->
         <div class="bg-amber-50 p-6 rounded-xl border border-amber-100">
               <div class="flex justify-between items-center mb-4">
                  <h3 class="text-sm font-bold text-amber-900 uppercase tracking-wide">✨ Action Items</h3>
                  <div class="flex gap-2">
                     <button onclick="handleExtractActions('${email.id}')"
                           class="text-xs bg-white text-amber-600 px-3 py-1 rounded-full border border-amber-200 hover:bg-amber-50 font-medium transition-colors flex items-center gap-1">
                           <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
                           </svg>
                           ${email.actionItems && email.actionItems.length > 0 ? 'Re-extract' : 'Extract'} Actions
                     </button>
                     ${email.actionItems && email.actionItems.length > 0 ? `
                           <button onclick="addEmailToTasks('${email.id}')" ${state.emailsAddedToTasks.has(email.id) ? 'disabled' : ''}
                              class="text-xs px-3 py-1 rounded-full font-medium transition-colors flex items-center gap-1 ${
                                 state.emailsAddedToTasks.has(email.id) 
                                 ? 'bg-green-100 text-green-700 border border-green-200 cursor-not-allowed' 
                                 : 'bg-blue-600 text-white hover:bg-blue-700'
                              }">
                              <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                 <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
                              </svg>
                              ${state.emailsAddedToTasks.has(email.id) ? '✓ Added to Tasks' : 'Add to Tasks'}
                           </button>
                     ` : ''}
                  </div>
               </div>
               ${email.actionItems && email.actionItems.length > 0 ? `
                  <ul class="space-y-3">
                     ${email.actionItems.map((item, idx) => `
                           <li class="flex items-start gap-3 bg-white p-3 rounded-lg border border-amber-100 shadow-sm">
                              <input type="checkbox" ${item.isCompleted ? 'checked' : ''} 
                                 onchange="toggleTaskCompletion('${email.id}', ${idx})"
                                 class="mt-1 text-amber-600 rounded focus:ring-amber-500">
                              <div class="flex-1">
                                 <p class="text-sm font-medium text-slate-800">${item.task}</p>
                                 <div class="flex gap-2 mt-1">
                                       ${item.deadline ? `<span class="text-xs text-amber-600 font-medium bg-amber-50 px-2 py-0.5 rounded">Due: ${item.deadline}</span>` : ''}
                                       ${item.priority ? `<span class="text-xs text-slate-500 bg-slate-100 px-2 py-0.5 rounded">${item.priority} Priority</span>` : ''}
                                 </div>
                              </div>
                           </li>
                     `).join('')}
                  </ul>
               ` : `
                  <p class="text-sm text-amber-600 italic">No action items extracted yet. Click "Extract Actions" to analyze this email.</p>
               `}
         </div>
      </div>
   `;
}

function renderDraftTab(email) {
   const draftInstruction = window.emailDetailState?.draftInstruction || '';
   const drafts = state.emailDrafts[email.id] || [];
   const activeDraftId = window.emailDetailState?.activeDraftId || (drafts.length > 0 ? drafts[0].id : null);
   const activeDraft = drafts.find(d => d.id === activeDraftId) || { id: null, content: '', title: 'New Draft' };
   
   return `
      <div class="max-w-4xl mx-auto h-full flex gap-4">
         <!-- Drafts Sidebar -->
         <div class="w-64 bg-white rounded-xl shadow-sm border border-slate-200 flex flex-col overflow-hidden">
               <div class="bg-gradient-to-r from-blue-600 to-purple-600 px-4 py-3 text-white">
                  <h3 class="text-sm font-bold">Saved Drafts (${drafts.length})</h3>
               </div>
               
               <div class="p-2">
                  <button onclick="createNewDraft('${email.id}')"
                     class="w-full bg-blue-50 hover:bg-blue-100 text-blue-700 px-3 py-2 rounded-lg text-sm font-medium flex items-center justify-center gap-2 transition-colors border border-blue-200">
                     <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                           <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                     </svg>
                     New Draft
                  </button>
               </div>
               
               <div class="flex-1 overflow-y-auto p-2 space-y-1">
                  ${drafts.length === 0 ? `
                     <div class="text-center py-8 text-slate-400 text-xs">
                           <p>No drafts yet</p>
                           <p class="mt-1">Click "New Draft" to start</p>
                     </div>
                  ` : drafts.map(draft => `
                     <div onclick="selectDraft('${email.id}', '${draft.id}')"
                           class="p-3 rounded-lg cursor-pointer transition-colors border ${
                              draft.id === activeDraftId 
                              ? 'bg-blue-50 border-blue-300' 
                              : 'bg-slate-50 border-slate-200 hover:bg-slate-100'
                           }">
                           <div class="flex justify-between items-start mb-1">
                              <p class="text-xs font-semibold text-slate-800 truncate flex-1">${draft.title}</p>
                              <button onclick="event.stopPropagation(); deleteDraft('${email.id}', '${draft.id}')"
                                 class="text-red-500 hover:text-red-700 ml-1">
                                 <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                       <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                                 </svg>
                              </button>
                           </div>
                           <p class="text-[10px] text-slate-500">${new Date(draft.timestamp).toLocaleString()}</p>
                           <p class="text-xs text-slate-600 mt-1 line-clamp-2">${draft.content.substring(0, 60)}...</p>
                     </div>
                  `).join('')}
               </div>
         </div>
         
         <!-- Draft Editor -->
         <div class="flex-1 flex flex-col">
               <div class="bg-white p-4 rounded-xl shadow-sm border border-slate-200 mb-4">
                  <div class="flex gap-2 mb-3">
                     <input type="text" id="draft-title-${email.id}"
                           class="flex-1 border border-slate-300 rounded-lg px-3 py-2 text-sm font-semibold focus:ring-2 focus:ring-blue-500 outline-none bg-white text-slate-900"
                           placeholder="Draft Title..."
                           value="${activeDraft.title}"
                           onchange="updateDraftTitle('${email.id}', '${activeDraftId}', this.value)">
                  </div>
                  <label class="block text-xs font-medium text-slate-700 mb-2">AI Instructions (Optional)</label>
                  <div class="flex gap-2">
                     <input type="text" id="draft-instruction"
                           class="flex-1 border border-slate-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 outline-none bg-white text-slate-900"
                           placeholder="e.g., Make it formal, add apology, mention deadline..."
                           value="${draftInstruction}"
                           onchange="updateDraftInstruction(this.value)">
                     <button onclick="generateDraftWithAI('${email.id}')"
                           class="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:from-blue-700 hover:to-purple-700 flex items-center gap-2 whitespace-nowrap">
                           <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
                           </svg>
                           Generate
                     </button>
                  </div>
               </div>

               <div class="flex-1 bg-white rounded-xl shadow-sm border border-slate-200 flex flex-col overflow-hidden">
                  <div class="bg-slate-50 px-4 py-2 border-b border-slate-200 flex justify-between items-center">
                     <span class="text-xs font-medium text-slate-500 uppercase tracking-wider">Draft Editor</span>
                     <span class="text-xs text-green-600 font-medium">✓ Auto-saved</span>
                  </div>
                  <textarea id="draft-content-${email.id}"
                     class="flex-1 p-6 w-full h-full resize-none outline-none bg-white text-slate-900 leading-relaxed font-sans"
                     placeholder="Start typing your draft or use AI to generate one..."
                     oninput="autoSaveDraft('${email.id}', '${activeDraftId}', this.value)"
                     style="color: #0f172a; background-color: #ffffff;">${activeDraft.content}</textarea>
               </div>
         </div>
      </div>
   `;
}

function renderChatTab(email) {
   if (!window.chatState) {
      window.chatState = {};
   }
   if (!window.chatState[email.id]) {
      window.chatState[email.id] = {
         messages: [{
               role: 'model',
               text: `Hello! I've read the email from ${email.sender.split('@')[0]}. How can I help you with it?`,
               timestamp: Date.now()
         }],
         input: '',
         isChatting: false
      };
   }

   const chatData = window.chatState[email.id];
   const canSend = chatData.input.trim().length > 0 && !chatData.isChatting;
   const messageCount = chatData.messages.length - 1; // Exclude initial greeting

   return `
      <div class="h-full flex flex-col bg-white">
         <!-- Chat Header -->
         <div class="px-6 py-3 bg-gradient-to-r from-blue-50 to-purple-50 border-b border-slate-200">
               <div class="flex items-center justify-between">
                  <div class="flex items-center gap-2">
                     <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                           <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"/>
                     </svg>
                     <span class="text-sm font-semibold text-slate-700">AI Email Assistant</span>
                  </div>
                  <div class="flex items-center gap-2">
                     ${messageCount > 0 ? `
                           <span class="text-xs bg-green-100 text-green-700 px-3 py-1 rounded-full border border-green-200 font-medium">
                              ✓ ${messageCount} message${messageCount > 1 ? 's' : ''} saved
                           </span>
                     ` : ''}
                     <button onclick="testChatSave('${email.id}')" class="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded hover:bg-blue-200" title="Test Save">
                           🧪 Test
                     </button>
                  </div>
               </div>
         </div>
         
         <!-- Chat Messages -->
         <div class="flex-1 overflow-y-auto p-6 bg-gradient-to-b from-slate-50 to-white" id="chat-messages-${email.id}">
               <div class="space-y-4">
                  ${chatData.messages.map((msg, i) => {
                     const escapedText = (msg.text || '').replace(/</g, '&lt;').replace(/>/g, '&gt;');
                     return `
                           <div class="flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'} w-full">
                              <div class="max-w-[75%] rounded-2xl px-4 py-3 text-sm ${
                                 msg.role === 'user' 
                                 ? 'bg-blue-600 text-white rounded-br-none shadow-md' 
                                 : 'bg-white text-slate-800 border border-slate-200 rounded-bl-none shadow-sm'
                              }">
                                 <div style="white-space: pre-wrap; word-wrap: break-word;">${escapedText}</div>
                              </div>
                           </div>
                     `;
                  }).join('\n')}
                  ${chatData.isChatting ? `
                     <div class="flex justify-start w-full">
                           <div class="bg-white px-4 py-3 rounded-2xl rounded-bl-none border border-slate-200 shadow-sm flex gap-1 items-center">
                              <div class="w-2 h-2 bg-slate-400 rounded-full animate-bounce animate-bounce-delay-1"></div>
                              <div class="w-2 h-2 bg-slate-400 rounded-full animate-bounce animate-bounce-delay-2"></div>
                              <div class="w-2 h-2 bg-slate-400 rounded-full animate-bounce animate-bounce-delay-3"></div>
                           </div>
                     </div>
                  ` : ''}
               </div>
         </div>

         <!-- Quick Actions -->
         ${chatData.messages.length <= 2 ? `
               <div class="px-6 py-3 bg-slate-50 border-t border-slate-100">
                  <div class="flex gap-2 overflow-x-auto">
                     <button onclick="handleQuickAction('${email.id}', 'Summarize this email in 2 sentences')"
                           class="text-xs bg-white hover:bg-blue-50 text-slate-700 hover:text-blue-700 px-3 py-2 rounded-lg whitespace-nowrap border border-slate-200 hover:border-blue-300 transition-all shadow-sm">
                           📝 Summarize
                     </button>
                     <button onclick="handleQuickAction('${email.id}', 'What action items are in this email?')"
                           class="text-xs bg-white hover:bg-blue-50 text-slate-700 hover:text-blue-700 px-3 py-2 rounded-lg whitespace-nowrap border border-slate-200 hover:border-blue-300 transition-all shadow-sm">
                           ✅ Find Tasks
                     </button>
                     <button onclick="handleQuickAction('${email.id}', 'Is this email urgent? Why?')"
                           class="text-xs bg-white hover:bg-blue-50 text-slate-700 hover:text-blue-700 px-3 py-2 rounded-lg whitespace-nowrap border border-slate-200 hover:border-blue-300 transition-all shadow-sm">
                           ⚡ Urgency Check
                     </button>
                  </div>
               </div>
         ` : ''}

         <!-- Input Area -->
         <div class="p-6 bg-white border-t border-slate-200">
               <div class="flex items-end gap-3">
                  <div class="flex-1 relative">
                     <input type="text" 
                           id="chat-input-${email.id}"
                           class="w-full px-4 py-3 pr-4 bg-slate-50 border border-slate-200 rounded-2xl text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 focus:bg-white transition-all outline-none text-slate-900 placeholder-slate-400"
                           placeholder="Type your question here..."
                           value="${chatData.input}"
                           onkeydown="if(event.key==='Enter' && !event.shiftKey) { event.preventDefault(); handleChatSend('${email.id}'); }"
                           oninput="updateChatInput('${email.id}', this.value)">
                  </div>
                  <button 
                     id="send-btn-${email.id}"
                     type="button"
                     onclick="handleChatSendClick('${email.id}')"
                     class="flex-shrink-0 p-3 rounded-xl transition-all duration-200 ${
                           canSend
                           ? 'bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white shadow-md hover:shadow-lg transform hover:scale-105 cursor-pointer' 
                           : 'bg-slate-200 text-slate-400 cursor-not-allowed'
                     }">
                     <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                           <path stroke-linecap="round" stroke-linejoin="round" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"/>
                     </svg>
                  </button>
               </div>
               <p class="text-xs text-slate-400 mt-2 px-1">Press Enter to send, Shift+Enter for new line</p>
         </div>
      </div>
   `;
}

function renderPromptManager() {
   if (!window.tempPrompts) {
      window.tempPrompts = JSON.parse(JSON.stringify(state.prompts));
   }
   
   // Fetch current model config if not already loaded
   if (!window.modelConfig) {
      fetchModelConfig();
   }

   return `
      <div class="flex flex-col h-full p-6 bg-slate-50 overflow-y-auto flex-1">
         <div class="max-w-3xl mx-auto w-full pb-20">
               <div class="flex justify-between items-center mb-6">
                  <h2 class="text-2xl font-bold text-slate-800">Agent Brain (Prompt Config)</h2>
                  <button onclick="changeView('inbox')" class="text-slate-500 hover:text-slate-800">Close</button>
               </div>
               
               <p class="text-slate-600 mb-8">
                  Customize how the AI agent perceives and processes your inbox. Changes affect subsequent operations.
               </p>

               <div class="space-y-8">
                  <!-- AI Model Selection -->
                  <div class="bg-gradient-to-br from-blue-50 to-purple-50 p-6 rounded-xl shadow-sm border-2 border-blue-200">
                     <div class="flex items-center gap-2 mb-3">
                           <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
                           </svg>
                           <label class="block text-sm font-bold text-slate-800">AI Model Selection</label>
                     </div>
                     <p class="text-xs text-slate-600 mb-3">Choose the AI model for email processing</p>
                     <select id="model-selector" 
                           onchange="handleModelChange(this.value)"
                           class="w-full p-3 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white">
                           ${window.modelConfig ? window.modelConfig.available_models.map(model => `
                              <option value="${model}" ${model === window.modelConfig.current_model ? 'selected' : ''}>
                                 ${model}
                              </option>
                           `).join('') : '<option>Loading...</option>'}
                     </select>
                     <p class="text-xs text-slate-500 mt-2">
                           Current: <span class="font-semibold text-blue-600">${window.modelConfig?.current_model || 'Loading...'}</span>
                     </p>
                  </div>
               
                  <div class="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
                     <label class="block text-sm font-medium text-slate-700 mb-2">Categorization Prompt</label>
                     <p class="text-xs text-slate-500 mb-3">Define rules for sorting emails into categories.</p>
                     <textarea id="prompt-categorization"
                           class="w-full h-32 p-3 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                           onchange="updatePromptField('categorization', this.value)">${window.tempPrompts.categorization || ''}</textarea>
                  </div>

                  <div class="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
                     <label class="block text-sm font-medium text-slate-700 mb-2">Action Item Extraction Prompt</label>
                     <p class="text-xs text-slate-500 mb-3">Instructions for identifying tasks and deadlines.</p>
                     <textarea id="prompt-actionExtraction"
                           class="w-full h-32 p-3 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                           onchange="updatePromptField('actionExtraction', this.value)">${window.tempPrompts.actionExtraction || ''}</textarea>
                  </div>

                  <div class="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
                     <label class="block text-sm font-medium text-slate-700 mb-2">Auto-Reply Persona</label>
                     <p class="text-xs text-slate-500 mb-3">Set the tone and logic for draft generation.</p>
                     <textarea id="prompt-autoReply"
                           class="w-full h-32 p-3 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                           onchange="updatePromptField('autoReply', this.value)">${window.tempPrompts.autoReply || ''}</textarea>
                  </div>

                  <!-- Custom Analyzers -->
                  <div>
                     <div class="flex justify-between items-center mb-4">
                           <h3 class="text-lg font-bold text-slate-800">Custom Analyzers</h3>
                           <button onclick="addAnalyzer()"
                              class="flex items-center gap-2 text-sm font-medium text-blue-600 hover:text-blue-700">
                              <div class="bg-blue-100 p-1 rounded-full">
                                 <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                       <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                                 </svg>
                              </div>
                              Add Analyzer
                           </button>
                     </div>
                     
                     ${(!window.tempPrompts.customAnalyzers || window.tempPrompts.customAnalyzers.length === 0) ? `
                           <div class="text-center p-8 bg-slate-100 rounded-xl border border-dashed border-slate-300 text-slate-500 text-sm">
                              No custom analyzers added. Add one to extract specific insights like "Sentiment" or "Urgency".
                           </div>
                     ` : `
                           <div class="space-y-4">
                              ${window.tempPrompts.customAnalyzers.map((analyzer, idx) => `
                                 <div class="bg-white p-6 rounded-xl shadow-sm border border-slate-200 relative group">
                                       <button onclick="removeAnalyzer('${analyzer.id}')"
                                          class="absolute top-4 right-4 text-slate-400 hover:text-red-500 transition-colors p-1"
                                          title="Remove Analyzer">
                                          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                             <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                                          </svg>
                                       </button>
                                       
                                       <div class="mb-4">
                                          <label class="block text-xs font-bold text-slate-500 uppercase mb-1">Analyzer Name</label>
                                          <input type="text" 
                                             class="w-full p-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                                             placeholder="e.g., Sentiment Analysis"
                                             value="${analyzer.name}"
                                             onchange="updateAnalyzer('${analyzer.id}', 'name', this.value)">
                                       </div>
                                       <div>
                                          <label class="block text-xs font-bold text-slate-500 uppercase mb-1">Analyzer Prompt</label>
                                          <textarea
                                             class="w-full h-24 p-3 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none resize-none"
                                             placeholder="e.g., Is the tone of this email positive, neutral, or negative?"
                                             onchange="updateAnalyzer('${analyzer.id}', 'prompt', this.value)">${analyzer.prompt}</textarea>
                                       </div>
                                 </div>
                              `).join('')}
                           </div>
                     `}
                  </div>
               </div>

               <div class="fixed bottom-0 left-20 right-0 p-4 bg-white border-t border-slate-200 flex justify-end z-10">
                  <div class="max-w-3xl w-full mx-auto flex justify-end">
                     <button onclick="savePromptsConfig()"
                           class="px-6 py-2 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors shadow-lg">
                           Save Configuration
                     </button>
                  </div>
               </div>
         </div>
      </div>
   `;
}

function renderToDoList() {
   const filter = window.todoFilter || 'All';
   
   // Flatten tasks - from both mock and gmail emails added to tasks
   const allTasks = [];
   
   // Add tasks from mock emails
   state.emails.forEach(email => {
      if (email.actionItems && state.emailsAddedToTasks.has(email.id)) {
         email.actionItems.forEach((item, index) => {
               allTasks.push({
                  ...item,
                  originEmail: email,
                  taskIndex: index,
                  source: 'mock'
               });
         });
      }
   });
   
   // Add tasks from Gmail emails
   state.gmailEmails.forEach(email => {
      if (email.actionItems && state.emailsAddedToTasks.has(email.id)) {
         email.actionItems.forEach((item, index) => {
               allTasks.push({
                  ...item,
                  originEmail: email,
                  taskIndex: index,
                  source: 'gmail'
               });
         });
      }
   });

   // Filter tasks
   const filteredTasks = allTasks.filter(item => {
      if (filter === 'All') return true;
      return item.priority === filter;
   });

   const activeTasks = filteredTasks.filter(item => !item.isCompleted);
   const completedTasks = filteredTasks.filter(item => item.isCompleted);

   return `
      <div class="flex flex-col h-full bg-slate-50 overflow-hidden flex-1">
         <div class="p-6 border-b border-slate-200 bg-white shadow-sm z-10">
               <div class="flex justify-between items-center mb-4">
                  <div>
                     <h2 class="text-2xl font-bold text-slate-800">Action Items & Tasks</h2>
                     <p class="text-slate-500 text-sm mt-1">Manage extracted tasks from your inbox.</p>
                  </div>
               </div>

               <!-- Filter Bar -->
               <div class="flex gap-2">
                  ${['All', 'High', 'Medium', 'Low'].map(f => `
                     <button onclick="changeTodoFilter('${f}')"
                           class="px-4 py-1.5 rounded-full text-xs font-medium transition-all ${
                              filter === f 
                              ? 'bg-slate-800 text-white shadow-md' 
                              : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                           }">
                           ${f} Priority
                     </button>
                  `).join('')}
               </div>
         </div>

         <div class="flex-1 overflow-y-auto p-6 space-y-8">
               ${allTasks.length === 0 ? `
                  <div class="flex flex-col items-center justify-center h-full text-slate-400">
                     <div class="w-16 h-16 bg-slate-200 rounded-full flex items-center justify-center mb-4">
                           <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
                           </svg>
                     </div>
                     <p>No tasks found. Process some emails to extract action items.</p>
                  </div>
               ` : `
                  <div class="max-w-4xl mx-auto space-y-4">
                     ${activeTasks.length > 0 ? activeTasks.map(item => {
                           const priorityColors = {
                              'High': 'bg-red-100 text-red-700',
                              'Medium': 'bg-amber-100 text-amber-700',
                              'Low': 'bg-blue-100 text-blue-700'
                           };
                           
                           return `
                              <div class="bg-white p-4 rounded-xl shadow-sm border border-slate-200 flex items-start gap-4 transition-all hover:shadow-md group">
                                 <input type="checkbox" 
                                       ${item.isCompleted ? 'checked' : ''}
                                       onchange="toggleTaskCompletion('${item.originEmail.id}', ${item.taskIndex})"
                                       class="mt-1.5 w-5 h-5 text-blue-600 rounded focus:ring-blue-500 border-slate-300 cursor-pointer">
                                 
                                 <div class="flex-1">
                                       <h3 class="text-base font-medium text-slate-900 group-hover:text-blue-900 transition-colors">${item.task}</h3>
                                       <div class="flex items-center gap-2 mt-2 text-sm">
                                          ${item.priority ? `
                                             <span class="px-2 py-0.5 rounded text-xs font-semibold ${priorityColors[item.priority] || 'bg-slate-100 text-slate-700'}">
                                                   ${item.priority}
                                             </span>
                                          ` : ''}
                                          ${item.deadline ? `
                                             <span class="text-slate-500 bg-slate-100 px-2 py-0.5 rounded text-xs">
                                                   Due: ${item.deadline}
                                             </span>
                                          ` : ''}
                                          <span class="text-slate-300 mx-1">•</span>
                                          <button onclick="selectEmailFromTask('${item.originEmail.id}')"
                                             class="text-slate-400 hover:text-blue-600 hover:underline cursor-pointer truncate max-w-[200px] text-xs">
                                             From: ${item.originEmail.subject}
                                          </button>
                                       </div>
                                 </div>
                                 
                                 <div class="flex gap-1">
                                       <button onclick="addToCalendar('${item.task}', '${item.originEmail.subject}')"
                                          class="p-2 text-slate-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors flex flex-col items-center gap-1 min-w-[60px]"
                                          title="Add to Google Calendar">
                                          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                             <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                                          </svg>
                                          <span class="text-[10px] font-medium">Calendar</span>
                                       </button>
                                       <button onclick="deleteTask('${item.originEmail.id}', ${item.taskIndex})" 
                                          class="p-2 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors flex flex-col items-center gap-1 min-w-[60px]"
                                          title="Delete task">
                                          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                             <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                                          </svg>
                                          <span class="text-[10px] font-medium">Delete</span>
                                       </button>
                                 </div>
                              </div>
                           `;
                     }).join('') : `
                           <p class="text-center text-slate-400 text-sm py-8 italic">No active tasks matching filter.</p>
                     `}
                  </div>

                  ${completedTasks.length > 0 ? `
                     <div class="max-w-4xl mx-auto pt-4">
                           <h3 class="text-sm font-bold text-slate-400 uppercase tracking-wider mb-4 border-b border-slate-200 pb-2">Marked as Done</h3>
                           <div class="space-y-3 opacity-60 grayscale hover:grayscale-0 transition-all">
                              ${completedTasks.map(item => `
                                 <div class="bg-slate-50 p-3 rounded-lg border border-slate-100 flex items-center gap-4">
                                       <input type="checkbox" checked
                                          onchange="toggleTaskCompletion('${item.originEmail.id}', ${item.taskIndex})"
                                          class="w-4 h-4 text-slate-400 rounded border-slate-300 cursor-pointer">
                                       <div class="flex-1">
                                          <h3 class="text-sm font-medium text-slate-500 line-through">${item.task}</h3>
                                       </div>
                                 </div>
                              `).join('')}
                           </div>
                     </div>
                  ` : ''}
               `}
         </div>
      </div>
   `;
}
