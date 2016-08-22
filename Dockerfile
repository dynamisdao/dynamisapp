FROM ubuntu:14.04

ENV PROJECT_DIR=/var/www/Dynamisapp \
    GUNICORN_BIND=0.0.0.0:8000 \
    DJANGO_SECRET_KEY='this-is-not-a-real-secret-key-do-not-use-me' \
    DJANGO_DEBUG='True' \
    DJANGO_DEBUG_TOOLBAR_ENABLED='True' \
    DJANGO_EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend \
    DJANGO_DATABASE_ENGINE='django.db.backends.postgresql' \
    DJANGO_DATABASE_NAME='postgres' \
    DJANGO_DATABASE_USER='postgres' \
    DJANGO_DATABASE_PASSWORD='postgres' \
    DJANGO_DATABASE_HOST='localhost' \
    DJANGO_DATABASE_PORT='5432' \
    DJANGO_SITE_DOMAIN="local-dev"

# copy only requirements.txt to cache the next RUN statement for the docker build if changes made in PROJECT_DIR
COPY requirements.txt $PROJECT_DIR/requirements.txt
RUN apt-get update \
    && apt-get install -y \
            python \
            python-dev \
            python-pip \
            python-pytest \
            libpq-dev \
            postgresql \
            postgresql-contrib \
            rng-tools \
    && pip install -r $PROJECT_DIR/requirements.txt

# copy only package.json to cache the next RUN statement of nodejs and it's packages installing
COPY package.json $PROJECT_DIR/package.json
WORKDIR $PROJECT_DIR
RUN apt-get install -y \
        curl \
        git \
        libcairo2-dev \
        libjpeg8-dev \
        libpango1.0-dev \
        libgif-dev \
        build-essential \
        g++ \
    && curl -sL https://deb.nodesource.com/setup_6.x | sudo bash - \
    && apt-get install -y nodejs \
    && npm install

# layer of static files rebuilding
COPY . $PROJECT_DIR
RUN npm run build

CMD gunicorn --bind $GUNICORN_BIND --log-level debug --access-logfile - --error-logfile - \
             -c dynamis/gunicorn.conf dynamis.wsgi
