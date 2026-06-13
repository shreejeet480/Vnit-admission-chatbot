"""Flask Web Application Interface"""

import os
import sys

# Allow running this file directly: add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from flask import Flask, render_template, request, jsonify
from src.chatbot import VNITChatbot
import uuid

app = Flask(
    __name__,
    template_folder=os.path.join(PROJECT_ROOT, "templates"),
    static_folder=os.path.join(PROJECT_ROOT, "static"),
)
app.config['JSON_SORT_KEYS'] = False

# Dictionary to store chatbots per session
chatbots = {}

def get_chatbot(session_id):
    """Get or create chatbot for session"""
    if session_id not in chatbots:
        chatbots[session_id] = VNITChatbot({'log_conversations': True})
        chatbots[session_id].set_user_id(session_id)
    return chatbots[session_id]

@app.route('/')
def index():
    """Render main chatbot page"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Chat API endpoint
    
    POST body:
        message (str): User message
        session_id (str, optional): Session identifier
    """
    try:
        data = request.json
        message = data.get('message', '').strip()
        session_id = data.get('session_id', str(uuid.uuid4()))

        if not message:
            return jsonify({'error': 'Empty message'}), 400

        chatbot = get_chatbot(session_id)
        result = chatbot.process_message(message)

        return jsonify({
            'session_id': session_id,
            'response': result['response'],
            'intent': result.get('intent', 'unknown'),
            'intent_source': result.get('intent_source', 'rules'),
            'confidence': result.get('confidence', 0),
            'suggestions': result.get('suggestions', [])
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/programs', methods=['GET'])
def get_programs():
    """Get all programs"""
    try:
        session_id = request.args.get('session_id', str(uuid.uuid4()))
        chatbot = get_chatbot(session_id)
        programs = chatbot.get_all_programs()
        return jsonify(programs)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/faq', methods=['GET'])
def get_faq():
    """Get FAQs"""
    try:
        session_id = request.args.get('session_id', str(uuid.uuid4()))
        limit = request.args.get('limit', 10, type=int)
        chatbot = get_chatbot(session_id)
        faqs = chatbot.get_faq(limit)
        return jsonify({'faqs': faqs})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
