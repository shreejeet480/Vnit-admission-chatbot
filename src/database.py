"""Database Module - Handles all database operations"""

import sqlite3
from datetime import datetime
from typing import List, Dict
from config.config import DATABASE_PATH

class Database:
    """Handle SQLite database operations"""

    def __init__(self, db_path: str = DATABASE_PATH):
        """Initialize database"""
        self.db_path = db_path
        self._initialize_db()

    def _initialize_db(self):
        """Initialize database tables"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Create users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT UNIQUE,
                    user_name TEXT NOT NULL,
                    first_interaction DATETIME DEFAULT CURRENT_TIMESTAMP,
                    last_interaction DATETIME,
                    total_queries INTEGER DEFAULT 0
                )
            ''')

            # Create conversations table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    user_name TEXT NOT NULL,
                    user_message TEXT NOT NULL,
                    bot_response TEXT NOT NULL,
                    intent TEXT,
                    program TEXT,
                    specialization TEXT,
                    confidence REAL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES users(user_id)
                )
            ''')

            # Create analytics table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS analytics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date DATE DEFAULT CURRENT_DATE,
                    total_users INTEGER DEFAULT 0,
                    total_queries INTEGER DEFAULT 0,
                    most_asked_intent TEXT,
                    most_asked_program TEXT
                )
            ''')

            conn.commit()
            conn.close()
            print("✅ Database initialized successfully")
        except sqlite3.Error as e:
            print(f"Database initialization error: {str(e)}")

    def register_user(self, user_id: str, user_name: str):
        """Register a new user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                INSERT OR IGNORE INTO users (user_id, user_name, last_interaction)
                VALUES (?, ?, ?)
            ''', (user_id, user_name, datetime.now()))

            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print(f"Error registering user: {str(e)}")

    def log_conversation(self, user_id: str, user_name: str, user_message: str,
                        bot_response: str, intent: str = None, program: str = None,
                        specialization: str = None, confidence: float = 0):
        """
        Log a conversation
        
        Args:
            user_id: User identifier
            user_name: User's name
            user_message: User's input
            bot_response: Bot's response
            intent: Recognized intent
            program: Program mentioned
            specialization: Specialization mentioned
            confidence: Confidence score
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Insert conversation
            cursor.execute('''
                INSERT INTO conversations
                (user_id, user_name, user_message, bot_response, intent, program, specialization, confidence)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, user_name, user_message, bot_response, intent, program, specialization, confidence))

            # Update user's last interaction and query count
            cursor.execute('''
                UPDATE users
                SET last_interaction = ?, total_queries = total_queries + 1
                WHERE user_id = ?
            ''', (datetime.now(), user_id))

            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print(f"Error logging conversation: {str(e)}")

    def get_user_conversations(self, user_id: str, limit: int = 50) -> List[Dict]:
        """Get conversations for a user"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute('''
                SELECT * FROM conversations
                WHERE user_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (user_id, limit))

            rows = cursor.fetchall()
            conversations = [dict(row) for row in rows]
            conn.close()

            return conversations
        except sqlite3.Error as e:
            print(f"Error retrieving conversations: {str(e)}")
            return []

    def get_all_users(self) -> List[Dict]:
        """Get all registered users with stats"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute('''
                SELECT user_id, user_name, first_interaction, last_interaction, total_queries
                FROM users
                ORDER BY last_interaction DESC
            ''')

            rows = cursor.fetchall()
            users = [dict(row) for row in rows]
            conn.close()

            return users
        except sqlite3.Error as e:
            print(f"Error retrieving users: {str(e)}")
            return []

    def get_conversation_stats(self, user_id: str) -> Dict:
        """Get conversation statistics for a user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Total conversations
            cursor.execute('SELECT COUNT(*) FROM conversations WHERE user_id = ?', (user_id,))
            total = cursor.fetchone()[0]

            # Most asked intent
            cursor.execute('''
                SELECT intent, COUNT(*) as count
                FROM conversations
                WHERE user_id = ?
                GROUP BY intent
                ORDER BY count DESC
                LIMIT 1
            ''', (user_id,))
            most_intent = cursor.fetchone()

            # Most asked program
            cursor.execute('''
                SELECT program, COUNT(*) as count
                FROM conversations
                WHERE user_id = ? AND program IS NOT NULL
                GROUP BY program
                ORDER BY count DESC
                LIMIT 1
            ''', (user_id,))
            most_program = cursor.fetchone()

            conn.close()

            return {
                'total_conversations': total,
                'most_asked_intent': most_intent[0] if most_intent else None,
                'most_asked_program': most_program[0] if most_program else None
            }
        except sqlite3.Error as e:
            print(f"Error getting stats: {str(e)}")
            return {}

    def get_user_interaction_report(self) -> List[Dict]:
        """Get report of all users and their interactions"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute('''
                SELECT 
                    u.user_name,
                    u.first_interaction,
                    u.last_interaction,
                    u.total_queries,
                    COUNT(DISTINCT c.id) as total_conversations
                FROM users u
                LEFT JOIN conversations c ON u.user_id = c.user_id
                GROUP BY u.user_id
                ORDER BY u.last_interaction DESC
            ''')

            rows = cursor.fetchall()
            report = [dict(row) for row in rows]
            conn.close()

            return report
        except sqlite3.Error as e:
            print(f"Error getting interaction report: {str(e)}")
            return []
