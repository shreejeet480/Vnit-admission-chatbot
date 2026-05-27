"""Admin Dashboard - View chatbot analytics and user data"""

import sqlite3
from datetime import datetime
from colorama import Fore, Style, init
from tabulate import tabulate

init(autoreset=True)

class AdminDashboard:
    """Admin interface for viewing analytics and user data"""

    def __init__(self, db_path: str = 'data/chatbot.db'):
        """Initialize admin dashboard"""
        self.db_path = db_path
        self.conn = None
        self.cursor = None

    def connect(self):
        """Connect to database"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
            print(f"{Fore.GREEN}✅ Connected to database{Style.RESET_ALL}\n")
        except sqlite3.Error as e:
            print(f"{Fore.RED}❌ Database connection error: {str(e)}{Style.RESET_ALL}")

    def disconnect(self):
        """Disconnect from database"""
        if self.conn:
            self.conn.close()

    def display_header(self, title: str):
        """Display section header"""
        print(f"\n{Fore.CYAN}")
        print("=" * 70)
        print(f"  {title}")
        print("=" * 70)
        print(f"{Style.RESET_ALL}\n")

    def view_all_users(self):
        """View all registered users"""
        self.display_header("👥 ALL USERS")
        
        try:
            self.cursor.execute('''
                SELECT 
                    user_name,
                    first_interaction,
                    last_interaction,
                    total_queries
                FROM users
                ORDER BY last_interaction DESC
            ''')
            
            rows = self.cursor.fetchall()
            
            if not rows:
                print(f"{Fore.YELLOW}No users found{Style.RESET_ALL}\n")
                return
            
            table_data = [
                [
                    row['user_name'],
                    row['first_interaction'][:19],
                    row['last_interaction'][:19],
                    row['total_queries']
                ]
                for row in rows
            ]
            
            print(tabulate(
                table_data,
                headers=['User Name', 'First Interaction', 'Last Interaction', 'Total Queries'],
                tablefmt='grid'
            ))
            print(f"\n{Fore.GREEN}Total Users: {len(rows)}{Style.RESET_ALL}\n")
            
        except sqlite3.Error as e:
            print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}\n")

    def view_user_conversations(self, user_name: str):
        """View all conversations for a specific user"""
        self.display_header(f"💬 CONVERSATIONS - {user_name.upper()}")
        
        try:
            self.cursor.execute('''
                SELECT 
                    timestamp,
                    user_message,
                    intent,
                    program,
                    specialization
                FROM conversations
                WHERE user_name = ?
                ORDER BY timestamp DESC
            ''', (user_name,))
            
            rows = self.cursor.fetchall()
            
            if not rows:
                print(f"{Fore.YELLOW}No conversations found for {user_name}{Style.RESET_ALL}\n")
                return
            
            for i, row in enumerate(rows, 1):
                print(f"{Fore.YELLOW}Query #{i}{Style.RESET_ALL}")
                print(f"  📅 Time: {row['timestamp'][:19]}")
                print(f"  ❓ Question: {row['user_message']}")
                print(f"  🎯 Intent: {row['intent']}")
                if row['program']:
                    print(f"  📚 Program: {row['program']}")
                if row['specialization']:
                    print(f"  🏢 Specialization: {row['specialization']}")
                print()
            
            print(f"{Fore.GREEN}Total Conversations: {len(rows)}{Style.RESET_ALL}\n")
            
        except sqlite3.Error as e:
            print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}\n")

    def view_analytics(self):
        """View overall analytics"""
        self.display_header("📊 OVERALL ANALYTICS")
        
        try:
            # Total users
            self.cursor.execute('SELECT COUNT(*) as count FROM users')
            total_users = self.cursor.fetchone()['count']
            
            # Total conversations
            self.cursor.execute('SELECT COUNT(*) as count FROM conversations')
            total_conversations = self.cursor.fetchone()['count']
            
            # Most asked intent
            self.cursor.execute('''
                SELECT intent, COUNT(*) as count
                FROM conversations
                WHERE intent IS NOT NULL
                GROUP BY intent
                ORDER BY count DESC
                LIMIT 5
            ''')
            top_intents = self.cursor.fetchall()
            
            # Most asked program
            self.cursor.execute('''
                SELECT program, COUNT(*) as count
                FROM conversations
                WHERE program IS NOT NULL
                GROUP BY program
                ORDER BY count DESC
                LIMIT 5
            ''')
            top_programs = self.cursor.fetchall()
            
            # Most asked specialization
            self.cursor.execute('''
                SELECT specialization, COUNT(*) as count
                FROM conversations
                WHERE specialization IS NOT NULL
                GROUP BY specialization
                ORDER BY count DESC
                LIMIT 5
            ''')
            top_specs = self.cursor.fetchall()
            
            # Display stats
            print(f"{Fore.GREEN}📈 Key Metrics:{Style.RESET_ALL}")
            print(f"  • Total Users: {total_users}")
            print(f"  • Total Conversations: {total_conversations}")
            if total_users > 0:
                print(f"  • Avg Questions per User: {total_conversations / total_users:.2f}")
            
            print(f"\n{Fore.CYAN}🎯 Top 5 Intents Asked:{Style.RESET_ALL}")
            for i, row in enumerate(top_intents, 1):
                print(f"  {i}. {row['intent']}: {row['count']} queries")
            
            print(f"\n{Fore.CYAN}📚 Top 5 Programs Asked:{Style.RESET_ALL}")
            for i, row in enumerate(top_programs, 1):
                program_name = row['program'] or 'General'
                print(f"  {i}. {program_name}: {row['count']} queries")
            
            print(f"\n{Fore.CYAN}🏢 Top 5 Specializations Asked:{Style.RESET_ALL}")
            for i, row in enumerate(top_specs, 1):
                spec_name = row['specialization'] or 'Not Specified'
                print(f"  {i}. {spec_name}: {row['count']} queries")
            
            print()
            
        except sqlite3.Error as e:
            print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}\n")

    def view_user_stats(self, user_name: str):
        """View detailed statistics for a user"""
        self.display_header(f"📊 USER STATISTICS - {user_name.upper()}")
        
        try:
            # User info
            self.cursor.execute('''
                SELECT * FROM users WHERE user_name = ?
            ''', (user_name,))
            user = self.cursor.fetchone()
            
            if not user:
                print(f"{Fore.YELLOW}User not found: {user_name}{Style.RESET_ALL}\n")
                return
            
            print(f"{Fore.GREEN}Basic Info:{Style.RESET_ALL}")
            print(f"  • Name: {user['user_name']}")
            print(f"  • First Interaction: {user['first_interaction']}")
            print(f"  • Last Interaction: {user['last_interaction']}")
            print(f"  • Total Queries: {user['total_queries']}")
            
            # Intent distribution
            self.cursor.execute('''
                SELECT intent, COUNT(*) as count
                FROM conversations
                WHERE user_name = ?
                GROUP BY intent
                ORDER BY count DESC
            ''', (user_name,))
            intents = self.cursor.fetchall()
            
            print(f"\n{Fore.CYAN}Intent Distribution:{Style.RESET_ALL}")
            for row in intents:
                print(f"  • {row['intent']}: {row['count']}")
            
            # Program interest
            self.cursor.execute('''
                SELECT program, COUNT(*) as count
                FROM conversations
                WHERE user_name = ? AND program IS NOT NULL
                GROUP BY program
                ORDER BY count DESC
            ''', (user_name,))
            programs = self.cursor.fetchall()
            
            print(f"\n{Fore.CYAN}Programs of Interest:{Style.RESET_ALL}")
            for row in programs:
                print(f"  • {row['program']}: {row['count']} queries")
            
            # Specialization interest
            self.cursor.execute('''
                SELECT specialization, COUNT(*) as count
                FROM conversations
                WHERE user_name = ? AND specialization IS NOT NULL
                GROUP BY specialization
                ORDER BY count DESC
            ''', (user_name,))
            specs = self.cursor.fetchall()
            
            print(f"\n{Fore.CYAN}Specializations of Interest:{Style.RESET_ALL}")
            for row in specs:
                print(f"  • {row['specialization']}: {row['count']} queries")
            
            print()
            
        except sqlite3.Error as e:
            print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}\n")

    def run(self):
        """Run interactive admin dashboard"""
        self.connect()
        
        print(f"\n{Fore.CYAN}")
        print("=" * 70)
        print("  🎓 VNIT ADMISSION CHATBOT - ADMIN DASHBOARD")
        print("=" * 70)
        print(f"{Style.RESET_ALL}\n")
        
        while True:
            try:
                print(f"{Fore.YELLOW}Options:{Style.RESET_ALL}")
                print("  1. View all users")
                print("  2. View overall analytics")
                print("  3. View user conversations")
                print("  4. View user statistics")
                print("  5. Exit")
                print()
                
                choice = input(f"{Fore.GREEN}Enter choice (1-5): {Style.RESET_ALL}").strip()
                
                if choice == '1':
                    self.view_all_users()
                
                elif choice == '2':
                    self.view_analytics()
                
                elif choice == '3':
                    user_name = input(f"{Fore.GREEN}Enter user name: {Style.RESET_ALL}").strip()
                    if user_name:
                        self.view_user_conversations(user_name)
                
                elif choice == '4':
                    user_name = input(f"{Fore.GREEN}Enter user name: {Style.RESET_ALL}").strip()
                    if user_name:
                        self.view_user_stats(user_name)
                
                elif choice == '5':
                    print(f"{Fore.YELLOW}Thank you for using Admin Dashboard! Goodbye 👋{Style.RESET_ALL}\n")
                    break
                
                else:
                    print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}\n")
                    
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Exiting... Goodbye 👋{Style.RESET_ALL}\n")
                break
            except Exception as e:
                print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}\n")
        
        self.disconnect()
