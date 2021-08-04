/* Ledger - A web application to track cryptocurrency investments
** Copyright (C) 2021 teleprint.me
**
** This program is free software: you can redistribute it and/or modify
** it under the terms of the GNU Affero General Public License as published by
** the Free Software Foundation, either version 3 of the License, or
** (at your option) any later version.
**
** This program is distributed in the hope that it will be useful,
** but WITHOUT ANY WARRANTY; without even the implied warranty of
** MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
** GNU Affero General Public License for more details.
**
** You should have received a copy of the GNU Affero General Public License
** along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/
const totalInputOnChange = () => {
    let form = document.querySelector('form');
    let inputs = document.querySelectorAll('input');
    let table = document.querySelector('table#total-value');
    inputs.forEach((element) => {
        element.addEventListener('change', (event) => {
            let total = 0;
            for (let element of form.elements) {
                total += (+(element.value));
            }
            table.tBodies[0].rows[0].cells[0].innerText = (+(total)).toFixed(2);
        });
    });
};


const coinbaseWebSocketFactory = (context, currency) => {
    return null;
};


const coinbaseProWebSocketFactory = (context, currency) => {
    let products = getCoinbaseProProducts(context, currency);
    let socket = new CoinbaseProWebSocket(products, coinbaseProPortfolioOnMessage);
    totalInputOnChange();
    socket.send();
};


const krakenWebSocketFactory = (context, currency) => {
    let products = getKrakenProducts(context, currency);
    let socket = new KrakenWebSocket(products, krakenPortfolioOnMessage);
    totalInputOnChange();
    socket.send();
};


const runWebSocketFactory = (map, currency) => {
    for (let view of map) {
        let client = view[0];
        let context = view[1];
        switch(client) {
            case 'coinbase':
                break
            case 'coinbase-pro':
                coinbaseProWebSocketFactory(context, currency);
                break;
            case 'kraken':
                krakenWebSocketFactory(context, currency);
                break;
            default:
                throw new Error(`[Error] ${client} is currently unsupported`);
        }
    }
};
