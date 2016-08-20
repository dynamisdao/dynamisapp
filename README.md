# Dynamis
https://codeship.com/projects/3abe4270-4901-0134-1120-52b63a9a4ec4/status?branch=master

[Installation details is here](INSTALL.md).

[Backend API documentation is here](http://docs.dynamis1.apiary.io).

[Django configuration help is here](DJANGO_HELP.md).

## Deployment scheme
![deployment scheme](https://s4.postimg.org/gdghow8rh/dynamis_deployment_scheme.png)

## Frontend (React)

* Tests run with `npm test`
* Build assets with `npm run build`
* Watch/build in development with `npm run watch`


## Backend (Django)

### Start server

```bash
# Start working in virtualenv (see installation details on how to prepare virtualenv) 
source venv/bin/active

# Start open to the world server on port 8000
python manage.py runserver 0.0.0.0:8000

# Exit virtualenv
deactivate
```

### Run tests 

```bash
# Start working in virtualenv (see installation details on how to prepare virtualenv) 
source venv/bin/active

cd tests/python

py.test -s 

# Exit virtualenv
deactivate
```

