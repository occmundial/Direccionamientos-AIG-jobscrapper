import os

env = os.environ.get('ENVIROMENT')
prod_env = False if "local" in env else True

# SLACK
channel = os.environ.get('CHANNEL')
slack_token = os.environ.get('SLACK_TOKEN')

# OCCPROD
host = os.environ.get('DB_HOST')
user = os.environ.get('DB_USER')
password = os.environ.get('DB_PASSWORD')
db_name = os.environ.get('DB_NAME')

# AWSS3
aws_access_key = os.environ.get('AWS_ACCESS_KEY')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
aws_token = os.environ.get('AWS_TOKEN')
aws_region = os.environ.get('AWS_REGION')
s3_bucket = os.environ.get('S3_BUCKET')
s3_key = os.environ.get('S3_KEY')
s3_urlDCN = os.environ.get('S3_URLDCN')

# SERVICES
tlaloc_url = os.environ.get('TLALOC')
tlaloc_token = os.environ.get('TLALOC_TOKEN')
semantic_url = os.environ.get('SEMANTIC')
salary_url = os.environ.get('SALARY')
clear_url = os.environ.get('CLEAR')

# AAIS
aais_token = os.environ.get('AAIS_TOKEN')
aais_server = os.environ.get("AAIS_SERVER")
user_job_scrapper = os.environ.get("USR_JOB_SCRAPER")
password_scrapper = os.environ.get("PASS_JOB_SCRAPER")

# WSDL WEB SERVICE
wsdl_auth_client = os.environ.get("WSDL_AUTH_CLIENT")
wsdl_client = os.environ.get("WSDL_CLIENT")

publish_jobs = os.environ.get('PUBLISH_JOBS')