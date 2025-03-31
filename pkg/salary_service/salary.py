from internal.config import configuration as c
import logging
import json
import re
import requests
import unicodedata



def get_salary(job):
    try:
        def remove_accents(input_str):
            nfkd_form = unicodedata.normalize('NFKD', input_str)
            return ''.join([cd for cd in nfkd_form if not unicodedata.combining(cd)])

        pattern = re.compile('<.*?>')
        txt_clean = re.sub(pattern, '', str(job.title))

        # Eliminar acentos del texto y luego eliminar caracteres no deseados
        txt_clean = remove_accents(txt_clean)
        txt_clean = re.sub(r"[^a-zA-Z0-9]+", ' ', txt_clean)
        skills_txt = ','.join(job.skills)
        url = c.salary_url
        job.title = job.title.replace('\n', '')
        querystring = {"title": job.title, "algorithm": "sal2cat2", "norm": "true",
                       "size": "1", "state": job.location.split(",")[1], "origin": "direccionamiento-scrapper",
                       "skills": skills_txt}
        response = requests.request("GET", url, data="", headers="", params=querystring)
        job.salary_prediction = json.loads(response.text)
        job.salary_min = int(job.salary_prediction['lower_bound'])
        job.salary_max = int(job.salary_prediction['upper_bound'])
    except Exception as e:
        logging.fatal("Error get salary service {}".format(e))
        if c.prod_env is False:
            job.salary_prediction =  json.loads(
                '{"CategoryId":17,"SubCategoryId":238,"InCatalogID":0,"lower_bound":17833.333333333332,"median":18333.333333333332,"upper_bound":18583.333333333332}')