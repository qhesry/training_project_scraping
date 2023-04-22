FROM python:3.10-slim

WORKDIR /dash

COPY . /dash

RUN pip install -r requirements.txt

EXPOSE 8050

CMD ["gunicorn", "-b", "0.0.0.0:8050", "main:server"]