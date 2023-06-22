class AsyncRequest {
    async get(url, type = 'text') {
        const response = await fetch(url);

        switch (type) {
            case 'text':
                return response.text();
            case 'json':
                return response.json();
            case 'blob':
                return response.blob();
            default:
                throw new Error(`Invalid response type: ${type}`);
        }
    }

    async template(url) {
        const html = await this.get(url, 'text');
        const template = document.createElement('template');
        template.innerHTML = html;
        return template;
    }

    async style(url) {
        const css = await this.get(url, 'text');
        const style = document.createElement('style');
        style.innerHTML = css;
        return style;
    }

    async cssStyleSheet(url) {
        const css = await this.get(url, 'text');
        const cssStyleSheet = new CSSStyleSheet();
        cssStyleSheet.replaceSync(css);
        return cssStyleSheet;
    }
}

export { AsyncRequest };
