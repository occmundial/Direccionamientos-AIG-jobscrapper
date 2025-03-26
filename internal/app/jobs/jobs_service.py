from internal.app.jobs.job_servicer import JobServicer
from pkg.slack_pkg import slack_func as sf
from pkg.db_conn import db_connection as dbc
from pkg.awss3 import s3_connection as s3c
import internal.app.jobs.jobs_repository as jr
import logging
import time

class JobService(JobServicer):
    def __init__(self):
        # Establecer conexión a AWSS3
        is_s3_connected, s3conn, s3_file_name = s3c.init_s3_connection()
        if is_s3_connected is False:
            sf.post_message(':warning: No se detectó algún archivo para procesar. Proceso finalizado.')
        else:
            # Establecer coneción a base de datos
            is_db_connected, db_conn = dbc.init_db_connection()
            if is_db_connected is False:
                time.sleep(1)
                is_db_connected, db_conn = dbc.init_db_connection()
                if is_db_connected is False:
                    sf.post_message(
                        ':exclamation: Error detectado al tratar de establecer conexión a BD. Proceso finalizado.')
            else:
                self.repository_publish_jobs = jr.JobRepository(s3_file_name, s3conn, db_conn)


    def Start(self):
        if self.repository_publish_jobs.s3conn is not None and self.repository_publish_jobs.cursor is not None:
            # Descarga del archivo S3
            is_downloaded, error = self.repository_publish_jobs.download_s3_file()
            if is_downloaded:
                # Obtención de datos del archivo.
                is_got_data, error = self.repository_publish_jobs.get_data_from_file()
                if is_got_data:
                    # Procesamiento de información.
                    self.repository_publish_jobs.process_information()
                else:
                    logging.error(error)
                    sf.post_message(
                        ':exclamation: Error detectado al tratar de obtener la información del archivo S3. Proceso finalizado.')
            else:
                logging.error(error)
                sf.post_message(':exclamation: Error detectado al tratar de descargar el archivo de AWSS3. Proceso finalizado.')