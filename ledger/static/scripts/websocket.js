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
