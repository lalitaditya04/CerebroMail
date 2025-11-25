"""
Chat History Routes
Handles saving and loading chat conversations
"""

from flask import Blueprint, request, jsonify, session
from datetime import datetime
import json
from database import DatabaseManager
from middleware.security import rate_limit_moderate, limit_content_length

bp = Blueprint('chat', __name__, url_prefix='/api/chat')

# Initialize database
db = DatabaseManager()


@bp.route('/test', methods=['GET'])
def test_chat_routes():
    """Test if chat routes are working"""
    chats = db.list_chats()
    return jsonify({
        'status': 'Chat routes are working!',
        'storage_type': 'SQLite Database',
        'chat_count': len(chats),
        'chats': chats
    })


@bp.route('/save', methods=['POST'])
@rate_limit_moderate  # 30 requests per minute
@limit_content_length(1024 * 100)  # 100KB max
def save_chat():
    """Save chat history for an email"""
    try:
        print("=" * 50)
        print("Received chat save request")
        
        data = request.json
        print(f"Request data: {data}")
        
        email_id = data.get('email_id')
        messages = data.get('messages', [])
        user_email = data.get('user_email')  # Gmail user email or None for mock
        
        print(f"Saving chat:")
        print(f"  - Email ID: {email_id}")
        print(f"  - User: {user_email}")
        print(f"  - Messages: {len(messages)}")
        
        if not email_id:
            print("Error: email_id is required")
            return jsonify({'error': 'email_id is required'}), 400
        
        # Save to database
        db.save_chat(email_id, messages, user_email)
        
        print(f"Chat saved to database!")
        print(f"Total chats: {len(db.list_chats())}")
        print("=" * 50)
        
        return jsonify({
            'success': True,
            'message': 'Chat history saved to database',
            'message_count': len(messages)
        })
        
    except Exception as e:
        print(f"Error saving chat: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('/load/<email_id>', methods=['GET'])
def load_chat(email_id):
    """Load chat history for an email"""
    try:
        print("=" * 50)
        print("Loading chat request")
        
        # Get user email from session (if Gmail user)
        user_email = session.get('gmail_user_email')
        
        print(f"Loading chat:")
        print(f"  - Email ID: {email_id}")
        print(f"  - Session user: {user_email}")
        
        # Load from database
        chat_data = db.load_chat(email_id, user_email)
        
        if chat_data:
            print(f"Found chat with {len(chat_data['messages'])} messages")
            print("=" * 50)
            return jsonify({
                'success': True,
                'messages': chat_data['messages'],
                'last_updated': chat_data['last_updated']
            })
        else:
            print(f"No chat found in database")
            print("=" * 50)
            return jsonify({
                'success': True,
                'messages': [],
                'last_updated': None
            })
            
    except Exception as e:
        print(f"Error loading chat: {e}")
        print("=" * 50)
        return jsonify({'error': str(e)}), 500


@bp.route('/delete/<email_id>', methods=['DELETE'])
def delete_chat(email_id):
    """Delete chat history for an email"""
    try:
        user_email = session.get('gmail_user_email')
        
        deleted = db.delete_chat(email_id, user_email)
        
        if deleted:
            return jsonify({
                'success': True,
                'message': 'Chat history deleted from database'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Chat history not found'
            }), 404
            
    except Exception as e:
        print(f"Error deleting chat: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('/list', methods=['GET'])
def list_chats():
    """List all chat histories for current user"""
    try:
        user_email = session.get('gmail_user_email')
        
        # Get chats from database
        chats = db.list_chats(user_email)
        
        return jsonify({
            'success': True,
            'chats': chats
        })
        
    except Exception as e:
        print(f"Error listing chats: {e}")
        return jsonify({'error': str(e)}), 500
