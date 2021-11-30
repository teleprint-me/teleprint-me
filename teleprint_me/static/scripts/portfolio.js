const updatePortfolioOnMessage = (event) => {
    let total = 0;
    let product = {};
    let message = JSON.parse(event.data);
    let table = document.querySelector('table#coinbase_pro');
    let input = document.querySelector('input#coinbase_pro_value');
    //console.log('[CoinbaseProWebSocketMessage]', message);
    if (message instanceof Object) {
        product.name = message.product_id ? message.product_id.split('-')[0] : '';
        product.price = message.price ? (+(message.price)).toFixed(2) : 0;
        if (!product.name) { 
            return;
        }
        for (let row of table.tBodies[0].rows) {
            if (row.dataset.name.includes('USD')) {
                product.balance = (+(row.dataset.balance)).toFixed(2); 
                if (0 < product.balance) {
                    row.children[3].innerText = product.balance;
                } else {
                    table.deleteRow(row.rowIndex);
                }
                total += (+(product.balance));
            }
            if (row.dataset.name.includes(product.name)) {
                product.balance = (+(row.dataset.balance)).toFixed(8); 
                product.value = (+(product.balance * product.price)).toFixed(2);
                if (0 < product.value) {
                    row.children[1].innerText = product.price;
                    row.children[2].innerText = product.value;
                    row.children[3].innerText = product.balance;
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


const set_total_on_change = () => {
    let form = document.querySelector('form');
    form.coinbase_pro.addEventListener('change', (event) => {
        let table = document.querySelector('table#total_value');
        table.
            tBodies[0].
            rows[0].
            cells[0].
            innerText = (+(form.coinbase_pro.value)).toFixed(2);
    });
};


const run_websocket = (context) => {
    set_total_on_change();
    let socket = new CoinbaseProWebSocket(context, updatePortfolioOnMessage);
    socket.send();
};
