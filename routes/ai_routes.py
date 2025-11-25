"""
AI Routes
Handles AI processing operations
Single Responsibility: AI operations and processing
"""

from flask import Blueprint, request, jsonify, session
from datetime import datetime
import os
from dotenv import load_dotenv
from services import GeminiService
from services.email_storage import email_storage
from routes.email_routes import get_email_store, update_email
from routes.config_routes import get_prompts_store
from middleware.security import rate_limit_ai, rate_limit_moderate, limit_content_length

load_dotenv()

bp = Blueprint('ai', __name__, url_prefix='/api')

# Initialize Gemini service with model from environment
gemini_service = GeminiService(
    api_key=os.getenv('GEMINI_API_KEY', ''),
    model_name=os.getenv('AI_MODEL', 'gemini-1.5-flash')
)

# Last auto-processed timestamp
last_auto_processed = 0


def get_last_auto_processed():
    """Accessor for last auto-processed timestamp"""
    return last_auto_processed


@bp.route('/process-inbox', methods=['POST'])
@rate_limit_ai  # 5 requests per minute (expensive AI operation)
def process_inbox():
    """Process all unprocessed emails with AI agent"""
    global last_auto_processed
    
    emails_store = get_email_store()
    prompts_store = get_prompts_store()
    
    if not emails_store:
        return jsonify({'error': 'No emails to process'}), 400
    
    processed_emails = []
    
    # Get user ID from session
    user_id = session.get('gmail_user_id')
    
    # Only process unprocessed emails to avoid wasting tokens
    for email_id, email in list(emails_store.items()):
        if email.get('category') != 'Unprocessed':
            processed_emails.append(email)
            continue
            
        # 1. Categorize with AI (returns AI-generated category)
        category = gemini_service.categorize_email(email, prompts_store['categorization'])
        email['category'] = category
        
        # Add category to database if it doesn't exist
        email_storage.add_category(category)
        
        # 2. Extract actions (skip for spam/newsletter-like categories)
        skip_categories = ['spam', 'newsletter', 'promotional']
        if category.lower() not in skip_categories:
            actions = gemini_service.extract_action_items(email, prompts_store['actionExtraction'])
            email['actionItems'] = actions
            
            # 3. Run custom analyzers
            if prompts_store.get('customAnalyzers'):
                custom_analysis = {}
                for analyzer in prompts_store['customAnalyzers']:
                    result = gemini_service.run_custom_analyzer(email, analyzer['prompt'])
                    custom_analysis[analyzer['name']] = result
                email['customAnalysis'] = custom_analysis
            
            # 4. Auto-draft for important-like emails
            important_keywords = ['important', 'urgent', 'priority', 'critical']
            if any(keyword in category.lower() for keyword in important_keywords) and not email.get('draftReply'):
                draft = gemini_service.generate_draft_reply(
                    email, 
                    prompts_store['autoReply'],
                    "Note: This is an auto-generated draft for a high priority email."
                )
                email['draftReply'] = draft
        
        # Save to database
        if user_id:
            email_storage.save_email(email, user_id)
        
        processed_emails.append(email)
    
    last_auto_processed = int(datetime.now().timestamp() * 1000)
    
    return jsonify({
        'success': True,
        'emails': processed_emails,
        'lastAutoProcessed': last_auto_processed
    })


@bp.route('/process-new-email', methods=['POST'])
@rate_limit_ai  # 5 requests per minute
def process_new_email():
    """Process a single newly arrived email with AI (triggered on new email arrival)"""
    data = request.json
    email = data.get('email')
    
    if not email:
        return jsonify({'error': 'Email data required'}), 400
    
    prompts_store = get_prompts_store()
    user_id = session.get('gmail_user_id')
    
    # 1. Categorize with AI
    category = gemini_service.categorize_email(email, prompts_store['categorization'])
    email['category'] = category
    
    # Add category to database if it doesn't exist
    email_storage.add_category(category)
    
    # 2. Extract actions (skip for spam/newsletter-like categories)
    skip_categories = ['spam', 'newsletter', 'promotional']
    if category.lower() not in skip_categories:
        actions = gemini_service.extract_action_items(email, prompts_store['actionExtraction'])
        email['actionItems'] = actions
        
        # 3. Auto-draft for important-like emails
        important_keywords = ['important', 'urgent', 'priority', 'critical']
        if any(keyword in category.lower() for keyword in important_keywords):
            draft = gemini_service.generate_draft_reply(
                email, 
                prompts_store['autoReply'],
                "Note: This is an auto-generated draft for a high priority email."
            )
            email['draftReply'] = draft
    
    # Update in store
    emails_store = get_email_store()
    emails_store[email['id']] = email
    
    # Save to database
    if user_id:
        email_storage.save_email(email, user_id)
    
    return jsonify({
        'success': True,
        'email': email,
        'processed': True
    })


@bp.route('/categorize', methods=['POST'])
def categorize_email_endpoint():
    """Categorize a single email"""
    data = request.json
    email = data.get('email')
    prompts_store = get_prompts_store()
    prompt = data.get('prompt', prompts_store['categorization'])
    
    category = gemini_service.categorize_email(email, prompt)
    return jsonify({'category': category})


@bp.route('/extract-actions', methods=['POST'])
@rate_limit_ai  # 5 requests per minute
def extract_actions():
    """Extract action items from an email (manual trigger)"""
    data = request.json
    email = data.get('email')
    prompts_store = get_prompts_store()
    prompt = data.get('prompt', prompts_store['actionExtraction'])
    
    actions = gemini_service.extract_action_items(email, prompt)
    return jsonify({'actionItems': actions})


@bp.route('/summarize', methods=['POST'])
def summarize_email_endpoint():
    """Generate summary for an email"""
    data = request.json
    email = data.get('email')
    
    summary = gemini_service.summarize_email(email)
    
    # Update stored email
    update_email(email.get('id'), {'summary': summary})
    
    return jsonify({'summary': summary})


@bp.route('/generate-draft', methods=['POST'])
@rate_limit_ai  # 5 requests per minute
def generate_draft():
    """Generate draft reply for an email"""
    data = request.json
    email = data.get('email')
    custom_instruction = data.get('instruction', '')
    prompts_store = get_prompts_store()
    prompt = data.get('prompt', prompts_store['autoReply'])
    
    draft = gemini_service.generate_draft_reply(email, prompt, custom_instruction)
    
    # Update stored email
    update_email(email.get('id'), {'draftReply': draft})
    
    return jsonify({'draft': draft})


@bp.route('/categories', methods=['GET'])
def get_categories():
    """Get all available email categories"""
    categories = email_storage.get_all_categories()
    return jsonify({
        'success': True,
        'categories': categories
    })


@bp.route('/chat', methods=['POST'])
def chat_with_email():
    """Chat about an email with the AI agent"""
    try:
        data = request.json
        email = data.get('email')
        history = data.get('history', [])
        user_message = data.get('message')
        
        if not email or not user_message:
            return jsonify({'error': 'Email and message are required'}), 400
        
        response = gemini_service.chat_with_email_agent(email, history, user_message)
        
        if not response:
            return jsonify({'error': 'No response from AI'}), 500
            
        return jsonify({'response': response})
    except Exception as e:
        print(f"Chat error: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('/custom-analyzer', methods=['POST'])
def run_custom_analyzer():
    """Run a custom analyzer on an email"""
    data = request.json
    email = data.get('email')
    prompt = data.get('prompt')
    
    result = gemini_service.run_custom_analyzer(email, prompt)
    return jsonify({'result': result})


@bp.route('/save-draft', methods=['POST'])
def save_draft():
    """Save a draft reply to an email"""
    data = request.json
    email_id = data.get('emailId')
    draft = data.get('draft')
    
    result = update_email(email_id, {'draftReply': draft})
    
    if not result:
        return jsonify({'error': 'Email not found'}), 404
    
    return jsonify({'success': True})


@bp.route('/model-config', methods=['GET'])
def get_model_config():
    """Get current AI model configuration"""
    return jsonify({
        'current_model': os.getenv('AI_MODEL', 'gemini-1.5-flash'),
        'available_models': [
            'gemini-2.5-flash',
            'gemini-2.5-flash-lite',
            'gemini-2.0-flash',
            'gemini-1.5-flash'
        ],
        'api_configured': bool(os.getenv('GEMINI_API_KEY'))
    })


@bp.route('/model-config', methods=['POST'])
def update_model_config():
    """Update AI model configuration"""
    data = request.json
    model_name = data.get('model_name')
    
    if not model_name:
        return jsonify({'error': 'model_name is required'}), 400
    
    # Update environment variable
    os.environ['AI_MODEL'] = model_name
    
    # Reinitialize Gemini service with new model
    global gemini_service
    try:
        gemini_service = GeminiService(
            api_key=os.getenv('GEMINI_API_KEY', ''),
            model_name=model_name
        )
        return jsonify({
            'success': True,
            'model': model_name,
            'message': f'Successfully switched to {model_name}'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
