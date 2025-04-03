import yaml
import logging.config
import os
from datetime import datetime


def setup_middleware():
    logger()


def logger():
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    log_dir = "logs"
    with open("logging.yaml", 'rt') as f:
        config = yaml.safe_load(f.read())
    log_filename = os.path.join(log_dir, f"logs-{fecha_actual}.log")
    print(log_filename)
    config['handlers']['info_file_handler']['filename'] = log_filename
    config['handlers']['error_file_handler']['filename'] = log_filename
    logging.config.dictConfig(config)
