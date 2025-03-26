import os

env = os.environ.get('ENVIROMENT')

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
