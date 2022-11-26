import { AsyncRequest } from './request.mjs';

const request = new AsyncRequest();

export class HashRouter {
    constructor(selector, routes) {
        this.selector = selector;
        this.routes = routes;
    }

    get root() {
        return '/#!/';
    }

    hashchange() {
        const selector = this.selector;
        const routes = this.routes;

        return async function () {
            const hash = window.location.hash;
            const route = routes[hash] || routes[404];
            const html = await request.text(route);

            document.querySelector(selector).innerHTML = html;
        };
    }

    route() {
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
        const route = this.route();
        const anchors = document.querySelector('.router').querySelectorAll('a');

        if (location.pathname === '/') {
            location = this.root;
        }

        for (let anchor of anchors) {
            if (anchor.getAttribute('data-theme')) {
                continue;
            }

            anchor.addEventListener('click', route);
        }

        window.addEventListener('hashchange', hashchange);
        hashchange();
    }
}
