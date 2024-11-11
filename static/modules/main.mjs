/**
 * @file static/modules/main.mjs
 */

export class Theme {
    get selector() {
        return 'data-theme';
    }

    light() {
        const selector = this.selector;

        return function (a) {
            const i = a.querySelector('i');
            const span = a.querySelector('span');

            a.setAttribute(selector, 'dark');
            a.classList.replace('theme-moon', 'theme-sun');
            i.classList.replace('bxs-moon', 'bxs-sun');
            span.innerText = 'Light';
        };
    }

    dark() {
        const selector = this.selector;

        return function (a) {
            const i = a.querySelector('i');
            const span = a.querySelector('span');

            a.setAttribute(selector, 'light');
            a.classList.replace('theme-sun', 'theme-moon');
            i.classList.replace('bxs-sun', 'bxs-moon');
            span.innerText = 'Dark';
        };
    }

    click() {
        const selector = this.selector;
        const light = this.light();
        const dark = this.dark();

        return function (event) {
            const a = event.target.closest('a');

            if ('light' === a.getAttribute(selector)) {
                light(a);
            } else {
                dark(a);
            }

            localStorage.setItem(selector, a.getAttribute(selector));
        };
    }

    init() {
        const element = document.querySelector('[data-theme]');
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

export function responsiveTables(event) {
    const tables = document.querySelectorAll('table');
    tables.forEach((table) => {
        const headers = Array.from(table.querySelectorAll('thead th'));
        table.querySelectorAll('tbody tr').forEach((row) => {
            Array.from(row.cells).forEach((cell, index) => {
                if (headers[index]) {
                    cell.setAttribute(
                        'data-label',
                        headers[index].textContent
                    );
                }
            });
        });
    });
}
