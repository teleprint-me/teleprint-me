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
            a.setAttribute('aria-label', 'Switch to Light Theme');
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
            a.setAttribute('aria-label', 'Switch to Dark Theme');
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

export function responsiveTables(selector = 'table') {
    const tables = document.querySelectorAll(selector);
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

export function setupMarkedOptions() {
    // Configure marked.js with highlight.js for code syntax highlighting
    marked.setOptions({
        highlight: function (code, lang) {
            // Function to handle code syntax highlighting using highlight.js
            // Get the language if available, otherwise set it as plain text
            const language = highlight.getLanguage(lang) ? lang : 'plaintext';
            // Apply highlighting and get the highlighted code
            return highlight.highlight(code, {language}).value;
        },
        // Use 'hljs' class prefix for compatibility with highlight.js CSS
        langPrefix: 'hljs language-',
        // Use async; this is disabled by default
        async: true
    });
    console.log('Successfully initialized marked.js');
}

export function setupHighlightJS() {
    // Highlight all the code snippets in the document
    hljs.highlightAll(); // Initial code highlighting, if any
    console.log('Successfully initialized highlight.js');
}

export function checkCDNDependencies() {
    const scripts = document.querySelectorAll('script[data-cdn]');
    const missingLibraries = [];

    scripts.forEach((script) => {
        const libName = script.getAttribute('data-cdn');

        // Check for the library's global presence based on known global objects
        const isLibraryLoaded = (() => {
            switch (libName.toLowerCase()) {
                case 'highlight.js':
                    return typeof hljs !== 'undefined';
                case 'marked':
                    return typeof marked !== 'undefined';
                case 'mathjax':
                    return typeof MathJax !== 'undefined';
                default:
                    return false;
            }
        })();

        if (!isLibraryLoaded) {
            missingLibraries.push(libName);
            console.warn(`${libName} failed to load from CDN`);
        } else {
            console.log(`${libName} loaded successfully`);
        }
    });

    if (missingLibraries.length) {
        console.error(
            'The following CDN libraries failed to load:',
            missingLibraries.join(', ')
        );
    } else {
        console.log('All CDN libraries loaded successfully');
    }
}
