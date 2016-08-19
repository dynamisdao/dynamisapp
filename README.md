# Dynamis

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

### Run tests (under virtual env)
```bash
cd tests/python
py.test -s 
```

### Start server 

```bash
# Install/create virtualenv (one-time only)
sudo pip install virtualenv
cd dynamis-folder
virtualenv venv

# Start working in virtualenv
source venv/bin/active
pip install -r requirements.txt

# Start open to the world server on port 8000
python manage.py runserver 0.0.0.0:8000

# Exit virtualenv
deactivate
```
