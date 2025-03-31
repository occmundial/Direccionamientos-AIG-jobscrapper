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
        self.published_vacancy = []
        self.count_vacancy_published = []
        self.vacancy_without_points = []
        self.count_vacancy_not_published = []
        self.vacancy_not_published = []
        self._second_petition = False

    def init_wsdl(self):
        try:
            token = token_service.aais_get_token()
            self.auth_client = Client(c.wsdl_auth_client)
            self.client = Client(c.wsdl_client)
            self.request = self.auth_client.factory.create("ns0:AuthenticationHeader")
            self.request.Username = cns.xmx
            self.request.Token = token
            self.client.set_options(soapheaders=self.request)
            logging.info("init wsdl finished - User: {}".format(cns.xmx))
            return True
        except Exception as error:
            logging.fatal("error init wsdl {}".format(str(error)))
            return False


    def invoke_job_scrapper(self, job):
        try:
            if c.publish_jobs is True:
                job.job_id = self.client.service.JobScrapper("", job.title, job.description, True,
                                                                 job.reference, job.salary_prediction['SubCategoryId'],
                                                                 job.url, job.show_salary,
                                                                 False, job.location_id, cns.xmx, job.salary_min, job.salary_max,
                                                                 job.job_type, job.bullet1, job.bullet2, job.bullet3, 'False', 'False',
                                                                 'False', 'True', '', '', '0', job.nombreComercial)

                if is_number(job.job_id) is True:
                    vacancy = cns.vacancy_published_message.format(job.title, str(job.job_id))
                    logging.info(vacancy)
                    self.published_vacancy.append(vacancy)
                    self.count_vacancy_published.append(job.job_id)
                else:
                    if cns.discount_point_error_message in job.job_id:
                        logging.info(
                                "{}- JobReference: {}".format(cns.discount_point_error_message,
                                    job.reference))
                        self.vacancy_without_points.append(job.title)
                    else:
                        logging.fatal(
                                str(':exclamation: -> Error, Respuesta del WS: {} - JobReference: {}').format(job.job_id,
                                                                                                              job.reference))
                        logging.fatal(str('> :exclamation: {} [PUBLICACIÓN FALLIDA {}] ').format(job.job_id, cns.company))
        except Exception as e:
            if self._second_petition:
                logging.fatal(':exclamation: writeDatabase {}'.format(str(e)))
                self.count_vacancy_not_published.append(1)
                self.vacancy_not_published.append(job.title)
            self._second_petition = True
            time.sleep(1)


def is_number(a):
    try:
        float(repr(a))
        bool_a = True
    except:
        bool_a = False

    return bool_a