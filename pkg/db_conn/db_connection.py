from internal.config import configuration as c
from pkg.slack_pkg import slack_func as sf
import pyodbc
import logging


def init_db_connection():
    try:
        db_conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};" "Server=" + c.host + ";" "UID=" + c.user + ";" "PWD=" + c.password + ";" "Database=" + c.db_name + ";",
                          readonly=True)
        logging.info('Conexión a BD establecida.')
        sf.post_message(':info: Conexión a BD establecida.')
        return True, db_conn
    except Exception as error:
        logging.info('No se pudo establecer conexión a base de datos. *{0}*-> {1}'.format('db_connection.init_db_connection', error))
        sf.post_message(':exclamation: No se pudo establecer conexión a base de datos. Proceso finalizado.')
        return False, None