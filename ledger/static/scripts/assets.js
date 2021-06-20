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
const getAssetsFromData = (object) => {
    let coinbasepro, kraken;
    for (let data of object) {
        if (data['platform'] === 'coinbase-pro') {
            coinbasepro = ['coinbase-pro', data['assets']];
        } else if (data['platform'] === 'kraken'){
            let iterator = getIteratorFromObject(data['assets']);
            kraken = ['kraken', new Map(iterator)];
        }
    }
    return new Map([coinbasepro, kraken]);
};


const setDefaultDatalist = (form, datalist) => {
    let node = document.createElement('option');
    node.setAttribute('value', 'Not Available');
    removeChildrenFromElement(datalist);
    datalist.appendChild(node);
};


const setCoinbaseProDatalist = (datalist, assets) => {
    let coinbasepro = assets.get('coinbase-pro');
    for (let asset of coinbasepro) {
        let node = document.createElement('option');
        node.setAttribute('value', asset['display_name']);
        datalist.appendChild(node);
    }
};


const setKrakenDatalist = (datalist, assets) => {
    let kraken = assets.get('kraken');
    for (let asset of kraken.values()) {
        if (asset['wsname'] == null) { 
            continue; 
        }
        node = document.createElement('option');
        node.setAttribute('value', asset['wsname']);
        datalist.appendChild(node);
    }
};


const setCoinbaseProMinValue = (form, assets) => {
    let coinbasepro = assets.get('coinbase-pro');
    for (let asset of coinbasepro) {
        console.log('seeking...')
        if (form.asset.value === asset['display_name']) {
            console.log('found coinbase-pro asset!')
            form.principle.setAttribute('min', asset['min_market_funds'])
            break;
        }
    } 
};


const setKrakenMinValue = (form, assets) => {
    let kraken = assets.get('kraken');
    for (let asset of kraken.values()) {
        console.log('seeking...')
        if (form.asset.value === asset['wsname']) {
            console.log('found kraken asset!')
            form.principle.setAttribute('min', asset['ordermin'])
            break;
        }
    }
}


const updateMinPrincipleAmount = (event) => {
    let form = event.target.form;
    switch (form.account.value) {
        case 'coinbase-pro':
            setCoinbaseProMinValue(form, assets);
            break;
        case 'kraken':
            setKrakenMinValue(form, assets);
            break;
        default:
            break;
    }
}


const toggleAccount = (event) => {
    let datalist = document.querySelector('#asset-pairs');
    let form = event.target.form;
    removeChildrenFromElement(datalist);
    form.asset.parentElement.classList.remove('d-none');
    form.strategy.parentElement.classList.remove('d-none');
    switch (event.target.value) {
        case 'coinbase-pro':
            setCoinbaseProDatalist(datalist, assets);
            break;
        case 'kraken':
            setKrakenDatalist(datalist, assets);
            break;
        default:
            setDefaultDatalist(form, datalist);
            break;
    };
};


const toggleStrategy = (event) => {
    let apy = event.target.form.apy;
    switch (event.target.value) {
        case 'cost-average':
        case 'dynamic-cost-average':
            apy.parentElement.classList.add('d-none');
            apy.removeAttribute('required');
            break;
        case 'value-average':
        case 'dynamic-value-average':
            apy.parentElement.classList.remove('d-none');
            apy.setAttribute('required', 'true');
            break;
        default:
            apy.parentElement.classList.add('d-none');
            apy.removeAttribute('required');
            break;
    }
};
