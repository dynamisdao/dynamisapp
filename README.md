# Dynamis
[ ![Codeship Status for dynamisdao/dynamisapp](https://codeship.com/projects/3abe4270-4901-0134-1120-52b63a9a4ec4/status?branch=master)](https://codeship.com/projects/169478)

[![Heroku Master branch Build is here](https://heroku-badge.herokuapp.com/?app=dynamisapp)](https://dynamisapp.herokuapp.com)
[![Heroku Develop branch Build is here](https://heroku-badge.herokuapp.com/?app=dynamisapp-develop)](https://dynamisapp-develop.herokuapp.com)


[![Stories in Ready](https://badge.waffle.io/dynamisdao/dynamisapp.svg?label=ready&title=Ready)](http://waffle.io/dynamisdao/dynamisapp)

[Installation details are here](INSTALL.md).

[Backend API documentation is here](http://docs.dynamis1.apiary.io).

[Django configuration help is here](DJANGO_HELP.md).

[WIKI is here](https://github.com/dynamisdao/dynamisapp/wiki/Dynamis-WIKI).

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

