import sys
import os

# Get the absolute path of the codegens folder
module_folder = os.path.abspath(os.path.join(os.path.dirname(__file__)))

# Add it to sys.path
if module_folder not in sys.path:
    sys.path.append(module_folder)
    print("Added %s to sys.path" % module_folder)

    
from gs_web_server import main as server_main

def main():
    """Entry point for the lp mcp package"""
    print("Starting mcp server...")
    server_main()


if __name__ == "__main__":
    main()
