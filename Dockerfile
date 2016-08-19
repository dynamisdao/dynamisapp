FROM ubuntu:14.04
ENV DJANGO_SECRET_KEY='this-is-not-a-real-secret-key-do-not-use-me'
ENV DJANGO_EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend'
ENV DJANGO_DEBUG='True'
ENV DJANGO_DEBUG_TOOLBAR_ENABLED='True'
ENV DATABASE_URL='sqlite://memory:'
ENV SITE_DOMAIN="local-dev"
ENV DJANGO_EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend

COPY . /var/www/Dynamisapp
RUN apt-get update \
    && apt-get install -y \
            python \
            python-dev \
            python-pip \
            python-pytest \
            libpq-dev \
            postgresql \
            postgresql-contrib \
            gunicorn \
            rng-tools \
    && pip install -r /var/www/Dynamisapp/requirements.txt \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get purge -y \
            python-dev \
            libpq-dev
WORKDIR /var/www/Dynamisapp
ENTRYPOINT gunicorn --bind 0.0.0.0:8000 --access-logfile - --error-logfile - dynamis.wsgi
