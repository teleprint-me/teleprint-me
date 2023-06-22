export class Theme {
    get selector() {
        return 'data-theme';
    }

    light = () => (a) => {
        const i = a.querySelector('i');
        const span = a.querySelector('span');

        a.setAttribute(this.selector, 'dark');
        a.classList.replace('theme-moon', 'theme-sun');
        i.classList.replace('bxs-moon', 'bxs-sun');
        span.innerText = 'Light';
    };

    dark = () => (a) => {
        const i = a.querySelector('i');
        const span = a.querySelector('span');

        a.setAttribute(this.selector, 'light');
        a.classList.replace('theme-sun', 'theme-moon');
        i.classList.replace('bxs-sun', 'bxs-moon');
        span.innerText = 'Dark';
    };

    click = () => (event) => {
        const a = event.target.closest('a');

        if ('light' === a.getAttribute(this.selector)) {
            this.light()(a);
        } else {
            this.dark()(a);
        }

        localStorage.setItem(this.selector, a.getAttribute(this.selector));
    };

    init() {
        const element = document.querySelector(`[${this.selector}]`);
        const selector = element.getAttribute(this.selector);
        const store = localStorage.getItem(this.selector);

        element.addEventListener('click', this.click());

        if (store != null) {
            if (store !== selector) {
                element.click();
            }
        }
    }
}
