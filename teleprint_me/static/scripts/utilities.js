const log_error = (message) => {
    console.log('[Error]', message);
};


const get_iterator_from = (object) => {
    let dataset = [];
    for (let key in object) { dataset.push([key, object[key]]); }
    return dataset;
}


const remove_children_from = (element) => {
    for (let child of Array.from(element.children)) { child.remove(); }
}
