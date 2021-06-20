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
