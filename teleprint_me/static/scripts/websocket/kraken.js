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
const getKrakenProducts = (context, currency) => {
    let base = null;
    let products = [];
    for (let account of context.accounts) {
        for (let asset of context.assets) {
            // asset.display -> '<currency>/<base>'
            if (asset.display && (account.name === asset.name)) {
                base = asset.display.split('/')[1];
                if (base.includes(currency) && base === currency) {
                    products.push(asset.display);
                }
            }
        }
    }
    return products;
};


const krakenPortfolioOnMessage = (event) => {
    let message = JSON.parse(event.data);
    let table = document.querySelector('table#kraken');
    let input = document.querySelector('input#kraken-value');
    let total = 0;
    let asset = {};
    //console.log('[KrakenSocketMessage]', message);
    if (message instanceof Array) {
        asset.name = message[3].split('/')[0];
        asset.price = (+(message[1].p[0])).toFixed(2);
        for (let row of table.tBodies[0].rows) {
            if (row.dataset.name.includes('USD')) {
                asset.balance = (+(row.dataset.balance)).toFixed(2); 
                if (asset.balance > 1)
                    row.children[3].innerText = asset.balance;
                else
                    table.deleteRow(row.rowIndex);
                total += (+(asset.balance));
            }
            if (row.dataset.name.includes(asset.name)) {
                asset.balance = (+(row.dataset.balance)).toFixed(8); 
                asset.value = (+(asset.balance * asset.price)).toFixed(2);
                if (1 < asset.value) {
                    row.children[1].innerText = asset.price;
                    row.children[2].innerText = asset.value;
                    row.children[3].innerText = asset.balance;
                } else {
                    table.deleteRow(row.rowIndex);
                }
            }
            total += (+(row.children[2].innerText));
            input.value = (+(total)).toFixed(2);
            input.dispatchEvent(new Event('change'));
        }
    }
};


class KrakenWebSocket {
    constructor(products, onmessage) {
        this.stream = new WebSocket('wss://ws.kraken.com');
        this.request = JSON.stringify({
            'event': 'subscribe',
            'pair': products,
            'subscription': {
                'name': 'ticker'
            }
        });
        this.stream.onerror = (event) => { 
            throw new Error('[KrakenSocketError]', event); 
        };
        this.stream.onopen = (event) => { 
            console.log('[KrakenSocketOpen]', event); 
        };
        this.stream.onclose = (event) => { 
            console.log('[KrakenSocketClose]', event); 
        };
        this.stream.onmessage = onmessage;
    }

    get name() {
        return 'kraken';
    }

    send() {
        let stream = this.stream;
        let request = this.request;
        setTimeout(() => { 
            if (stream.OPEN) {
                stream.send(request);
            } else {
                throw new Error('[Kraken] failed to initialize websocket stream');
            }
        }, 1000);
    }
}
