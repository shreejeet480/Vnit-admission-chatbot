"""Utility Functions"""

import re
from typing import List

def clean_text(text: str) -> str:
    """
    Clean and normalize text
    
    Args:
        text: Input text
        
    Returns:
        Cleaned text
    """
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_program_name(text: str) -> str:
    """
    Extract program name from text
    
    Args:
        text: Input text
        
    Returns:
        Program name if found, empty string otherwise
    """
    programs = ['B.Tech', 'B.Arch', 'M.Tech', 'M.Sc', 'MBA', 'Ph.D']
    text_lower = text.lower()

    for program in programs:
        if program.lower() in text_lower:
            return program

    return ""

def tokenize(text: str) -> List[str]:
    """
    Tokenize text into words
    
    Args:
        text: Input text
        
    Returns:
        List of tokens
    """
    text = text.lower()
    # Remove special characters
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text.split()
