export class Theme {
    get attribute() {
        return 'data-theme';
    }

    light() {
        const attribute = this.attribute;

        return function (a) {
            const i = a.querySelector('i');
            const span = a.querySelector('span');

            a.setAttribute(attribute, 'dark');
            a.classList.replace('theme-moon', 'theme-sun');
            i.classList.replace('bxs-moon', 'bxs-sun');
            span.innerText = 'Light';
        };
    }

    dark() {
        const attribute = this.attribute;

        return function (a) {
            const i = a.querySelector('i');
            const span = a.querySelector('span');

            a.setAttribute(attribute, 'light');
            a.classList.replace('theme-sun', 'theme-moon');
            i.classList.replace('bxs-sun', 'bxs-moon');
            span.innerText = 'Dark';
        };
    }

    click() {
        const attribute = this.attribute;
        const light = this.light();
        const dark = this.dark();

        return function (event) {
            const a = event.target.closest('a');

            if ('light' === a.getAttribute(attribute)) {
                light(a);
            } else {
                dark(a);
            }

            localStorage.setItem(attribute, a.getAttribute(attribute));
        };
    }

    init() {
        const element = document.querySelector('[data-theme]');
        const attribute = element.getAttribute('data-theme');
        const store = localStorage.getItem('data-theme');

        element.addEventListener('click', this.click());

        if (store != null) {
            if (store !== attribute) {
                element.click();
            }
        }
    }
}
