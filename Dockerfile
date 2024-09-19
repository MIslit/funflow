FROM python:3.10-slim

SHELL ["/bin/bash", "-c"]

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN apt update && apt -qy install gcc libjpeg-dev libxslt-dev \
    libpq-dev libmariadb-dev libmariadb-dev-compat gettext cron openssh-client flake8 locales vim

RUN useradd -rms /bin/bash funflow && chmod 777 /opt /run

WORKDIR /funflow


RUN mkdir /funflow/static && mkdir /funflow/media && chown -R funflow:funflow /funflow && chmod 755 /funflow

COPY --chown=funflow:funflow . .


RUN pip install -r requirements.txt

USER funflow

RUN chmod +x /funflow/manage.py

CMD ["bash", "-c", "./manage.py collectstatic --noinput && ./manage.py migrate && ./manage.py runserver 0.0.0.0:8000"]
