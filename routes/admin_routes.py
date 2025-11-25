"""
Admin Routes
Error logging dashboard and admin operations
"""

from flask import Blueprint, jsonify, render_template_string
from utils.error_logger import error_logger
from utils.error_handler import handle_errors

bp = Blueprint('admin', __name__, url_prefix='/api/admin')


@bp.route('/errors/recent', methods=['GET'])
@handle_errors
def get_recent_errors():
    """Get recent errors for monitoring"""
    errors = error_logger.get_recent_errors(limit=100)
    return jsonify({
        'success': True,
        'errors': errors,
        'count': len(errors)
    })


@bp.route('/errors/stats', methods=['GET'])
@handle_errors
def get_error_stats():
    """Get error statistics"""
    stats = error_logger.get_error_stats()
    return jsonify({
        'success': True,
        'stats': stats
    })


@bp.route('/errors/<int:error_id>/resolve', methods=['POST'])
@handle_errors
def resolve_error(error_id):
    """Mark an error as resolved"""
    from flask import request
    data = request.get_json() or {}
    notes = data.get('resolution_notes')
    
    success = error_logger.mark_resolved(error_id, notes)
    return jsonify({
        'success': success,
        'error_id': error_id
    })


@bp.route('/dashboard', methods=['GET'])
def error_dashboard():
    """Simple HTML dashboard for viewing errors"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>CerbroMail - Error Dashboard</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-50">
        <div class="container mx-auto p-8">
            <h1 class="text-3xl font-bold mb-8">📊 Error Dashboard</h1>
            
            <!-- Error Stats -->
            <div class="bg-white rounded-lg shadow p-6 mb-8">
                <h2 class="text-xl font-bold mb-4">Error Statistics</h2>
                <div id="stats" class="grid grid-cols-4 gap-4">
                    <div class="text-center">
                        <div class="text-3xl font-bold text-blue-600" id="total-errors">-</div>
                        <div class="text-sm text-gray-600">Total Errors</div>
                    </div>
                    <div class="text-center">
                        <div class="text-3xl font-bold text-red-600" id="unresolved">-</div>
                        <div class="text-sm text-gray-600">Unresolved</div>
                    </div>
                    <div class="text-center">
                        <div class="text-3xl font-bold text-green-600" id="resolved">-</div>
                        <div class="text-sm text-gray-600">Resolved</div>
                    </div>
                    <div class="text-center">
                        <div class="text-3xl font-bold text-purple-600" id="unique">-</div>
                        <div class="text-sm text-gray-600">Unique Types</div>
                    </div>
                </div>
            </div>
            
            <!-- Top Error Types -->
            <div class="bg-white rounded-lg shadow p-6 mb-8">
                <h2 class="text-xl font-bold mb-4">Top Error Types</h2>
                <div id="error-types" class="space-y-2">
                    <p class="text-gray-500">Loading...</p>
                </div>
            </div>
            
            <!-- Recent Errors -->
            <div class="bg-white rounded-lg shadow p-6">
                <h2 class="text-xl font-bold mb-4">Recent Errors</h2>
                <div id="recent-errors" class="space-y-4">
                    <p class="text-gray-500">Loading...</p>
                </div>
            </div>
        </div>
        
        <script>
            // Fetch and display error stats
            async function loadStats() {
                const res = await fetch('/api/admin/errors/stats');
                const data = await res.json();
                
                if (data.success) {
                    const stats = data.stats;
                    const totalCount = stats.reduce((sum, s) => sum + s.count, 0);
                    
                    document.getElementById('total-errors').textContent = totalCount;
                    document.getElementById('unique').textContent = stats.length;
                    
                    // Display top error types
                    const typesHtml = stats.slice(0, 10).map(s => `
                        <div class="flex justify-between items-center p-3 bg-gray-50 rounded">
                            <span class="font-mono text-sm">${s.error_code}</span>
                            <span class="font-bold text-blue-600">${s.count}x</span>
                        </div>
                    `).join('');
                    document.getElementById('error-types').innerHTML = typesHtml || '<p class="text-gray-500">No errors logged</p>';
                }
            }
            
            // Fetch and display recent errors
            async function loadRecentErrors() {
                const res = await fetch('/api/admin/errors/recent');
                const data = await res.json();
                
                if (data.success) {
                    const errors = data.errors;
                    
                    // Count resolved vs unresolved
                    const unresolved = errors.filter(e => !e.resolved).length;
                    const resolved = errors.filter(e => e.resolved).length;
                    document.getElementById('unresolved').textContent = unresolved;
                    document.getElementById('resolved').textContent = resolved;
                    
                    const errorsHtml = errors.slice(0, 50).map(e => `
                        <div class="border-l-4 ${e.resolved ? 'border-green-500' : 'border-red-500'} p-4 bg-gray-50 rounded">
                            <div class="flex justify-between items-start mb-2">
                                <div>
                                    <span class="font-mono text-xs bg-gray-200 px-2 py-1 rounded">${e.error_code}</span>
                                    <span class="text-xs text-gray-500 ml-2">${new Date(e.timestamp).toLocaleString()}</span>
                                    ${e.resolved ? '<span class="text-xs bg-green-100 text-green-700 px-2 py-1 rounded ml-2">✓ Resolved</span>' : ''}
                                </div>
                                <span class="text-xs font-mono text-gray-500">#${e.id}</span>
                            </div>
                            <div class="text-sm font-semibold mb-1">${e.error_type}</div>
                            <div class="text-sm text-gray-700">${e.message}</div>
                            ${e.endpoint ? `<div class="text-xs text-gray-500 mt-2">Endpoint: ${e.method} ${e.endpoint}</div>` : ''}
                            ${e.user_id ? `<div class="text-xs text-gray-500">User: ${e.user_id}</div>` : ''}
                        </div>
                    `).join('');
                    
                    document.getElementById('recent-errors').innerHTML = errorsHtml || '<p class="text-gray-500">No errors logged</p>';
                }
            }
            
            // Load data on page load
            loadStats();
            loadRecentErrors();
            
            // Refresh every 30 seconds
            setInterval(() => {
                loadStats();
                loadRecentErrors();
            }, 30000);
        </script>
    </body>
    </html>
    """
    return render_template_string(html)
