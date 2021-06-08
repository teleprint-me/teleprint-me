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
function navbarRemovePageHighlight() {
    let navItems = document.querySelectorAll('.nav-item');

    for (let navItem of navItems) {
        let anchor = navItem.children[0];

        if (anchor.classList.contains('active')) {
            anchor.classList.remove('active');
            anchor.removeAttribute('aria-current');

            return true;
        }
    }

    return false;
}


function navbarSetPathname() {
    let pathname = document.location.pathname;

    if (pathname === '/') {
        return 'portfolio';
    }

    pathname = pathname.split('/')[1].toLowerCase();

    if (!pathname) {
        throw '[Error] failed to detect the document pathname';
        return undefined;
    }

    return pathname;
}


function navbarSetAnchor(pathname) {
    let anchor = document.querySelector(`#nav-${pathname}`);

    if (anchor) {
        anchor.classList.add('active');
        anchor.setAttribute('aria-current', 'page');
    } else {
        throw '[Error] failed to highlight current page in navbar';
        return undefined;
    }

    return anchor;
}


function navbarAddPageHighlight() {
    let pathname = navbarSetPathname();
    let anchor = navbarSetAnchor(pathname);
}
