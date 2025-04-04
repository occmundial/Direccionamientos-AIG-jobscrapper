from internal.config import configuration as c
from pkg.slack_pkg import slack_func as sf
import logging
import pyodbc
import socket



def init_db_connection():
    try:
        print("Resolviendo host:", c.host)
        print("IP:", socket.gethostbyname(c.host))
        conn_str = ("Driver={ODBC Driver 17 for SQL Server};"
                                f"Server={c.host};"
                                f"UID={c.user};"
                                f"PWD={c.password};"
                                f"Database={c.db_name};"
                                "Connection Timeout=20;")
        print(conn_str)
        db_conn = pyodbc.connect(conn_str,
                                 readonly=True)
        logging.info('Conexión a BD establecida.')
        sf.post_message(':information_source: Conexión a BD establecida.')
        return True, db_conn
    except Exception as error:
        logging.info('No se pudo establecer conexión a base de datos. *{0}*-> {1}'.format('db_connection.init_db_connection', error))
        sf.post_message(':exclamation: No se pudo establecer conexión a base de datos. Proceso finalizado.')
        return False, None