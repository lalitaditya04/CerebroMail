"""
Configuration Routes
Handles application configuration and prompts
Single Responsibility: Configuration management
"""

from flask import Blueprint, request, jsonify
from config import DEFAULT_PROMPTS

bp = Blueprint('config', __name__, url_prefix='/api')

# Prompts storage
prompts_store = DEFAULT_PROMPTS.copy()


@bp.route('/prompts', methods=['GET', 'PUT'])
def prompts_config():
    """Get or update prompt configuration"""
    global prompts_store
    
    if request.method == 'GET':
        return jsonify(prompts_store)
    
    elif request.method == 'PUT':
        data = request.json
        prompts_store.update(data)
        return jsonify(prompts_store)


def get_prompts_store():
    """Accessor for prompts store (Dependency Inversion)"""
    return prompts_store
