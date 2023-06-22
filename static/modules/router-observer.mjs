import { AsyncRequest } from './async-request.mjs';

// Define a simple observer class that updates the inner HTML of a specified
// element with the provided content. The class also defines the hashchange
// and click methods to handle the routing.
class RouterObserver {
    constructor(selector, routes) {
        this.selector = selector;
        this.routes = routes;
    }

    update(route, content, queryParams) {
        const element = document.querySelector(this.selector);
        element.innerHTML = content;

        if (queryParams) {
            for (const param of queryParams) {
                const element = document.querySelector(
                    `[data-param=${param[0]}]`
                );
                if (element) {
                    element.innerHTML = param[1];
                }
            }
        }
    }

    hashchange() {
        const request = new AsyncRequest();
        const routes = this.routes;
        const update = this.update.bind(this);

        return async function () {
            let hash = window.location.hash;

            // Check whether the hash is empty and redirect to the root route if it is.
            // Otherwise, proceed as usual.
            if (!hash) {
                window.location = this.root;
                return;
            }

            // Extract the query string from the hash.
            const queryIndex = hash.indexOf('?');
            let queryString = null;
            if (queryIndex !== -1) {
                queryString = hash.substring(queryIndex + 1);
                hash = hash.substring(0, queryIndex);
            }

            // Parse the query string and access the query parameters.
            const queryParams = queryString
                ? new URLSearchParams(queryString)
                : null;

            // Fetch the content for the corresponding route.
            const route = routes[hash] || routes[404];
            const content = await request.text(route);

            // Call the update method to handle the routing, passing the query
            // parameters as an argument.
            update(route, content, queryParams);
        };
    }

    click() {
        const hashchange = this.hashchange();

        return function (event) {
            event = event || window.event;

            const a = event.target.closest('a');

            console.log('Anchor Clicked', a.href);
            event.preventDefault();

            if (!a.hash.startsWith('#!/')) {
                console.log('Anchor Blocked:', a.href);
                return;
            }

            window.history.pushState({}, '', a.href);
            hashchange();
        };
    }
}

export { RouterObserver };
