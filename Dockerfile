FROM python:3.11-slim-buster

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY /donateasyouread /app

WORKDIR /app

RUN python manage.py migrate && \
    python manage.py collectstatic

EXPOSE 8888

CMD ["python", "manage.py", "runserver", "0.0.0.0:8888"]

