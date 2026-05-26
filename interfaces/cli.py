"""Command-Line Interface (CLI) for the Chatbot"""

from src.chatbot import VNITChatbot
from colorama import Fore, Style, init

# Initialize colorama for colored terminal output
init(autoreset=True)

class CLIInterface:
    """Command-line interface for chatbot"""

    def __init__(self):
        """Initialize CLI interface"""
        self.chatbot = VNITChatbot({'log_conversations': True})
        self.user_name = None
        self.user_id = None

    def get_user_name(self):
        """Get user's name for personalized greeting"""
        while True:
            name = input(f"{Fore.CYAN}👤 Please enter your name: {Style.RESET_ALL}").strip()
            if name and len(name) >= 2:
                self.user_name = name
                self.user_id = f"cli_user_{name.lower().replace(' ', '_')}"
                self.chatbot.set_user_id(self.user_id)
                return name
            else:
                print(f"{Fore.YELLOW}⚠️  Please enter a valid name (at least 2 characters){Style.RESET_ALL}\n")

    def display_welcome(self):
        """Display personalized welcome message"""
        print(f"\n{Fore.CYAN}")
        print("="*60)
        print("  🎓 VNIT NAGPUR ADMISSION CHATBOT")
        print("="*60)
        print(f"{Style.RESET_ALL}")
        print(f"\n👋 Welcome, {Fore.GREEN}{self.user_name}{Style.RESET_ALL}!")
        print("I'm here to help you with VNIT admission information.")
        print("📝 Type 'help' for common questions, 'exit' to quit.\n")

    def display_help(self):
        """Display help information"""
        print(f"\n{Fore.YELLOW}❓ Common Questions:{Style.RESET_ALL}")
        print("• What programs does VNIT offer?")
        print("• Tell me about B.Tech")
        print("• Tell me about M.Tech")
        print("• Tell me about M.Sc")
        print("• What is the eligibility for B.Tech?")
        print("• How is the admission process?")
        print("• What about placement statistics?")
        print("• What is the fee structure?")
        print("• How does JoSAA counseling work?")
        print("")

    def run(self):
        """Run the CLI chatbot in an interactive loop"""
        # Get user name
        self.get_user_name()
        
        # Display welcome
        self.display_welcome()

        while True:
            try:
                # Get user input with personalized prompt
                user_input = input(f"{Fore.GREEN}{self.user_name}: {Style.RESET_ALL}").strip()

                if not user_input:
                    continue

                # Handle exit command
                if user_input.lower() == 'exit':
                    print(f"\n{Fore.YELLOW}Thank you for using VNIT Admission Chatbot! See You Around 👋{Style.RESET_ALL}\n")
                    break

                # Display help
                if user_input.lower() == 'help':
                    self.display_help()
                    continue

                # Process user message
                result = self.chatbot.process_message(user_input)

                if result['success']:
                    # Display bot response
                    print(f"\n{Fore.CYAN}🤖 Bot: {Style.RESET_ALL}{result['response']}\n")

                    # Display suggestions
                    if result.get('suggestions'):
                        print(f"{Fore.YELLOW}💡 Suggested Questions:{Style.RESET_ALL}")
                        for i, suggestion in enumerate(result['suggestions'], 1):
                            print(f"  {i}. {suggestion}")
                        print()
                else:
                    print(f"{Fore.RED}❌ Error: {result['response']}{Style.RESET_ALL}\n")

            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Thank you for using VNIT Admission Chatbot! See You Around 👋{Style.RESET_ALL}\n")
                break
            except Exception as e:
                print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
