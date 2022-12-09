import { AsyncRequest } from './async-request.mjs';

export class HashRouter {
    constructor(selector, routes) {
        this.selector = selector;
        this.routes = routes;
    }

    get root() {
        return '/#!/';
    }

    hashchange() {
        const request = new AsyncRequest();
        const selector = this.selector;
        const routes = this.routes;
        return async function () {
            let hash = window.location.hash;
            // block empty hashes
            // NOTE: hash and query params still need to be implemented
            if (!hash) {
                window.history.back();
                return;
            }
            const route = routes[hash] || routes[404];
            const html = await request.text(route);

            document.querySelector(selector).innerHTML = html;
        };
    }

    click() {
        const hashchange = this.hashchange();

        return function (event) {
            event = event || window.event;

            const a = event.target.closest('a');

            event.preventDefault();

            window.history.pushState({}, '', a.href);
            hashchange();
        };
    }

    init(selector) {
        const hashchange = this.hashchange();
        const click = this.click();
        const element = document.querySelector(selector);
        const anchors = element.querySelectorAll('a');

        if (!window.location.hash) {
            window.location = this.root;
        }

        for (let a of anchors) {
            if (a.getAttribute('data-route')) {
                a.addEventListener('click', click);
            }
        }

        window.addEventListener('hashchange', hashchange);
        hashchange();
    }
}
