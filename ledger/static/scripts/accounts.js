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
function accountsResponsiveResize() {
    let list = document.querySelector('.list-group');
    ['load', 'resize'].forEach((event) => {
        window.addEventListener(event, () => {
            if (window.innerWidth < 768) {
                list.classList.remove('w-50');
                list.classList.remove('w-75');
                list.classList.add('w-100');
            } else if (window.innerWidth < 992) { 
                list.classList.remove('w-50')
                list.classList.remove('w-100')
                list.classList.add('w-75')
            } else {
                list.classList.remove('w-75');
                list.classList.remove('w-100');
                list.classList.add('w-50');
            }
        });
    });
}


function accountsToggleSelectField() {
    let form = document.querySelector('#create-accounts');

    form.platform.addEventListener('change', (event) => {
        let element, value = event.target.value;

        switch (value) {
            case 'coinbase-pro':
                element = form.passphrase.parentElement;
                element.classList.remove('d-none');
                form.passphrase.setAttribute('type', 'password');
                break;
            case 'kraken':
                element = form.passphrase.parentElement;
                element.classList.add('d-none');
                form.passphrase.setAttribute('type', 'hidden');
                break;
            default:
                throw '[Error] selected platform is unsupported';
                break;
        }
    });
}
