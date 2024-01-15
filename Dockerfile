FROM python:slim

WORKDIR /code

COPY ./requirements-es.txt /code/requirements.txt

RUN apt-get update && apt-get install -y build-essential

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY /app-es /code/app

WORKDIR /code/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

EXPOSE 8080