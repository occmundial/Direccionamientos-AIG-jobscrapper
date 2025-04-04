from pkg.slack_pkg import slack_func as sf
import yaml
import logging.config
from datetime import datetime


def setup_middleware():
    logger()


def logger():
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    fecha_hora_actual = datetime.now().strftime("%Y-%m-%d %H-%M")
    with open("logging.yaml", 'rt') as f:
        config = yaml.safe_load(f.read())
    config['handlers']['info_file_handler']['filename'] = "logs/logs-{}.log".format(fecha_actual)
    config['handlers']['error_file_handler']['filename'] = "logs/logs-{}.log".format(fecha_actual)
    logging.config.dictConfig(config)
    sf.post_message(':information_source: Inicio del proceso AIG publish jobs - *ASPEND* V1 - {}'.format(fecha_hora_actual))
