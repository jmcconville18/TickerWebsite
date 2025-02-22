import sys
import os
import site
import logging

# Set up logging
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

def log_and_raise(exception, message):
    logging.error(message)
    raise exception(message)

# Path to the virtual environment
VENV_PATH = '/home/joe/Documents/TickerWebsite/venv'

# Check if the virtual environment directory exists
if not os.path.exists(VENV_PATH):
    log_and_raise(FileNotFoundError, f"Virtual environment path not found: {VENV_PATH}")

# Add the site-packages of the virtualenv to work with
site_packages_path = os.path.join(VENV_PATH, 'lib/python3.12/site-packages')
if os.path.exists(site_packages_path):
    site.addsitedir(site_packages_path)
    logging.info(f"Added site-packages to path: {site_packages_path}")
else:
    log_and_raise(FileNotFoundError, f"Site-packages directory not found: {site_packages_path}")

# Add the app's directory to the PYTHONPATH
project_path = '/home/joe/Documents/TickerWebsite'
if os.path.exists(project_path):
    sys.path.insert(0, project_path)
    logging.info(f"Added project directory to PYTHONPATH: {project_path}")
else:
    log_and_raise(FileNotFoundError, f"Project directory not found: {project_path}")

# Activate the virtual environment
activate_env = os.path.join(VENV_PATH, 'bin', 'activate')
if os.path.exists(activate_env):
    try:
        logging.info(f"Attempting to activate virtual environment using: {activate_env}")
        with open(activate_env) as f:
            exec(f.read(), dict(__file__=activate_env))
        logging.info(f"Activated virtual environment: {activate_env}")
    except Exception as e:
        log_and_raise(e, f"Failed to activate virtual environment: {e}")
else:
    log_and_raise(FileNotFoundError, f"Virtual environment activation script not found: {activate_env}")

# Import the Flask app
try:
    from app import app as application
    logging.info("Successfully imported app as application")
except ImportError as e:
    log_and_raise(ImportError, "Could not import 'app' from the application. Ensure that 'app.py' exists and is correctly set up.")
except Exception as e:
    log_and_raise(e, "An error occurred while importing the application.")

