class GalleryItemBuilder {
    constructor() {
        this.li = document.createElement('li');
        this.img = document.createElement('img');
    }

    setAttribute(object) {
        let label = object.label.split('_');
        this.li.setAttribute('class', 'gallery__item');
        this.img.setAttribute('class', 'gallery__image');
        this.img.setAttribute('src', object.path);
        this.img.setAttribute('alt', `${label[0]} project image ${label[1]}`);
    }

    appendChild(element) {
        this.li.appendChild(this.img);
        element.appendChild(this.li);
    }

    addEventListener(type, callback) {
        this.img.addEventListener(type, callback);
    }
}

class GalleryDisplayHandler {
    constructor() {
        this.div = document.querySelector('#display');
        this.img = document.querySelector('#display__image');
    }

    toggleDisplayOff() {
        this.div.classList.remove('display__container');
        this.div.classList.add('display-none');
    }

    toggleDisplayOn() {
        this.div.classList.remove('display-none');
        this.div.classList.add('display__container');
    }

    toggleImageOff() {
        this.img.classList.remove('display__image');
        this.img.classList.add('display-none');
    }

    toggleImageOn() {
        this.img.classList.remove('display-none');
        this.img.classList.add('display__image');
    }

    setImageSource(src) {
        this.img.setAttribute('src', src);
    }

    addEventListener(type, callback) {
        this.img.addEventListener(type, callback);
    }
}

function hideImageItem(event) {
    let gdh = new GalleryDisplayHandler();
    gdh.toggleImageOff();
    gdh.toggleDisplayOff();
    gdh.setImageSource('');
}

function displayImageItem(event) {
    let gdh = new GalleryDisplayHandler();
    gdh.toggleImageOn();
    gdh.toggleDisplayOn();
    gdh.setImageSource(event.target.src);
    gdh.addEventListener('click', hideImageItem);
}

function buildGalleryList(data) {
    let gallery = document.querySelector('.gallery');
    for (let object of data) {
        let gib = new GalleryItemBuilder();
        gib.setAttribute(object);
        gib.addEventListener('click', displayImageItem);
        gib.appendChild(gallery);
    }
}

fetch('/assets/data/jira.json')
    .then((response) => response.json())
    .then((data) => buildGalleryList(data))
    .catch((error) => console.log(error));
