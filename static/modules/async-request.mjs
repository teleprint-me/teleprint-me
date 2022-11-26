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
        let template = document.createElement('template');
        template.innerHTML = await this.text(url);
        return template;
    }
}
