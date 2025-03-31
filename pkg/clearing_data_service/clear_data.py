import re
import logging

def clear_data(job):
    job.description = lock_information(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', '', job.description)
    job.description = lock_information(r'([442][0-9]{9})', '', job.description)
    job.description = lock_information(r'\b\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}\b', '', job.description)
    job.description = lock_information(r'([www.]+[a-zA-Z0-9_.+-]+.com)', '', job.description)


def lock_information(pattern, replace_with, text):
    try:
        reg = re.compile(pattern)
        text = reg.sub(replace_with, text)
        return text
    except Exception as error:
        logging.error(':exclamation: Error pkg/clearing_data_service/clear_data.lock_information -> {}'.format(str(error)))