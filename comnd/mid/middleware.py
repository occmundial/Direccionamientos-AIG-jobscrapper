import yaml
import logging.config
from datetime import datetime


def setup_middleware():
    logger()


def logger():
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    with open("logging.yaml", 'rt') as f:
        config = yaml.safe_load(f.read())
    config['handlers']['info_file_handler']['filename'] = "logs/logs-{}.log".format(fecha_actual)
    config['handlers']['error_file_handler']['filename'] = "logs/logs-{}.log".format(fecha_actual)
    logging.config.dictConfig(config)
