from internal.config import configuration as c
from comnd.constants import constants as cns
from pkg.slack_pkg import slack_func as sf
from internal.app.jobs.job_functionaliter import JobFunctionaliter
from boto3.s3.transfer import S3Transfer
from internal.models.job import Job
import logging
import os
import csv


class JobRepository(JobFunctionaliter):
    def __init__(self, s3_file_name, s3conn, db_conn):
        self.s3_file_name = s3_file_name
        self.s3conn = s3conn
        self.cursor = db_conn.cursor()
        self.jobs = []
        self.existing_jobs = []

    def download_s3_file(self):
        try:
            file_name = self.s3_file_name.replace(c.s3_key + "/", "")
            download_route = os.getcwd() + '\\logs\\' + file_name
            archivo = S3Transfer(self.s3conn)
            archivo.download_file(c.s3_bucket, self.s3_file_name, download_route)
            logging.info("Archivo de AWSS3 '{}' descargado.".format(file_name))
            return True, None
        except Exception as error:
            return False, str(error)

    def get_data_from_file(self):
        try:
            file_name = os.getcwd() + '\\logs\\' + self.s3_file_name.replace(c.s3_key + "/", "")
            with open(file_name, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    job = Job('', row["ReferenceID"], row["JobTitle"], row["JobLocation"], row["JobURL"], row["JobDescription"])
                    self.jobs.append(job)
            logging.info("Información de vacantes substraida.")
            return True, None
        except Exception as error:
            return False, str(error)

    def process_information(self):
        try:
            logging.info("Proceso de publicación de vacantes, iniciado.")
            sf.post_message(':info: Proceso de publicación de vacantes, iniciado.')
            # Eliminar del listado las vacantes que ya existen para no republicarlas.
            self.remove_existing_jobs()
            logging.info("Proceso de publicación de vacantes, concluido.")
            sf.post_message(':info: Proceso de publicación de vacantes, concluido.')
            # Borrado del archivo.
            self.delete_file()
            return True, None
        except Exception as error:
            return False, str(error)

    def remove_existing_jobs(self):
        query = self.check_jobs_query()
        result = self.cursor.execute(query)
        for j in result:
            self.existing_jobs.append(j.JobRefCode)
        self.jobs = [p for p in self.jobs if p.reference_id not in self.existing_jobs]

    def check_jobs_query(self):
        str_jobs = ""
        for job in self.jobs:
            str_jobs += "\'" + job.reference_id + "\',"
        str_jobs = str_jobs[0:len(str_jobs) - 1]
        return cns.query_existence.format(cns.xmx, str_jobs)

    def delete_file(self):
        file_name = os.getcwd() + '\\logs\\' + self.s3_file_name.replace(c.s3_key + "/", "")
        if os.path.exists(file_name):
            os.remove(file_name)
            logging.info("Archivo '{}' borrado.".format(self.s3_file_name.replace(c.s3_key + "/", "")))