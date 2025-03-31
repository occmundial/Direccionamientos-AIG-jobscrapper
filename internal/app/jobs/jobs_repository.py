from comnd.constants import constants as cns
from internal.app.jobs.job_functionaliter import JobFunctionaliter
from internal.config import configuration as c
from internal.models.job import Job
from pkg.clearing_data_service import clear_data
from pkg.salary_service import salary
from pkg.semantic_search_service import semantic_search
from pkg.slack_pkg import slack_func as sf
from pkg.tlaloc_service import tlaloc
from pkg.web_service import job_scrapper
from boto3.s3.transfer import S3Transfer
import csv
import logging
import os


class JobRepository(JobFunctionaliter):
    def __init__(self, s3_file_name, s3conn, db_conn):
        self.s3_file_name = s3_file_name
        self.s3conn = s3conn
        self.cursor = db_conn.cursor()
        self.jobs = []
        self.existing_jobs = []
        self.total_jobs_in_file = 0
        self.total_jobs_to_discard = 0
        self.total_jobs_to_process = 0

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
            self.total_jobs_in_file = len(self.jobs)
            return True, None
        except Exception as error:
            return False, str(error)

    def process_information(self):
        try:
            message = cns.information_process_started_message
            self.print_send_message(cns.info_type, message, ":info: ")
            # Eliminar del listado las vacantes que ya existen para no republicarlas.
            self.remove_existing_jobs()
            self.publish_jobs()
            message = cns.information_process_finished_message
            self.print_send_message(cns.info_type, message, ":info: ")
            # Borrado del archivo.
            self.delete_file()
            return None
        except Exception as error:
            return str(error)

    def remove_existing_jobs(self):
        references, query = self.check_jobs_query()
        params = [cns.xmx] + references
        result = self.cursor.execute(query, params)
        for j in result:
            self.existing_jobs.append(j.JobRefCode)
        self.jobs = [p for p in self.jobs if p.reference_id not in self.existing_jobs]
        self.total_jobs_to_discard = len(self.existing_jobs)
        self.total_jobs_to_process = len(self.jobs)

    def check_jobs_query(self):
        str_jobs = ""
        references = []
        for job in self.jobs:
            str_jobs += "CAST(? AS VARCHAR(255)),"
            references.append(job.reference_id)
        str_jobs = str_jobs[0:len(str_jobs) - 1]
        return references, cns.query_existence.format(str_jobs)

    def publish_jobs(self):
        if c.prod_env:
            ws = job_scrapper.WebService()
            if ws.init_wsdl() is False:
                if ws.init_wsdl() is False:
                    logging.error(
                        'No se logró establecer conexión con el WS haciendo uso de las credenciales del usuario - {}'.format(
                            cns.xmx))
                else:
                    self.publish(ws)
            else:
                self.publish(ws)
        else:
            self.print_jobs_results()

    def publish(self, ws):
        for job in self.jobs:
            self.complete_data(job)
            ws.invoke_job_scrapper(job)
        self.print_jobs_results()
        self.print_vacancy_results(ws)


    def complete_data(self, job):
        tlaloc.get_tlaloc_id(job)
        semantic_search.get_skill_list(job)
        salary.get_salary(job)
        clear_data.clear_data(job)

    def delete_file(self):
        file_name = os.getcwd() + '\\logs\\' + self.s3_file_name.replace(c.s3_key + "/", "")
        if os.path.exists(file_name):
            os.remove(file_name)
            # logging.info("Archivo '{}' borrado.".format(self.s3_file_name.replace(c.s3_key + "/", "")))

    def print_jobs_results(self):
        count = 1
        for job in self.jobs:
            print("Vacante " + str(count))
            print("Tipo de vacante: " + job.job_type)
            print("Titulo:          " + job.title)
            print("Url:             " + job.url)
            print("Ref:             " + job.reference_id)
            print("Loc:             " + job.location)
            print("user:            " + cns.xmx)
            if job.job_type != '1':
                print("Nombre comercial:" + job.commercial_name)
            print('\n')
            count += 1
        message = cns.total_jobs_in_file_message.format(self.total_jobs_in_file)
        self.print_send_message(cns.info_type, message, "")
        message = cns.total_jobs_to_discard_message.format(self.total_jobs_to_discard)
        self.print_send_message(cns.info_type, message, "")
        message = cns.total_jobs_to_process.format(self.total_jobs_to_process)
        self.print_send_message(cns.info_type, message, "")

    def print_vacancy_results(self, ws):
        message = cns.published_vacancies_count_message.format(len(ws.published_vacancies_count))
        self.print_send_message(cns.info_type, message, ">>> :white_check_mark: ")
        message = cns.not_published_vacancies_count_message.format(len(ws.not_published_vacancies_count))
        self.print_send_message(cns.info_type, message, ":exclamation: ")
        message = cns.vacancies_without_points_message.format(len(ws.vacancies_without_points))
        self.print_send_message(cns.info_type, message, ":negative_squared_cross_mark: ")
        message = cns.error_count_message.format(len(ws.error_count))
        self.print_send_message(cns.info_type, message, ":x: ")


    def print_send_message(self, message_type, message, icon):
        if "" in icon:
            sf.post_message(message)
        else:
            sf.post_message(icon.join(message))

        if message_type == "info":
            logging.info(message)
        else:
            logging.error(message)