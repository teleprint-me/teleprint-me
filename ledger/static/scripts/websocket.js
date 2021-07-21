const getClientSocket = (data, callback) => {
    let socket = new WebSocket(url);
    socket.onerror = (event) => {
        console.log('[Error]', event);
    };
    socket.onopen = (event) => {
        console.log(`[Open] opened socket with ${data.url} using ${data.message}`);
        socket.send(JSON.stringify(message));
    };
    socket.onclose = (event) => {
        console.log(`[Close] closed socket with ${data.url} using ${data.auth}`);
    };
    socket.onmessage = callback;
    return socket;
};

const getKrakenWebSocket = (data) => {
    const getAssetPairs = () => {
        let base = null;
        let pairs = [];

        for (let account of data.accounts) {
            for (let asset of data.assets) {
                // asset.display is type String of '<currency>/<base>' format
                if (asset.display && (account.name === asset.name)) {
                    base = asset.display.split('/')[1];
                    if (base.includes(data.currency) && base === data.currency) {
                        pairs.push(asset.display);
                    }
                }
            }
        }

        return pairs;
    };

    const getAssetNameFrom = (message) => {
        return message[3].split('/')[0];
    };

    const getAssetPriceFrom = (message) => {
        return (+(message[1].p[0])).toFixed(2);
    };

    const getAssetValueFor = (price, row) => {
        return (+(row.dataset.balance * price)).toFixed(2);
    };

    const getAssetBalanceFor = (row) => {
        return (+(row.dataset.balance)).toFixed(8);
    };

    const hasAssetFor = (name, row) => {
        return Boolean(row.id) && row.dataset.name.includes(name);
    };

    data.pairs = getAssetPairs();

    let socket = new WebSocket('wss://ws.kraken.com');

    socket.onerror = (event) => { 
        throw new Error('[KrakenError]', event); 
    };

    socket.onopen = (event) => { 
        console.log('[KrakenOpen] Opened new websocket stream'); 
    };

    socket.onclose = (event) => { 
        console.log('[KrakenClose] Closed existing websocket stream'); 
    };

    socket.onmessage = (event) => {
        let message = JSON.parse(event.data);

        console.log('[KrakenMessage]', message);

        if (message instanceof Array) {
            let name = getAssetNameFrom(message),
                price = getAssetPriceFrom(message),
                value = null;

            for (let row of data.table.rows) {
                if (hasAssetFor(name, row)) {
                    value = getAssetValueFor(price, row); 
                    if (value >= 1) {
                        row.children[1].innerText = price;
                        row.children[2].innerText = value;
                        row.children[3].innerText = getAssetBalanceFor(row); 
                    } else {
                        data.table.deleteRow(row.rowIndex);
                    }
                }
            }
        }
    };

    setTimeout(() => { 
        let message = JSON.stringify({
            'event': 'subscribe',
            'pair': data.pairs,
            'subscription': {
                'name': 'ticker'
            }
        });

        if (socket.OPEN) {
            socket.send(message);
        } else {
            throw new Error('[Kraken] failed to initialize websocket stream');
        }
    }, 1000);

    return socket;
};
