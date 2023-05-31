import os
import logging
from pathlib import Path
from dotenv import load_dotenv

logging.getLogger('watchdog').setLevel(logging.ERROR)  # suppress watchdog spammy logging

# Get the project root directory
PROJECT_ROOT = Path(os.path.dirname(os.path.abspath(__file__)))
ROOT_FILE_DIR = os.path.join(PROJECT_ROOT, 'static')
ROOT_SESSION_DIR = os.path.join(ROOT_FILE_DIR, 'sessions')
ROOT_SCRIPT_DIR = os.path.join(ROOT_FILE_DIR, 'scripts')

load_dotenv()


def get_env_variable(var_name, default_value=None):
    try:
        return os.environ[var_name]
    except KeyError:
        if default_value is None:
            raise Exception(f"The {var_name} environment variable is not set.")
        return default_value


class Config:
    DEBUG = get_env_variable('DEBUG', 'false').lower() == 'true'
    MAX_BUFFER_SIZE_MB = int(get_env_variable('MAX_BUFFER_SIZE_MB', 200))
    MAX_BODY_SIZE_MB = int(get_env_variable('MAX_BODY_SIZE_MB', 200))
    SESSION_INACTIVITY_TIMEOUT = int(get_env_variable('SESSION_INACTIVITY_TIMEOUT', 5 * 60))
    COMPRESS_RESPONSE = get_env_variable('COMPRESS_RESPONSE', 'true').lower() == 'true'
    COOKIE_SECRET = get_env_variable('COOKIE_SECRET', 'PLOTOLO_SECRET')
    ENABLE_XSRF = get_env_variable('ENABLE_XSRF', 'false').lower() == 'true'

