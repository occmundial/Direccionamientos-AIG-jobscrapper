from comnd.constants import constants as cons
from internal.config import configuration as c
import logging
import requests


def aais_get_token():
    url = f"{c.aais_token.format(c.user_job_scrapper, c.password_scrapper, cons.xmx)}"
    url = c.aais_server.format(url)
    response = requests.post(url)
    response.raise_for_status()
    token = response.json().get('response', {}).get('instead_of_authentication', {}).get('authentication_token',
                                                                                         {}).get('token')
    if not token:
        logging.fatal("Token not found in response")
    return token