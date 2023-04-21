FROM python:3.10-slim

WORKDIR /dash

COPY . /dash

RUN pip install -r requirements.txt

EXPOSE 8050

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8050"]