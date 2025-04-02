from internal.config import configuration as c
import logging
import requests
import unidecode


def get_tlaloc_id(job):
    state = job.location.split(",")[1]
    city = job.location.split(",")[0]
    state = unidecode.unidecode(str(state).lower())

    body = {
        "locations": [
            {
                "state": state,
                "city": city
            }
        ]
    }

    request = requests.post(c.tlaloc_url, json=body, headers={"Authorization": "Token " + c.tlaloc_token})
    if request.status_code == 200:
        json_response = request.json()
        location_id = json_response['compatibility']
        location_id = str(location_id).split(':')[1].replace("'", '').replace('}', '').strip()
        # state_response = json_response['locations'][str(location_id)]['statename']
        job.location_id = location_id
    else:
        logging.fatal(f'tlaloc_id not found, ref {job.reference_id} - title {job.title}')
        return ['mexico', 1]