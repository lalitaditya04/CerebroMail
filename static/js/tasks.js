// ==================== TASK MANAGEMENT ====================

function toggleTaskCompletion(emailId, taskIndex) {
    const currentEmails = getCurrentEmails();
    const email = currentEmails.find(e => e.id === emailId);
    if (!email || !email.actionItems[taskIndex]) return;
    
    email.actionItems[taskIndex].isCompleted = !email.actionItems[taskIndex].isCompleted;
    updateEmail(email);
}

function addEmailToTasks(emailId) {
    const currentEmails = getCurrentEmails();
    const email = currentEmails.find(e => e.id === emailId);
    if (!email || !email.actionItems || email.actionItems.length === 0) {
        alert('No action items to add!');
        return;
    }
    
    state.emailsAddedToTasks.add(emailId);
    showNotification(`✅ ${email.actionItems.length} task(s) added to To-Do list!`);
    render();
}

function deleteTask(emailId, taskIndex) {
    if (!confirm('Are you sure you want to delete this task?')) {
        return;
    }
    
    const currentEmails = getCurrentEmails();
    const email = currentEmails.find(e => e.id === emailId);
    if (!email || !email.actionItems) return;
    
    // Remove the task
    email.actionItems.splice(taskIndex, 1);
    
    // If no more tasks, remove from tasks set
    if (email.actionItems.length === 0) {
        state.emailsAddedToTasks.delete(emailId);
    }
    
    showNotification('🗑️ Task deleted');
    render();
}

function addToCalendar(task, emailSubject) {
    const title = encodeURIComponent(task);
    const details = encodeURIComponent(`Origin Email: ${emailSubject}`);
    const calendarUrl = `https://calendar.google.com/calendar/render?action=TEMPLATE&text=${title}&details=${details}`;
    window.open(calendarUrl, '_blank');
}

function setTodoFilter(filter) {
    window.todoFilter = filter;
    render();
}

function changeTodoFilter(filter) {
    window.todoFilter = filter;
    render();
}

function selectEmailFromTask(emailId) {
    selectEmail(emailId);
    changeView('inbox');
}
