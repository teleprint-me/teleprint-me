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
const getIteratorFromObject = (object) => {
    let dataSet = [];
    for (let key in object) {
        dataSet.push([key, object[key]]);
    }
    return dataSet;
}


const removeChildrenFromElement = (element) => {
    children = Array.from(element.children);
    for (child of children) { 
        child.remove(); 
    }
}
