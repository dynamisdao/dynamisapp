
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

### Start Ethereum server

Dynamis requires running Ethereum node: see [User's Wallet screenshot here](https://s4.postimg.org/njujdb3x9/wallet.png)

Please start DEDICATED server. Do not run **geth** on the same machine that backend uses.

```bash
# Install geth on Ubuntu
# Please see https://github.com/ethereum/go-ethereum/wiki/Installation-Instructions-for-Ubuntu

sudo apt-get install software-properties-common
sudo add-apt-repository -y ppa:ethereum/ethereum
sudo add-apt-repository -y ppa:ethereum/ethereum-dev
sudo apt-get update
sudo apt-get install ethereum

# Start geth (MainNet)
geth --rpc --rpcport "8545" --rpcaddr "0.0.0.0" --rpccorsdomain "*"

# Start geth (TestNet)
geth --testnet --rpc --rpcport "8545" --rpcaddr "0.0.0.0" --rpccorsdomain "*"
```
