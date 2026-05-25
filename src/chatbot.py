import json
from typing import Dict, List
from .intent_recognition import IntentRecognizer
from .response_generator import ResponseGenerator

class VNITChatbot:
    def __init__(self):
        self.intent_recognizer = IntentRecognizer()
        self.response_generator = ResponseGenerator()
        self.conversation_history = []

    def process_message(self, user_message: str) -> Dict:
        """Process user message and generate response"""
        # Recognize intent
        intent_result = self.intent_recognizer.recognize(user_message)
        intent = intent_result.get('intent', 'general')
        
        # Generate response
        response = self.response_generator.generate(user_message, intent)
        
        return {
            'response': response,
            'intent': intent
        }
