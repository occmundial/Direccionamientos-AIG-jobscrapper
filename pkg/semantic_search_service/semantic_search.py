from internal.config import configuration as c
import logging
import json
import re
import requests
import unicodedata


def get_skills(job):
    try:
        if c.prod_env is False:
            return ['specreq-innovative', 'specreq-adaptability', 'specreq-creative-thinking']

        # Función para eliminar acentos
        def remove_accents(input_str):
            nfkd_form = unicodedata.normalize('NFKD', input_str)
            return ''.join([cd for cd in nfkd_form if not unicodedata.combining(cd)])

        pattern = re.compile('<.*?>')
        txt_clean = re.sub(pattern, '', str(job.description))

        # Eliminar acentos del texto y luego eliminar caracteres no deseados
        txt_clean = remove_accents(txt_clean)
        txt_clean = re.sub(r"[^a-zA-Z0-9]+", ' ', txt_clean)

        response = requests.post(c.semantic_url, data="[\"" + txt_clean + "\"]",
                                 headers={'Authorization': 'Basic c2VhcmNoOkpncHFMeW55bUFRcG5MUnROM0N1TlJTYw==',
                                          'Content-Type': 'text/plain'})
        json_response = json.loads(response.text)
        skills = get_skill_list(json_response)

        if len(skills) == 0:
            logging.fatal("error get skills semantic")
        job.skills = skills
    except Exception as e:
        logging.fatal('error petition semantic {}'.format(e))


def get_skill_list(json_response):
    count = 0
    skill_list = []
    for i in range(len(json_response[0])):
        if json_response[0][i]['type'] == 'SKILL':
            if count < 3:
                skill_list.append(json_response[0][i]['id'])
                count = count + 1
                continue
    return skill_list