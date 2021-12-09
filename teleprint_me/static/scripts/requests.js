const request = function (method, url, message=null) {
    return new Promise(function (resolve, reject) {
        let xhr = new XMLHttpRequest();
        xhr.open(method, url);
        xhr.onload = function (event) {
            if (this.status >= 200 && this.status < 300) {
                resolve(xhr.response);
            } else {
                reject({
                    status: this.status,
                    statusText: xhr.statusText
                });
            }
        };
        xhr.onerror = function (event) {
            reject({
                status: this.status,
                statusText: xhr.statusText
            });
        };
        if (message) {
            xhr.send(JSON.stringify(message));
        } else {
            xhr.send();
        }
    });
};
