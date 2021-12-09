# teleprint-me

Apply averaging strategies to cryptocurrency with this web application.

## project status

- This application is currently in the planning phase.
- Core application features may be broken, buggy, and/or missing.
- Ideas and Contributions are welcome

## Prerequisites

- Linux 5.4.x or greater
- Python 3.9.x or greater
- Sqlite 3.36.x or greater
- Coinbase Account
- Coinbase Pro API Key

## About

- A web application to apply averaging strategies to cryptocurrency investments.
    - Use Fiat to trade crypto to maximize capital gains.
    - Use Bitcoin or Ether to trade between cryptos to maximize stacking Sats and Gwei.
    - Set a target with, or without, a yield to pump up returns over time.
    - Get an analysis on your investment strategy so you can optimize returns.

- Supports Multiple Averaging Strategies
    - Cost Averaging
    - Dynamic Cost Averaging
    - Value Averaging
    - Dynamic Value Averaging

## Setup and Run

_Note: You may experience issues if `sqlite3` is not installed and properly configured._

```sh
# download the repository
git clone https://github.com/teleprint-me/teleprint-me.git
# setup the virtual environment
cd teleprint-me
virtualenv venv
source venv/bin/activate
# install 3rd party dependencies
pip install -r requirements.txt
# run the flask server
./run.sh
```

## Task List

- [x] Client Support
    - [x] Coinbase Pro
- [ ] Core
    - [x] Security
    - [x] Sqlite
    - [ ] Database
- [ ] Nav
    - [ ] Portfolio
    - [ ] Trade
    - [ ] Menu
- [ ] Portfolio
    - [x] Ticker
    - [ ] ???
- [ ] Trade
    - [ ] ???
- [ ] Menu
    - [x] Interfaces
    - [x] Strategies
    - [ ] Wallets
    - [x] Settings
    - [ ] Tips
    - [x] License
    - [x] Source

## Tips

- Bitcoin (Segwit): 3E1YSahzUnYYx2RTuRt4KWogDBCsdCS1n3
- Ethereum: 0x7be933221135468b9886632771fF289341144C3a
- Litecoin (Segwit): MMNDfhgc3jfs3XJoJ7DSCedBp742dH12jD

## License
Copyright (C) 2021 teleprint.me

This program is free software: you can redistribute it and/or modify
it under the terms of the [GNU Affero General Public License](https://www.gnu.org/licenses/agpl-3.0.html) as published
by the [Free Software Foundation](https://www.fsf.org/), either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
[GNU Affero General Public License](https://www.gnu.org/licenses/agpl-3.0.html) for more details.

You should have received a copy of the [GNU Affero General Public License](https://www.gnu.org/licenses/agpl.html)
along with this program.  If not, see [GNU Licenses](https://www.gnu.org/licenses/).
