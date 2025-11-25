"""
Email Routes
Handles email CRUD operations and inbox management
Single Responsibility: Email data management
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
from models import EmailCategory
from config import DEFAULT_PROMPTS, get_mock_inbox, get_gmail_mock_inbox

bp = Blueprint('emails', __name__, url_prefix='/api/emails')

# In-memory storage (for demo)
emails_store = {}


@bp.route('', methods=['GET'])
def get_emails():
    """Get all emails"""
    from routes.ai_routes import get_last_auto_processed
    return jsonify({
        'emails': list(emails_store.values()),
        'lastAutoProcessed': get_last_auto_processed()
    })


@bp.route('/load-mock', methods=['POST'])
def load_mock_emails():
    """Load mock inbox data"""
    global emails_store
    emails_store = {}
    
    for email in get_mock_inbox():
        email_copy = email.copy()
        # Reset to unprocessed
        email_copy['category'] = EmailCategory.UNPROCESSED.value
        email_copy['actionItems'] = []
        email_copy['draftReply'] = None
        email_copy['customAnalysis'] = None
        emails_store[email_copy['id']] = email_copy
    
    return jsonify({
        'success': True,
        'emails': list(emails_store.values())
    })


@bp.route('/load-gmail', methods=['POST'])
def load_gmail_emails():
    """Load Gmail mock data (simulated connection)"""
    global emails_store
    emails_store = {}
    
    for email in get_gmail_mock_inbox():
        emails_store[email['id']] = email.copy()
    
    return jsonify({
        'success': True,
        'emails': list(emails_store.values())
    })


@bp.route('/<email_id>', methods=['GET', 'PUT'])
def email_detail(email_id):
    """Get or update a specific email"""
    if request.method == 'GET':
        email = emails_store.get(email_id)
        if not email:
            return jsonify({'error': 'Email not found'}), 404
        return jsonify(email)
    
    elif request.method == 'PUT':
        if email_id not in emails_store:
            return jsonify({'error': 'Email not found'}), 404
        
        data = request.json
        emails_store[email_id].update(data)
        return jsonify(emails_store[email_id])


@bp.route('/simulate-new', methods=['POST'])
def simulate_new_email():
    """Simulate a new email arrival - processes automatically"""
    import random
    from datetime import datetime
    
    # New email templates
    new_emails_pool = [
        {
            'sender': 'urgent@client.com',
            'subject': 'URGENT: Server Down!',
            'body': 'Our production server is down. Please investigate immediately and provide an ETA for resolution.'
        },
        {
            'sender': 'partner@business.com',
            'subject': 'Partnership Proposal',
            'body': 'We would like to discuss a potential partnership. Are you available for a call next week?'
        },
        {
            'sender': 'news@dailytech.com',
            'subject': 'Daily Tech News Digest',
            'body': 'Here are today\'s top tech stories: AI breakthroughs, startup funding news, and more...'
        },
        {
            'sender': 'spam@offers.com',
            'subject': 'You WON a FREE iPhone!!!',
            'body': 'Click here NOW to claim your prize! Limited time offer! Act fast!'
        },
        {
            'sender': 'project.lead@company.com',
            'subject': 'Project Alpha Status Update Required',
            'body': 'Please provide a status update on Project Alpha by EOD. We need to present to stakeholders tomorrow.'
        }
    ]
    
    # Pick a random email template
    template = random.choice(new_emails_pool)
    
    # Generate unique ID
    email_id = f'new_{int(datetime.now().timestamp() * 1000)}'
    
    new_email = {
        'id': email_id,
        'sender': template['sender'],
        'subject': template['subject'],
        'timestamp': datetime.now().isoformat(),
        'body': template['body'],
        'isRead': False,
        'category': EmailCategory.UNPROCESSED.value,
        'actionItems': [],
        'draftReply': None,
        'summary': None,
        'customAnalysis': None
    }
    
    # Add to store (unprocessed)
    emails_store[email_id] = new_email
    
    return jsonify({
        'success': True,
        'email': new_email,
        'message': 'New email arrived! Use "Process New Email" to analyze it.'
    })


def get_email_store():
    """Accessor for email store (Dependency Inversion)"""
    return emails_store


def update_email(email_id, updates):
    """Update email in store (Encapsulation)"""
    if email_id in emails_store:
        emails_store[email_id].update(updates)
        return emails_store[email_id]
    return None
