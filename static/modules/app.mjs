import { Register } from './register.mjs';
import { HashRouter } from './hash-router.mjs';
import { Theme } from './theme.mjs';
import { AppRouter } from '../components/router.mjs';

const components = [
    {
        name: 'app-router',
        constructor: AppRouter
    }
];

const register = new Register();
console.log('Has Template Support:', register.hasTemplateSupport);
console.log('Has Shadow Support:', register.hasShadowSupport);
register.components(...components);

const setup_router = async () => {
    const routes = {
        404: '/static/views/404.html',
        '#!/': '/static/views/profile.html',
        '#!/portfolio': '/static/views/portfolio.html',
        '#!/contact': '/static/views/contact.html'
    };

    const router = new HashRouter('#app', routes);

    router.init('app-router');
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
