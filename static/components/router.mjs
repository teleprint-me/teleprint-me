import { AsyncRequest } from '../modules/async-request.mjs';

const TEMPLATE_URL = '/static/templates/router.html';

export class AppRouter extends HTMLElement {
    constructor() {
        super();
    }

    async connectedCallback() {
        const request = new AsyncRequest();
        const template = await request.template(TEMPLATE_URL);
        const node = template.content.cloneNode(true);
        const shadow = this.attachShadow({ mode: 'open' });
        shadow.appendChild(node);
    }
}
