"""Tests for main chatbot module"""

import pytest
from src.chatbot import VNITChatbot

class TestVNITChatbot:
    """Test cases for VNITChatbot class"""

    def setup_method(self):
        """Setup before each test"""
        self.chatbot = VNITChatbot({'log_conversations': False})
        self.chatbot.set_user_id('test_user')

    def test_chatbot_initialization(self):
        """Test chatbot initialization"""
        assert self.chatbot is not None
        assert self.chatbot.user_id == 'test_user'

    def test_process_message(self):
        """Test message processing"""
        response = self.chatbot.process_message("Hello")
        assert response['success'] == True
        assert 'response' in response

    def test_program_query(self):
        """Test program information query"""
        response = self.chatbot.process_message("Tell me about B.Tech")
        assert response['success'] == True
        assert response['response'] != ''
