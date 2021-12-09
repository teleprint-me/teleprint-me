const set_datalist_default = (response) => {
    let message = JSON.parse(response);
    let datalist = document.querySelector('#products');
    let node = document.createElement('option');
    removeChildrenFromElement(datalist);
    node.setAttribute('value', 'Not Available');
    datalist.appendChild(node);
    console.log('[StrategyDataListError]', message)
};


const set_datalist_products = (method, url) => {
    let promise = request(method, url);
    promise.then((response) => {
        let products = JSON.parse(response);
        let datalist = document.querySelector('#products');
        remove_children_from(datalist);
        for (let product of products) {
            if (!product.display_name) { continue; }
            let node = document.createElement('option');
            node.setAttribute('value', product.id);
            node.setAttribute('data-quote-increment', product.quote_increment);
            node.setAttribute('data-min-market-funds', product.min_market_funds);
            node.setAttribute('data-max-market-funds', product.max_market_funds);
            datalist.appendChild(node);
        }
    }).catch(set_datalist_default);
    return promise;
};


const toggle_product_oninput = (event) => {
    event.target.value = event.target.value.toUpperCase();
};


const toggle_strategy_onchange = (event) => {
    let yield_ = event.target.form.yield_;
    switch (event.target.value) {
        case 'value_average':
        case 'dynamic_value_average':
            yield_.parentElement.classList.remove('d-none');
            yield_.setAttribute('required', 'true');
            break;
        case 'cost_average':
        case 'dynamic_cost_average':
        default:
            yield_.parentElement.classList.add('d-none');
            yield_.removeAttribute('required');
            break;
    }
};


const get_principal_data = (datalist) => {
    for (let option of datalist.children) {
        if (option.value === form.product.value) {
            return option;
        }
    }
    return null;
};


const set_principal_data = (form, option) => {
    form.principal.value = option.dataset.minMarketFunds;
    form.principal.min = option.dataset.minMarketFunds;
    form.principal.max = option.dataset.maxMarketFunds;
    form.principal.step = option.dataset.quoteIncrement;
};


const set_principal_default = (form) => {
    form.principal.value = '';
    form.principal.min = '0';
    form.principal.step = '0.01';
};


const toggle_principal_onfocus = (event) => {
    let form = event.target.form;
    let datalist = document.querySelector('#products');
    let option = get_principal_data(datalist);

    if (!option) {
        set_principal_default(form);
        event.preventDefault();
        event.stopPropagation();
        return;
    }

    set_principal_data(form, option);
};
