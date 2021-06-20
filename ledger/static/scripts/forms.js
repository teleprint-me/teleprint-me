/* Ledger - A web application to track cryptocurrency investments
** Copyright (C) 2021 teleprint.me
**
** This program is free software: you can redistribute it and/or modify
** it under the terms of the GNU Affero General Public License as published by
** the Free Software Foundation, either version 3 of the License, or
** (at your option) any later version.
**
** This program is distributed in the hope that it will be useful,
** but WITHOUT ANY WARRANTY; without even the implied warranty of
** MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
** GNU Affero General Public License for more details.
**
** You should have received a copy of the GNU Affero General Public License
** along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/
// TODO: use css `@media min-width` instead of 
// js `window.innerWidth` for affecting form width...
const formsResponsiveResize = () => {
    // adjust the form width based on the size of the window
    let forms = Array.from(document.forms);
    
    ['load', 'resize'].forEach((event) => {
        window.addEventListener(event, () => {
            if (window.innerWidth < 768) {
                forms.forEach((form) => {
                    form.classList.remove('w-50');
                    form.classList.remove('w-75');
                    form.classList.add('w-100');
                });
            } else if (window.innerWidth < 992) { 
                forms.forEach((form) => {
                    form.classList.remove('w-50')
                    form.classList.remove('w-100')
                    form.classList.add('w-75')
                });
            } else {
                forms.forEach((form) => {
                    form.classList.remove('w-75');
                    form.classList.remove('w-100');
                    form.classList.add('w-50');
                });
            }
        });
    });
};


const formsValidateRequired = () => {
    // validate required form fields
    let forms = Array.from(document.forms);

    forms.forEach((form) => {
        form.addEventListener('submit', (event) => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
    
            form.classList.add('was-validated');
        }, false);
    });
};


const formsHideElements = (form, ...names) => {
    // skip given [...names] and hide all other elements
    for (element of form.elements) {
        let skip = false;
        for (name of names) {
            if (element.name === name) {
                skip = true;
                break;
            }
        }
        if (skip) { continue; }
        element.parentElement.classList.add('d-none');
    }
    form.submit.classList.add('d-none');
};
