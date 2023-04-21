# Dockerfile_airflow
FROM python:3.10-slim

RUN apt-get update && apt-get install -y libpq-dev postgresql-client && rm -rf /var/lib/apt/lists/*
RUN pip install apache-airflow[postgres]

ENV AIRFLOW_HOME=/usr/local/airflow
ENV AIRFLOW__CORE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres/airflow
ENV AIRFLOW__CELERY__RESULT_BACKEND: db+postgresql://airflow:airflow@postgres/airflow
ENV AIRFLOW__WEBSERVER__AUTHENTICATE=True
ENV AIRFLOW__WEBSERVER__AUTH_BACKEND=airflow.contrib.auth.backends.password_auth
ENV AIRFLOW__WEBSERVER__AUTH_USER=admin
ENV AIRFLOW__WEBSERVER__AUTH_PASSWORD=admin

RUN airflow db init
RUN airflow users create --username admin --password admin --firstname first --lastname last --role Admin --email admin@example.com

WORKDIR /scraping

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /scraping

COPY ./dags /usr/local/airflow/dags

RUN airflow scheduler &

CMD ["airflow", "webserver", "-p", "8080"]