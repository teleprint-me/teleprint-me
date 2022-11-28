import { AsyncRequest } from './async-request.mjs';
import { HashRouter } from './hash-router.mjs';
import { Theme } from './theme.mjs';

const setup_router = async () => {
    const request = new AsyncRequest();

    const template = await request.template('/static/templates/router.html');

    const header = document.querySelector('#router');
    header.appendChild(template.content.cloneNode(true));

    const routes = {
        404: '/static/views/404.html',
        '#/': '/static/views/profile.html',
        '#/portfolio': '/static/views/portfolio.html',
        '#/contact': '/static/views/contact.html'
    };

    const router = new HashRouter('#app', routes);
    router.init();
};

const setup_theme = () => {
    const theme = new Theme();

    theme.init();
};

const main = async () => {
    await setup_router();
    setup_theme();
};

main();
