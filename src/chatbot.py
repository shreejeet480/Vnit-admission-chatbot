"""Main Chatbot Class - Orchestrates all chatbot functionality"""

import json
import logging
from datetime import datetime
from typing import Dict, List
from .intent_recognition import IntentRecognizer
from .ml_intent_classifier import MLIntentClassifier
from .response_generator import ResponseGenerator
from .database import Database

logger = logging.getLogger(__name__)

class VNITChatbot:
    """Main chatbot class for handling admission queries"""

    def __init__(self, config: Dict = None):
        """Initialize the chatbot"""
        self.config = config or {}
        self.intent_recognizer = IntentRecognizer()
        self.ml_classifier = MLIntentClassifier()
        self.response_generator = ResponseGenerator()
        self.db = Database()
        self.conversation_history = []
        self.user_id = None
        self.user_name = None

    def set_user(self, user_id: str, user_name: str):
        """Set user ID and name"""
        self.user_id = user_id
        self.user_name = user_name
        # Register user in database
        self.db.register_user(user_id, user_name)

    def set_user_id(self, user_id: str):
        """Set the user ID (for backward compatibility)"""
        self.user_id = user_id

    def process_message(self, user_message: str) -> Dict:
        """Process user message and generate response"""
        try:
            # Add user message to conversation history
            self.conversation_history.append({
                'timestamp': datetime.now().isoformat(),
                'role': 'user',
                'content': user_message
            })

            # --- HYBRID INTENT RECOGNITION ---
            # 1) Try the ML classifier (TF-IDF + Logistic Regression)
            ml_result = self.ml_classifier.predict(user_message)

            # 2) Always run rule-based recognizer too (it extracts
            #    program/specialization entities the ML model doesn't)
            rule_result = self.intent_recognizer.recognize(user_message)
            program = rule_result.get('program')
            specialization = rule_result.get('specialization')

            # 3) Pick the source: ML if confident, else regex fallback
            if ml_result['is_confident']:
                intent = ml_result['intent']
                confidence = ml_result['confidence']
                intent_source = 'ml'
            else:
                intent = rule_result.get('intent', 'general')
                confidence = rule_result.get('confidence', 0)
                intent_source = 'rules'

            # Generate response using ResponseGenerator
            response = self.response_generator.generate(
                user_message=user_message,
                intent=intent,
                confidence=confidence,
                program=program,
                specialization=specialization,
                conversation_history=self.conversation_history
            )

            # Add bot response to conversation history
            self.conversation_history.append({
                'timestamp': datetime.now().isoformat(),
                'role': 'bot',
                'content': response['text']
            })

            # Log conversation to database if enabled
            if self.config.get('log_conversations', True) and self.user_id:
                self.db.log_conversation(
                    user_id=self.user_id,
                    user_name=self.user_name or 'Unknown',
                    user_message=user_message,
                    bot_response=response['text'],
                    intent=intent,
                    program=program,
                    specialization=specialization,
                    confidence=confidence
                )

            return {
                'success': True,
                'response': response['text'],
                'intent': intent,
                'program': program,
                'specialization': specialization,
                'confidence': confidence,
                'intent_source': intent_source,
                'suggestions': response.get('suggestions', [])
            }

        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            return {
                'success': False,
                'response': "I apologize, but I encountered an error processing your request. Please try again.",
                'error': str(e)
            }

    def get_conversation_history(self, limit: int = None) -> List[Dict]:
        """Get conversation history"""
        if limit:
            return self.conversation_history[-limit:]
        return self.conversation_history

    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []

    def get_user_stats(self) -> Dict:
        """Get user conversation statistics"""
        if self.user_id:
            return self.db.get_conversation_stats(self.user_id)
        return {}

    def get_program_info(self, program_name: str) -> Dict:
        """Get information about a specific program"""
        return self.response_generator.get_program_info(program_name)

    def get_eligibility(self, program_name: str) -> Dict:
        """Get eligibility criteria for a program"""
        return self.response_generator.get_eligibility(program_name)

    def get_faq(self, limit: int = 10) -> List[Dict]:
        """Get frequently asked questions"""
        return self.response_generator.get_faq(limit)

    def get_all_programs(self) -> Dict:
        """Get information about all programs"""
        return self.response_generator.get_all_programs()
