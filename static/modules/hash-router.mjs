import { AsyncRequest } from './async-request.mjs';

export class HashRouter {
    constructor(selector, routes) {
        this.selector = selector;
        this.routes = routes;
    }

    get root() {
        return '/#/';
    }

    hashchange() {
        const request = new AsyncRequest();
        const selector = this.selector;
        const routes = this.routes;

        return async function () {
            const hash = window.location.hash;
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

            window.history.pushState({ location: a.href }, '', a.href);
            hashchange();
        };
    }

    init() {
        const hashchange = this.hashchange();
        const click = this.click();
        const anchors = document.querySelector('.router').querySelectorAll('a');

        if (!location.hash) {
            location = this.root;
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
