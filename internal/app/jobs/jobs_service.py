from internal.app.jobs.job_servicer import JobServicer
import internal.app.jobs.jobs_repository as jr
from pkg.awss3 import s3_connection as s3c
from pkg.db_conn import db_connection as dbc
from pkg.slack_pkg import slack_func as sf
import logging
import time

class JobService(JobServicer):
    def __init__(self):
        self.repository_publish_jobs = None
        self.s3conn = None
        self.db_conn = None
        # Establecer conexión a AWSS3
        is_s3_connected, self.s3conn, s3_file_name = s3c.init_s3_connection()
        if is_s3_connected is False:
            sf.post_message(':warning: No se detectó algún archivo para procesar. Proceso finalizado.')
        else:
            # Establecer conexión a base de datos
            is_db_connected, self.db_conn = dbc.init_db_connection()
            if is_db_connected is False:
                time.sleep(1)
                is_db_connected, self.db_conn = dbc.init_db_connection()
                if is_db_connected is False:
                    sf.post_message(
                        ':exclamation: Error detectado al tratar de establecer conexión a BD. Proceso finalizado.')
            else:
                self.repository_publish_jobs = jr.JobRepository(s3_file_name, self.s3conn, self.db_conn)


    def Start(self):
        # Descarga del archivo S3
        is_downloaded, error = self.repository_publish_jobs.download_s3_file()
        if is_downloaded:
            # Obtención de datos del archivo.
            is_got_data, error = self.repository_publish_jobs.get_data_from_file()
            if is_got_data:
                # Procesamiento de información.
                error = self.repository_publish_jobs.process_information()
                if error is not None:
                    logging.error(error)
                    sf.post_message(
                            ':exclamation: Error durante el procesamiento de la información. Proceso finalizado.')
            else:
                logging.error(error)
                sf.post_message(
                        ':exclamation: Error detectado al tratar de obtener la información del archivo S3. Proceso finalizado.')
        else:
            logging.error(error)
            sf.post_message(':exclamation: Error detectado al tratar de descargar el archivo de AWSS3. Proceso finalizado.')