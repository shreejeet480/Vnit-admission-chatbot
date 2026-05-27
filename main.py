#!/usr/bin/env python3
"""Main Entry Point for VNIT Admission Chatbot"""

import argparse
import sys
from interfaces.cli import CLIInterface
from interfaces.web_app import app

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='🎓 VNIT Nagpur Admission Chatbot'
    )
    parser.add_argument(
        '--mode',
        choices=['cli', 'web'],
        default='cli',
        help='Interface mode (default: cli)'
    )
    parser.add_argument(
        '--host',
        default='localhost',
        help='Host for web mode (default: localhost)'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=5000,
        help='Port for web mode (default: 5000)'
    )

    args = parser.parse_args()

    if args.mode == 'cli':
        print("Starting CLI Chatbot...")
        cli = CLIInterface()
        cli.run()

    elif args.mode == 'web':
        print(f"Starting Web Chatbot on http://{args.host}:{args.port}")
        print("Open your browser and visit: http://localhost:5000")
        app.run(host=args.host, port=args.port, debug=True)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nShutting down...")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
