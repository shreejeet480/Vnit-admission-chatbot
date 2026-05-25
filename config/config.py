import os
from datetime import datetime

# Environment
ENV = os.getenv('FLASK_ENV', 'development')
DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'

# Flask Config
FLASK_CONFIG = {
    'DEBUG': DEBUG,
    'JSON_SORT_KEYS': False,
}

# Database
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
DATABASE_PATH = os.path.join(BASE_DIR, 'data', 'chatbot.db')
SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE_PATH}'

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

# Data Files
DATA_DIR = os.path.join(BASE_DIR, 'data')
ADMISSION_DATA_FILE = os.path.join(DATA_DIR, 'admission_data.json')
FAQ_FILE = os.path.join(DATA_DIR, 'faqs.json')
PROGRAMS_FILE = os.path.join(DATA_DIR, 'programs.json')
