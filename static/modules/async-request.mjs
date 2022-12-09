export class AsyncRequest {
    async text(url) {
        return await fetch(url).then((response) => response.text());
    }

    async json(url) {
        return await fetch(url).then((response) => response.json());
    }

    async blob(url) {
        return await fetch(url).then((response) => response.blob());
    }

    async template(url) {
        const html = await this.text(url);
        const template = document.createElement('template');
        template.innerHTML = html;
        return template;
    }

    async style(url) {
        const css = await this.text(url);
        const style = document.createElement('style');
        style.innerHTML = css;
        return style;
    }

    async cssStyleSheet(url) {
        const css = await this.text(url);
        const cssStyleSheet = new CSSStyleSheet();
        cssStyleSheet.replaceSync(css);
        return cssStyleSheet;
    }
}
