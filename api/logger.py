import os
import yaml
import logging
import logging.config
from utils import get_config


with open('logger_config.yaml', 'rt') as f:
    log_config = yaml.safe_load(f.read())

# Create the log file if it does not exist
filename = log_config['handlers']['file']['filename']

if not os.path.exists(os.path.dirname(filename)):
    os.makedirs(os.path.dirname(filename))

# Set up the configuration for the logger
logging.config.dictConfig(log_config)


def get_logger():
    '''
    Get logger with the appropriate configuration

    Returns:
        logger: logging.Logger
    '''
    config = get_config()
    logger = logging.getLogger(config['logger'])
    
    return logger