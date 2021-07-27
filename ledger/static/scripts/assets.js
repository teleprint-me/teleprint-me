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
const error = (message) => {
    console.log('[Error]', message);
};


const setAssetPromise = (method, url) => {
    let promise = request(method, url);
    promise.then((response) => {
        let assets = JSON.parse(response);
        let datalist = document.querySelector('#pairs');
        removeChildrenFromElement(datalist);
        for (let asset of assets) {
            if (!asset['display']) { continue; }
            let node = document.createElement('option');
            node.setAttribute('value', asset['display']);
            node.setAttribute('data-id', asset['id']);
            node.setAttribute('data-min', asset['min-size']);
            node.setAttribute('data-name', asset['name']);
            datalist.appendChild(node);
        }
    }).catch(error);
    return promise;
};


const setDefaultDatalist = () => {
    let datalist = document.querySelector('#pairs');
    let node = document.createElement('option');
    removeChildrenFromElement(datalist);
    node.setAttribute('value', 'Not Available');
    datalist.appendChild(node);
};


const togglePlatformOnChange = (event) => {
    let platform = event.target.value;
    switch (platform) {
        case 'coinbase-pro':
        case 'kraken':
            setAssetPromise('GET', `/client/${platform}/assets`);
            break;
        default:
            setDefaultDatalist();
            break;
    };
};


const toggleStrategyOnChange = (event) => {
    let apy = event.target.form.apy;
    switch (event.target.value) {
        case 'value-average':
        case 'dynamic-value-average':
            apy.parentElement.classList.remove('d-none');
            apy.setAttribute('required', 'true');
            break;
        case 'cost-average':
        case 'dynamic-cost-average':
        default:
            apy.parentElement.classList.add('d-none');
            apy.removeAttribute('required');
            break;
    }
};


const getMessageOnError = (object) => {
    let message;

    if (!object.platform) {
        message = '[Error] platform field is empty';
    } else if (!object.asset) { 
        message = '[Error] asset field is empty';
    } else if (!object.id) { 
        message = `[Error] failed to set id=${object.id}`;
    } else if (!object.min) {
        message = `[Error] failed to set min=${min}`;
    }

    return message;
};


const getPrincipleData = (datalist) => {
    for (let child of datalist.children) {
        console.log('[Info] seeking `id` and `min`');
        let value = child.getAttribute('value');
        if (value === form.asset.value) {
            let id = child.getAttribute('data-id');
            let min = child.getAttribute('data-min');
            console.log(`[Info] set id=${id} and min=${min} using value=${value}`);
            return {'id': id, 'min': min};
        }
    }
    return {};
};


const togglePrincipleOnFocus = (event) => {
    // grab elements
    let form = event.target.form;
    let datalist = document.querySelector('#pairs');

    // grab required attributes
    let data = getPrincipleData(datalist);

    let fields = {
        'platform': form.platform.value,
        'asset': form.asset.value,
        'id': data.id,
        'min': data.min
    };

    // set message on error
    let message = getMessageOnError(fields);

    // avoid making the request if an error occurred
    if (message) {
        console.log(message);
        event.preventDefault();
        event.stopPropagation();
        return;
    }

    // grab data
    let promise = request('GET', `/client/${fields.platform}/price/${fields.id}`);

    // commit promise
    promise.then((response) => {
        // update principle min value
        let amount = undefined;
        let price = JSON.parse(response);
        switch (fields.platform) {
            case 'coinbase-pro':
            case 'kraken':
                if (fields.min > 0 && fields.min < 1) {
                    amount = Math.ceil(price.ask * fields.min);
                } else {
                    amount = fields.min;
                }
                if (amount <= 5) {
                    amount = 5;
                }
                form.principle.setAttribute('min', amount);
                console.log(`[Info] set amount=${amount} using price['ask']=${price['ask']}`)
                break;
            default:
                form.principle.setAttribute('min', 5);
                break;
        }
    }).catch(error);
};
