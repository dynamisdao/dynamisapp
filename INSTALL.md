
## Reqs:

### Required packages for Ubuntu:

* libpq-dev sqlite3 libsqlite3-dev postgresql postgresql-contrib rng-tools
* python-pip python-dev python-pytest

### Install postgress

```bash
# Change all to TRUST (no password)
sudo vim /etc/postgresql/9.3/main/pg_hba.conf

# Create new DB
createdb dynamis

# Access it
sudo -i -u postgres
psql -d dynamis
```

### Create migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

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

python manage.py runserver 0.0.0.0:8000

# Exit virtualenv
deactivate
```

