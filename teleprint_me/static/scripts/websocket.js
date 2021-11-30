class CoinbaseProWebSocket {
    constructor(context, onmessage) {
        this.context = context;
        this.stream = new WebSocket(context.feed);
        this.request = JSON.stringify({
            'type': 'subscribe',
            'product_ids': context.product_ids,
            'channels': ['ticker']
        });
        this.stream.onerror = (event) => { 
            throw new Error('[CoinbaseProWebSocketError]', event); 
        };
        this.stream.onopen = (event) => { 
            console.log('[CoinbaseProWebSocketOpen]', event); 
        };
        this.stream.onclose = (event) => { 
            console.log('[CoinbaseProWebSocketClose]', event); 
        };
        this.stream.onmessage = onmessage;
    }

    get name() {
        return this.context.name;
    }

    get feed() {
        return this.context.feed;
    }

    send() {
        let stream = this.stream;
        let request = this.request;
        setTimeout(() => { 
            if (stream.OPEN) {
                stream.send(request);
            } else {
                throw new Error('[CoinbaseProWebSocketError] failed to initialize websocket stream');
            }
        }, 1000);
    }
}
