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
const getCoinbaseProProducts = (context, currency) => {
    let base = null;
    let products = [];
    for (let account of context.accounts) {
        for (let asset of context.assets) {
            // asset.display -> '<currency>/<base>'
            if (asset.id && (account.name === asset.name)) {
                base = asset.id.split('-')[1];
                if (base.includes(currency) && base === currency) {
                    products.push(asset.id);
                }
            }
        }
    }
    return products;
};


const coinbaseProPortfolioOnMessage = (event) => {
    let asset = {};
    let table = document.querySelector('table#coinbase-pro');
    let message = JSON.parse(event.data);
    console.log('[CoinbaseProSocketMessage]', message);
    if (message instanceof Object) {
        asset.name = message.product_id ? message.product_id.split('-')[0] : '';
        asset.price = message.price ? (+(message.price)).toFixed(2) : 0;
        if (!asset.name || !asset.price) { 
            return;
        }
        for (let row of table.tBodies[0].rows) {
            if (row.dataset.name.includes(asset.name)) {
                asset.value = (+(row.dataset.balance * asset.price)).toFixed(2);
                asset.balance = (+(row.dataset.balance)).toFixed(8); 
                if (asset.value >= 1) {
                    row.children[1].innerText = asset.price;
                    row.children[2].innerText = asset.value;
                    row.children[3].innerText = asset.balance;
                } else {
                    table.deleteRow(row.rowIndex);
                }
            }
        }
    }
};


class CoinbaseProWebSocket {
    constructor(products, onmessage) {
        this.stream = new WebSocket('wss://ws-feed.pro.coinbase.com');
        this.request = JSON.stringify({
            'type': 'subscribe',
            'product_ids': products,
            'channels': ['ticker']
        });
        this.stream.onerror = (event) => { 
            throw new Error('[CoinbaseProSocketError]', event); 
        };
        this.stream.onopen = (event) => { 
            console.log('[CoinbaseProSocketOpen]', event); 
        };
        this.stream.onclose = (event) => { 
            console.log('[CoinbaseProSocketClose]', event); 
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
                throw new Error('[CoinbasePro] failed to initialize websocket stream');
            }
        }, 1000);
    }
}
