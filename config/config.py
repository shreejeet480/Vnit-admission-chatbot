"""Configuration file for VNIT Admission Chatbot"""

import os
from datetime import datetime

# Environment
ENV = os.getenv('FLASK_ENV', 'development')
DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'

# Flask Config
FLASK_CONFIG = {
    'DEBUG': DEBUG,
    'JSON_SORT_KEYS': False,
    'JSONIFY_PRETTYPRINT_REGULAR': True,
}

# Database
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
DATABASE_PATH = os.path.join(BASE_DIR, 'data', 'chatbot.db')
SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE_PATH}'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# NLP Configuration
NLP_CONFIG = {
    'intent_threshold': 0.6,     # Confidence threshold for intent recognition
    'enable_stemming': True,
    'enable_lemmatization': True,
}

# Chatbot Behavior
CHATBOT_CONFIG = {
    'max_conversation_history': 50,
    'response_timeout': 10,
    'enable_learning': True,
    'log_conversations': True,
}

# Data Files
DATA_DIR = os.path.join(BASE_DIR, 'data')
ADMISSION_DATA_FILE = os.path.join(DATA_DIR, 'admission_data.json')
FAQ_FILE = os.path.join(DATA_DIR, 'faqs.json')
PROGRAMS_FILE = os.path.join(DATA_DIR, 'programs.json')

# API Configuration
API_CONFIG = {
    'enable_api': True,
    'api_prefix': '/api',
    'max_requests_per_minute': 60,
}

# VNIT Information
VNIT_INFO = {
    'name': 'Visvesvaraya National Institute of Technology',
    'short_name': 'VNIT',
    'location': 'Nagpur, Maharashtra, India',
    'website': 'https://vnit.ac.in',
    'admission_website': 'https://vnit.ac.in/section/academics/admission/',
    'email': 'admissions@vnit.ac.in',
    'phone': '+91-712-2801000',
}

# Programs Offered
PROGRAMS = {
    'undergraduate': ['B.Tech', 'B.Arch'],
    'postgraduate': ['M.Tech', 'M.Sc', 'MBA'],
    'doctorate': ['Ph.D'],
}
