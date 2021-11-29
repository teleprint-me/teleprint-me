// TODO: use css `@media min-width` instead of 
// js `window.innerWidth` for affecting form width...
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
