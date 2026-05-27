"""Main Entry Point for VNIT Admission Chatbot"""

import argparse
from interfaces.cli import CLIInterface
from interfaces.admin import AdminDashboard

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='VNIT Nagpur Admission Chatbot'
    )
    
    parser.add_argument(
        '--mode',
        choices=['cli', 'admin'],
        default='cli',
        help='Run mode: cli (chatbot) or admin (dashboard)'
    )
    
    args = parser.parse_args()
    
    if args.mode == 'cli':
        print("Starting CLI Chatbot...")
        cli = CLIInterface()
        cli.run()
    
    elif args.mode == 'admin':
        print("Starting Admin Dashboard...")
        admin = AdminDashboard()
        admin.run()

if __name__ == '__main__':
    main()
