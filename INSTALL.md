
## Reqs:

### Required packages for Ubuntu:

* libpq-dev sqlite3 libsqlite3-dev postgresql postgresql-contrib rng-tools
* python-pip python-dev python-pytest

### Install Node
```bash
curl -sL https://deb.nodesource.com/setup_6.x | sudo bash -
sudo npm install -g brunch mocha

# Build web site 
npm run build
```

### Install postgress

```bash
# TODO: Change all to TRUST (no password) in this file
sudo vim /etc/postgresql/9.3/main/pg_hba.conf

# Create new DB
createdb dynamis

# Access it
sudo -i -u postgres
psql -d dynamis
```

### Install Python/dependencies

```bash
# Install/create virtualenv (one-time only)
sudo pip install virtualenv
virtualenv venv

source venv/bin/active
pip install -r requirements.txt
pip install -r requirements-dev.txt
deactivate
```

### Create migrations
```bash
python manage.py makemigrations

# Will populate your DB (see DB settings in your .env file)
python manage.py migrate
```


### Install and start IPFS daemon
```bash
wget https://dist.ipfs.io/go-ipfs/v0.4.2/go-ipfs_v0.4.2_linux-amd64.tar.gz
tar xvfz go-ipfs.tar.gz
sudo mv go-ipfs/ipfs /usr/local/bin/ipfs

ipfs init

# Start daemon on 5001 port
ipfs daemon

# Do not forget to add IPFS_HOST and IPFS_PORT to .env file
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
