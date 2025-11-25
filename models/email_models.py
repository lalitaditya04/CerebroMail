"""
Email Data Models
Defines email-related data structures
"""

from enum import Enum
from typing import Optional, List, Dict


class EmailCategory(Enum):
    """Email category enumeration"""
    IMPORTANT = 'Important'
    NEWSLETTER = 'Newsletter'
    SPAM = 'Spam'
    TODO = 'To-Do'
    PROJECT = 'Project'
    UNPROCESSED = 'Unprocessed'


class ActionItem:
    """Action item data structure"""
    def __init__(self, task: str, deadline: Optional[str] = None, 
                 priority: Optional[str] = None, is_completed: bool = False):
        self.task = task
        self.deadline = deadline
        self.priority = priority  # 'High', 'Medium', 'Low'
        self.is_completed = is_completed
    
    def to_dict(self):
        return {
            'task': self.task,
            'deadline': self.deadline,
            'priority': self.priority,
            'isCompleted': self.is_completed
        }


class EmailData:
    """Email data structure"""
    def __init__(self, id: str, sender: str, subject: str, timestamp: str, 
                 body: str, is_read: bool = False, 
                 category: EmailCategory = EmailCategory.UNPROCESSED,
                 action_items: List[ActionItem] = None, 
                 draft_reply: Optional[str] = None,
                 summary: Optional[str] = None,
                 custom_analysis: Optional[Dict[str, str]] = None):
        self.id = id
        self.sender = sender
        self.subject = subject
        self.timestamp = timestamp
        self.body = body
        self.is_read = is_read
        self.category = category
        self.action_items = action_items or []
        self.draft_reply = draft_reply
        self.summary = summary
        self.custom_analysis = custom_analysis
    
    def to_dict(self):
        return {
            'id': self.id,
            'sender': self.sender,
            'subject': self.subject,
            'timestamp': self.timestamp,
            'body': self.body,
            'isRead': self.is_read,
            'category': self.category.value,
            'actionItems': [item.to_dict() for item in self.action_items],
            'draftReply': self.draft_reply,
            'summary': self.summary,
            'customAnalysis': self.custom_analysis
        }


class CustomAnalyzer:
    """Custom analyzer configuration"""
    def __init__(self, id: str, name: str, prompt: str):
        self.id = id
        self.name = name
        self.prompt = prompt
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'prompt': self.prompt
        }


class PromptConfig:
    """Prompt configuration structure"""
    def __init__(self, categorization: str, action_extraction: str, 
                 auto_reply: str, custom_analyzers: List[CustomAnalyzer] = None):
        self.categorization = categorization
        self.action_extraction = action_extraction
        self.auto_reply = auto_reply
        self.custom_analyzers = custom_analyzers or []
    
    def to_dict(self):
        return {
            'categorization': self.categorization,
            'actionExtraction': self.action_extraction,
            'autoReply': self.auto_reply,
            'customAnalyzers': [a.to_dict() for a in self.custom_analyzers]
        }


class ChatMessage:
    """Chat message structure"""
    def __init__(self, role: str, text: str, timestamp: int):
        self.role = role  # 'user' or 'model'
        self.text = text
        self.timestamp = timestamp
    
    def to_dict(self):
        return {
            'role': self.role,
            'text': self.text,
            'timestamp': self.timestamp
        }
