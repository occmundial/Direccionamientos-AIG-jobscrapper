from internal.config import configuration as c
from pkg.slack_pkg import slack_func as sf
import boto3
import logging


def init_s3_connection():
    cons3 = boto3.client('s3', aws_access_key_id=c.aws_access_key,
                         aws_secret_access_key=c.aws_secret_access_key,
                         aws_session_token=c.aws_token,
                         region_name=c.aws_region)
    key = c.s3_key + '/aig-'
    occ_direcc = cons3.list_objects_v2(Bucket=c.s3_bucket, Prefix=key)
    if 'Contents' in occ_direcc:
        sorted_objects = sorted(occ_direcc['Contents'], key=lambda obj: obj['LastModified'], reverse=True)
        if key in sorted_objects[0]['Key']:
            logging.info("El último archivo a procesar es - {}".format(sorted_objects[0]['Key']))
            sf.post_message(':info: El último archivo a procesar es - {}'.format(sorted_objects[0]['Key']))
            return True, cons3, sorted_objects[0]['Key']
        else:
            logging.error("No se detectó algún archivo para procesar.")
            sf.post_message(':warning: No se detectó algún archivo para procesar. Proceso finalizado.')
            return False, None, ""
    else:
        logging.error("No se pudo establecer conexión a AWSS3.")
        sf.post_message(':exclamation: No se pudo establecer conexión a AWSS3. Proceso finalizado.')
        return False, None, ""

