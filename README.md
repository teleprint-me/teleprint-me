# teleprint-me

A web application to track cryptocurrency investments

## Status

- This is a work in progress
- Core application features may be broken, buggy, and/or missing
- This application is currenctly in the prototype phase.

## Requirements

- Linux 5.4.x or greater
- Python 3.6.x or greater
- [MongoDB](https://docs.mongodb.com/manual/installation/) 4.2.x or greater

## Install and Run

```sh
# clone the repo
$ git clone https://github.com/teleprint-me/ledger.git
# change directory
$ cd ledger
# initialize virtual environment
$ virtualenv venv
# use/enter the virtual environment
$ source venv/bin/activate 
# using setup.py is optional
$ python setup.py install
# using requirements is recommended
$ pip install -r requirements.txt
$ echo 'MONGO_URI=\'mongodb://localhost:27017/ledger\'' > .env
# run the server
$ ./run.sh
```

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
