"""
Constants and Mock Data
Default prompts and mock email datasets
"""

from datetime import datetime, timedelta
from models.email_models import EmailCategory


# Default prompt configurations
DEFAULT_PROMPTS = {
    'categorization': """Analyze the email content and categorize it into exactly one of the following: Important, Newsletter, Spam, To-Do, Project. 
"To-Do" emails must include a direct request requiring user action. 
"Important" is for high-stakes communication from leadership or clients.
Return ONLY the category name.""",
    
    'actionExtraction': """Extract actionable tasks from the email. 
Return a JSON object with a key "tasks" containing an array of objects. 
Each object must have: "task" (string description), "deadline" (string or null), and "priority" (High/Medium/Low).
If no tasks, return an empty array.""",
    
    'autoReply': """Draft a polite, professional reply based on the sender's tone. 
If it is a meeting request, ask for an agenda if missing. 
If it is a task assignment, acknowledge receipt and estimated completion time.
Keep it concise.""",
    
    'customAnalyzers': []
}


# Mock inbox data
MOCK_INBOX = [
    {
        'id': '1',
        'sender': 'sarah.manager@company.com',
        'subject': 'Urgent: Q3 Report Review',
        'timestamp': (datetime.now() - timedelta(hours=3)).isoformat(),
        'body': 'Hi Team, I need everyone to review the attached Q3 financial report by EOD tomorrow. It is crucial for the board meeting on Monday. Please highlight any discrepancies.',
        'isRead': False,
        'category': EmailCategory.UNPROCESSED.value,
        'actionItems': []
    },
    {
        'id': '2',
        'sender': 'newsletter@techweekly.com',
        'subject': 'Top 10 AI Trends of 2024',
        'timestamp': (datetime.now() - timedelta(hours=5)).isoformat(),
        'body': 'Welcome to TechWeekly! In this edition, we explore the rise of agents, the fall of legacy code, and how to optimize your React apps...',
        'isRead': False,
        'category': EmailCategory.UNPROCESSED.value,
        'actionItems': []
    },
    {
        'id': '3',
        'sender': 'alex.dev@company.com',
        'subject': 'Sync on Project Titan?',
        'timestamp': (datetime.now() - timedelta(days=1, hours=7)).isoformat(),
        'body': "Hey, are you free to sync regarding the API migration? I'm stuck on the authentication flow. Let's meet tomorrow at 2 PM if possible.",
        'isRead': True,
        'category': EmailCategory.UNPROCESSED.value,
        'actionItems': []
    },
    {
        'id': '4',
        'sender': 'deals@cheapflights.com',
        'subject': 'Last Chance: 50% off to Bali!',
        'timestamp': (datetime.now() - timedelta(days=1, hours=10)).isoformat(),
        'body': "Don't miss out on these incredible savings. Book now before midnight!",
        'isRead': False,
        'category': EmailCategory.UNPROCESSED.value,
        'actionItems': []
    },
    {
        'id': '5',
        'sender': 'ceo@company.com',
        'subject': 'Company All-Hands',
        'timestamp': (datetime.now() - timedelta(days=2, hours=14)).isoformat(),
        'body': 'Team, we will have an all-hands meeting next Friday at 10 AM to discuss the annual roadmap. Attendance is mandatory.',
        'isRead': True,
        'category': EmailCategory.UNPROCESSED.value,
        'actionItems': []
    }
]


# Gmail mock inbox (simulated connection)
GMAIL_MOCK_INBOX = [
    {
        'id': 'g1',
        'sender': 'alert@bank.com',
        'subject': 'Security Alert: New sign-in detected',
        'timestamp': datetime.now().isoformat(),
        'body': 'We detected a new sign-in to your account from a new device. If this was you, you can ignore this email.',
        'isRead': False,
        'category': EmailCategory.UNPROCESSED.value,
        'actionItems': []
    },
    {
        'id': 'g2',
        'sender': 'recruiter@techjobs.com',
        'subject': 'Interview Request: Senior Frontend Engineer',
        'timestamp': (datetime.now() - timedelta(hours=1)).isoformat(),
        'body': 'Hi, we were impressed by your profile. Are you available for a 30-minute intro call this week? Please let us know your availability.',
        'isRead': True,
        'category': EmailCategory.UNPROCESSED.value,
        'actionItems': []
    },
    {
        'id': 'g3',
        'sender': 'billing@aws.com',
        'subject': 'AWS Invoice Available',
        'timestamp': (datetime.now() - timedelta(days=1)).isoformat(),
        'body': 'Your AWS invoice for the previous month is now available. Total amount: $12.34. Please login to the console to view details.',
        'isRead': False,
        'category': EmailCategory.UNPROCESSED.value,
        'actionItems': []
    }
]
