import { AsyncRequest } from './async-request.mjs';
import { HashRouter } from './hash-router.mjs';
import { Theme } from './theme.mjs';

const request = new AsyncRequest();

const t_router = await request.template('/static/views/router.html');

const header = document.querySelector('#router');
header.appendChild(t_router.content.cloneNode(true));

const routes = {
    404: '/static/views/404.html',
    '#/': '/static/views/profile.html',
    '#/portfolio': '/static/views/portfolio.html',
    '#/contact': '/static/views/contact.html'
};

const router = new HashRouter('#app', routes);
const theme = new Theme();

router.init();
theme.init();
