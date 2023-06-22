import { RouterObserver } from './router-observer.mjs';

class HashRouter {
    constructor(selector, routes) {
        this.selector = selector;
        this.routes = routes;
        this.observer = null;
    }

    get root() {
        return '/#!/';
    }

    // Set the observer property to the specified observer object.
    observe(observer) {
        this.observer = observer;
    }

    init(selector) {
        const hashchange = this.observer.hashchange();
        const click = this.observer.click();

        const element = document.querySelector(selector);
        const anchors = element.querySelectorAll('a');

        // Create a new RouterObserver instance and register it as the observer
        // for the HashRouter.
        this.observe(new RouterObserver(this.selector, this.routes));

        if (!window.location.hash) {
            window.location = this.root;
        }

        for (let a of anchors) {
            if (a.hash.startsWith('#!/')) {
                console.log('Registered Route:', a.hash);
                a.addEventListener('click', click);
            }
        }

        window.addEventListener('hashchange', hashchange);
        hashchange();
    }
}

export { HashRouter };
