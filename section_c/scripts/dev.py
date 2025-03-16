#!/usr/bin/env python3
import os
import sys
from pathlib import Path
from subprocess import run
from dotenv import load_dotenv

def main():
    """Run the application in development mode with hot reload."""
    # Get the project root directory
    project_root = Path(__file__).parent.parent.absolute()
    
    # Load development environment variables
    load_dotenv(project_root / '.env.development')
    
    # Set up environment for Flask development
    os.environ['PYTHONPATH'] = str(project_root)
    
    print("Starting development server with hot reload...")
    
    # Run Flask development server
    result = run([
        'flask',
        'run',
        '--host=0.0.0.0',
        '--port=5000',
        '--reload',
        '--debug'
    ], cwd=project_root)
    
    return result.returncode

if __name__ == '__main__':
    sys.exit(main()) 