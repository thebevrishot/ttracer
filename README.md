# TORN Tracker

## Installation

```sh
python3 -m venv venv
./venv/bin/activate

pip install -r requirements.txt
```

## Setup RETHINK DB

1. install rethink DB using brew or docker https://rethinkdb.com/

2. Go to admin server http://localhost:8080/?#tables, Create DB name `torn` with tables
  - `addresses` with index `address`
  - `dest`
  - `txns`

## Test running

```sh
ETHERSCAN_API_KEY=... python main.py
```