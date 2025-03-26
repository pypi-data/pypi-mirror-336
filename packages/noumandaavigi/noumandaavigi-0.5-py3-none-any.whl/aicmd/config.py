import json
import importlib.resources
import os

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def load_settings():
    # Get the current working directory (relative path)
    current_dir = os.path.dirname(__file__)  # __file__ gives the current script path
    
    # Define the relative path to the settings.json file in the same directory
    settings_path = os.path.join(current_dir, 'settings.json')
    
    # Open the settings file and load its contents
    with open(settings_path, 'r') as settings_file:
        settings = json.load(settings_file)
    
    return settings

# Load settings
settings = load_settings()