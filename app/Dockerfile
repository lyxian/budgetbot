FROM python:3.10.1-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

CMD ["python", "Server/main.py"]