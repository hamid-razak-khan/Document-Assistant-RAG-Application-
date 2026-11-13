#!/usr/bin/env python
"""
Script to start the Django development server with proper settings
to avoid connection timeout issues during file uploads.
"""

import os
import sys
import subprocess

def start_server():
    # Change to the backend directory
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    if not os.path.exists(backend_dir):
        print("Error: Backend directory not found")
        return
    
    # Start the Django development server with proper binding
    # Using 0.0.0.0:8000 to ensure it's accessible
    cmd = [
        sys.executable, 
        'manage.py', 
        'runserver', 
        '0.0.0.0:8000',
        '--noreload'  # Disable auto-reload to prevent issues with file uploads
    ]
    
    print("Starting Django development server...")
    print("Command:", ' '.join(cmd))
    
    try:
        # Change to backend directory and run the command
        result = subprocess.run(cmd, cwd=backend_dir)
        if result.returncode == 0:
            print("Server started successfully")
        else:
            print(f"Server failed to start with return code {result.returncode}")
    except Exception as e:
        print(f"Error starting server: {e}")

if __name__ == "__main__":
    start_server()