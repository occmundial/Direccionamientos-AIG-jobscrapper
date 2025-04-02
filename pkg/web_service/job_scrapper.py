from pkg.aais_service import token_service
from suds.client import Client
from internal.config import configuration as c
from comnd.constants import constants as cns
import logging
import time


class WebService:
    def __init__(self):
        self.auth_client = None
        self.client = None
        self.request = None
        self.published_vacancies = []
        self.published_vacancies_count = []
        self.vacancies_without_points = []
        self.not_published_vacancies_count = []
        self.not_published_vacancies = []
        self.error_count = []

    def init_wsdl(self):
        try:
            token = token_service.aais_get_token()
            self.auth_client = Client(c.wsdl_auth_client)
            self.client = Client(c.wsdl_client)
            self.request = self.auth_client.factory.create("ns0:AuthenticationHeader")
            self.request.Username = cns.xmx
            self.request.Token = token
            self.client.set_options(soapheaders=self.request)
            logging.info("init wsdl done")
            return True
        except Exception as error:
            logging.fatal("error init wsdl {}".format(str(error)))
            return False


    def invoke_job_scrapper(self, job):
        try:
            job.job_id = self.client.service.JobScrapper("", job.title, job.description, True,
                                                                 job.reference_id, job.salary_prediction['SubCategoryId'],
                                                                 job.url, job.show_salary,
                                                                 False, job.location_id, cns.xmx, job.salary_min, job.salary_max,
                                                                 job.job_type, job.bullet1, job.bullet2, job.bullet3, 'False', 'False',
                                                                 'False', 'True', '', '', '0', job.commercial_name)

            if is_number(job.job_id):
                vacancy = cns.vacancy_published_message.format(job.title, str(job.job_id))
                logging.info(vacancy)
                self.published_vacancies.append(vacancy)
                self.published_vacancies_count.append(job.job_id)
            else:
                if cns.discount_point_error_message in job.job_id:
                    logging.info(
                                "{}- JobReference: {}".format(cns.discount_point_error_message,
                                    job.reference_id))
                    self.vacancies_without_points.append(job.title)
                else:
                    logging.fatal(
                                str(':exclamation: -> Error, Respuesta del WS: {} - JobReference: {}').format(job.job_id,
                                                                                                              job.reference_id))
                    self.error_count.append(job.job_id + " - " + job.reference_id)
        except Exception as e:
            logging.fatal(':exclamation: Error {}'.format(str(e)))
            self.not_published_vacancies_count.append(job.reference_id)
            self.not_published_vacancies.append(job.title)
            time.sleep(1)


def is_number(a):
    try:
        float(repr(a))
        bool_a = True
    except:
        bool_a = False

    return bool_a