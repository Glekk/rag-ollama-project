import os
import yaml
import logging
import logging.config
from utils import get_config


with open('logger_config.yaml', 'rt') as f:
    log_config = yaml.safe_load(f.read())

filename = log_config['handlers']['file']['filename']

if not os.path.exists(os.path.dirname(filename)):
    os.makedirs(os.path.dirname(filename))

logging.config.dictConfig(log_config)


def get_logger():
    config = get_config()
    logger = logging.getLogger(config['logger'])
    
    return logger