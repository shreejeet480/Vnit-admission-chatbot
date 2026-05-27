"""Intent Recognition Module - Identifies what the user is asking about"""

import re
from typing import Dict

class IntentRecognizer:
    """Recognize user intent from messages"""

    def __init__(self):
        """Initialize intent recognizer with intent patterns and keywords"""
        self.intents = {
            'program_info': {
                'keywords': ['program', 'course', 'specialization', 'branch', 'about', 'details', 'tell', 'information'],
                'patterns': [
                    r'tell me about.*program',
                    r'information about.*course',
                    r'what.*specializations',
                    r'available.*branches',
                    r'tell.*about.*(?:b\.tech|btech|m\.tech|mtech|m\.sc|msc)',
                    r'(?:b\.tech|btech|m\.tech|mtech|m\.sc|msc).*(?:computer|cse|ece|electrical|mechanical|civil|chemical)',
                    r'(?:computer science|electronics|electrical|mechanical|civil|chemical).*(?:b\.tech|btech|m\.tech|mtech)'
                ]
            },
            'eligibility': {
                'keywords': ['eligible', 'eligibility', 'qualify', 'requirements', 'criteria', 'qualification'],
                'patterns': [
                    r'eligibility.*for',
                    r'can i apply',
                    r'requirements.*for',
                    r'qualify.*for',
                    r'am i eligible'
                ]
            },
            'admission_process': {
                'keywords': ['admission', 'apply', 'process', 'how', 'steps', 'procedure'],
                'patterns': [
                    r'how.*admission',
                    r'admission.*process',
                    r'steps.*apply',
                    r'how.*apply.*to'
                ]
            },
            'entrance_exam': {
                'keywords': ['exam', 'jee', 'gate', 'jam', 'entrance', 'test', 'nata'],
                'patterns': [
                    r'what.*exam',
                    r'entrance.*exam',
                    r'required.*exam',
                    r'jee|gate|jam|nata'
                ]
            },
            'documents': {
                'keywords': ['document', 'certificate', 'mark sheet', 'require', 'papers'],
                'patterns': [
                    r'what.*documents',
                    r'required.*documents',
                    r'documents.*needed'
                ]
            },
            'fees': {
                'keywords': ['fee', 'cost', 'price', 'expense', 'tuition', 'afford', 'payment', 'last date', 'deadline'],
                'patterns': [
                    r'fee.*structure',
                    r'how.*much',
                    r'cost.*of',
                    r'tuition.*fee',
                    r'payment.*date',
                    r'last.*date',
                    r'deadline.*fee'
                ]
            },
            'placement': {
                'keywords': ['placement', 'job', 'salary', 'package', 'recruit', 'career'],
                'patterns': [
                    r'placement.*rate',
                    r'average.*package',
                    r'job.*prospect',
                    r'salary.*package'
                ]
            },
            'counseling': {
                'keywords': ['counseling', 'josaa', 'ccmt', 'seat', 'allot', 'allocation'],
                'patterns': [
                    r'counseling.*process',
                    r'josaa|ccmt|ccmn',
                    r'seat.*alloc',
                    r'how.*counseling'
                ]
            },
            'general': {
                'keywords': ['hello', 'hi', 'help', 'info', 'tell', 'what'],
                'patterns': [r'hello|hi|help|what|tell']
            }
        }
        
        # Program and specialization keywords
        self.programs = ['b.tech', 'btech', 'b tech', 'm.tech', 'mtech', 'm tech', 'm.sc', 'msc', 'm sc', 'b.arch', 'barch', 'mba', 'phd']
        self.specializations = {
            'cse': ['computer', 'cse', 'cs', 'software'],
            'ece': ['electronics', 'ece', 'communication'],
            'ee': ['electrical', 'ee', 'power'],
            'me': ['mechanical', 'me', 'thermal'],
            'ce': ['civil', 'ce', 'structural'],
            'che': ['chemical', 'che', 'chemistry']
        }

    def recognize(self, message: str) -> Dict:
        """
        Recognize intent from user message
        
        Returns:
            Dictionary containing:
            - intent: Identified intent type
            - confidence: Confidence score (0-1)
            - program: Program if identified
            - specialization: Specialization if identified
            - all_scores: Scores for all intents
        """
        message_lower = message.lower()
        intent_scores = {}
        
        # Extract program and specialization
        program = self._extract_program(message_lower)
        specialization = self._extract_specialization(message_lower)

        # Check pattern matches
        for intent_name, intent_data in self.intents.items():
            score = 0

            # Check patterns (higher weight)
            for pattern in intent_data.get('patterns', []):
                if re.search(pattern, message_lower, re.IGNORECASE):
                    score += 0.5

            # Check keywords (lower weight)
            for keyword in intent_data.get('keywords', []):
                if keyword in message_lower:
                    score += 0.1

            if score > 0:
                intent_scores[intent_name] = min(score, 1.0)

        # Get best match
        if intent_scores:
            best_intent = max(intent_scores, key=intent_scores.get)
            confidence = intent_scores[best_intent]
        else:
            best_intent = 'general'
            confidence = 0.5

        return {
            'intent': best_intent,
            'confidence': confidence,
            'program': program,
            'specialization': specialization,
            'all_scores': intent_scores
        }
    
    def _extract_program(self, message: str) -> str:
        """Extract program name from message"""
        for program in self.programs:
            if program in message:
                if 'b.tech' in message or 'btech' in message or 'b tech' in message:
                    return 'b_tech'
                elif 'm.tech' in message or 'mtech' in message or 'm tech' in message:
                    return 'm_tech'
                elif 'm.sc' in message or 'msc' in message or 'm sc' in message:
                    return 'm_sc'
                elif 'b.arch' in message or 'barch' in message:
                    return 'b_arch'
                elif 'mba' in message:
                    return 'mba'
                elif 'phd' in message or 'ph.d' in message:
                    return 'phd'
        return None
    
    def _extract_specialization(self, message: str) -> str:
        """Extract specialization from message"""
        for spec_code, keywords in self.specializations.items():
            for keyword in keywords:
                if keyword in message:
                    return spec_code
        return None
