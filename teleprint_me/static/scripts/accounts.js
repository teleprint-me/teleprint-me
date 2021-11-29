function toggleAccountsSelectField() {
    let form = document.querySelector('#create-accounts');

    form.platform.addEventListener('change', (event) => {
        let element, value = event.target.value;

        switch (value) {
            case 'coinbase-pro':
                element = form.passphrase.parentElement;
                element.classList.remove('d-none');
                form.passphrase.setAttribute('type', 'password');
                break;
            case 'coinbase':
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
