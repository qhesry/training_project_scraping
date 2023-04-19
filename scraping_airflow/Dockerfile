# Dockerfile_airflow
FROM apache/airflow:2.5.3-python3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

# Configure Airflow
ENV AIRFLOW_HOME=/app/airflow
RUN airflow db init
RUN airflow users create --username admin --password admin --firstname Admin --lastname User --role Admin --email admin@example.com

CMD ["airflow", "webserver", "--port", "8080"]