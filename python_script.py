#!/usr/bin/env python3
"""
Sample Python script that can be called from PHP
"""
import sys
import json

def main():
    # Get arguments passed from PHP
    args = sys.argv[1:]

    # Process the arguments
    result = {
        'script': 'python_script.py',
        'arguments_received': args,
        'message': 'Hello from Python!',
        'timestamp': '2024-01-01T00:00:00Z'  # You could use datetime here
    }

    # Output JSON that PHP can parse
    print(json.dumps(result))

if __name__ == '__main__':
    main()