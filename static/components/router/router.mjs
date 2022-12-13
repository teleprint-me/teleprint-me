import { AsyncRequest } from '../../modules/async-request.mjs';

const TEMPLATE_URL = '/static/components/router/template.html';
const STYLE_URL = '/static/components/router/style.css';

export class AppRouter extends HTMLElement {
    constructor() {
        super();
    }

    async connectedCallback() {
        const request = new AsyncRequest();
        const template = await request.template(TEMPLATE_URL);
        const style = await request.style(STYLE_URL);
        const node = template.content.cloneNode(true);
        const shadow = this.attachShadow({ mode: 'open' });
        node.appendChild(style);
        shadow.appendChild(node);
    }
}
