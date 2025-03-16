#!/usr/bin/env python3
import sys
import subprocess
from pathlib import Path

def main():
    """Run tests and start the application if tests pass."""
    # Get the project root directory
    project_root = Path(__file__).parent.parent.absolute()
    
    print("Running tests...")
    test_result = subprocess.run(
        [sys.executable, 'scripts/run_tests.py'],
        cwd=project_root
    )
    
    if test_result.returncode != 0:
        print("\nTests failed! Not starting the application.")
        return test_result.returncode
    
    print("\nTests passed! Starting the application...")
    
    # Start the Flask application
    app_result = subprocess.run(
        [sys.executable, 'src/app.py'],
        cwd=project_root
    )
    
    return app_result.returncode

if __name__ == '__main__':
    sys.exit(main()) 