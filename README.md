# teleprint-me

Apply averaging strategies to cryptocurrency with this web application.

## About

A web application to apply averaging strategies to cryptocurrency investments.

- Use Fiat to trade crypto to maximize capital gains.
- Use Bitcoin or Ether to trade between cryptos to maximize stacking Sats and Gwei.
- Set a target with, or without, a yield to pump up returns over time.
- Get an analysis on your investment strategy so you can optimize returns.

Supports Multiple Averaging Strategies

- Cost Averaging
- Dynamic Cost Averaging
- Value Averaging
- Dynamic Value Averaging

## Status

- This application is currently in the planning phase.
- Core application features may be broken, buggy, and/or missing.
- Ideas and Contributions are welcome

## Requirements

- Linux 5.4.x or greater
- Python 3.6.x or greater
- [MongoDB](https://docs.mongodb.com/manual/installation/) 4.2.x or greater
- Coinbase Account
- Coinbase Pro API Key

## Setup and Run

### Pip Setup

```sh
# This is not recommended because this project is still in planning phase
pip install --user git+https://github.com/teleprint-me/teleprint-me.git#egg=teleprint-me
```

### Manual Setup

```sh
git clone https://github.com/teleprint-me/teleprint-me.git
cd teleprint-me
virtualenv venv
source venv/bin/activate 
pip install -r requirements.txt  # recommended
python setup.py install  # not recommended
echo 'MONGO_URI="mongodb://localhost:27017/ledger"' > .env
./run.sh  # run the server
```

## Task List

- [ ] Client Support
    - [x] Coinbase Pro
- [ ] Core
    - [ ] Server Side Rest API
    - [ ] Client Side Websocket
- [ ] Management
    - [ ] Session
    - [ ] Settings
    - [ ] Account
    - [ ] Asset
    - [ ] Strategy
    - [ ] Wallet
    - [ ] Portfolio
- [ ] Trade
    - [ ] Manual
    - [ ] Automatic

## Tips

- Bitcoin (Segwit): 3E1YSahzUnYYx2RTuRt4KWogDBCsdCS1n3
- Ethereum: 0x7be933221135468b9886632771fF289341144C3a
- Litecoin (Segwit): MMNDfhgc3jfs3XJoJ7DSCedBp742dH12jD

## License
Copyright (C) 2021 teleprint.me

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see [GNU Licenses](https://www.gnu.org/licenses/).
