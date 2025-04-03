FROM python:3.9-slim-buster AS base

ENV ACCEPT_EULA=Y

RUN apt-get update && \
    apt-get install --no-install-suggests --no-install-recommends --yes curl wget ca-certificates build-essential firefox-esr && \
    curl https://packages.microsoft.com/keys/microsoft.asc | tee /etc/apt/trusted.gpg.d/microsoft.asc && \
    curl https://packages.microsoft.com/config/debian/11/prod.list | tee /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update && \
    apt-get install --no-install-suggests --no-install-recommends --yes msodbcsql17
RUN sed -i 's/SECLEVEL=2/SECLEVEL=1/g' /etc/ssl/openssl.cnf

FROM base AS dependencies
RUN pip3 install --upgrade pip
COPY requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt
RUN pip3 install pyodbc

FROM dependencies
WORKDIR /app
COPY . .
RUN mkdir -p "app/logs"
CMD ["python","-i", "main.py"]