let BOOK_PREFIX = "";

if (window.isTemplate) {
    BOOK_PREFIX = 'philosophy_friends/lacan/FR/';
}

class ComicReader {
    constructor() {
        this.images = [];
        this.currentMode = 'single'; // 'gallery' or 'single' - default changed to single page
        this.currentPage = 0;
    }

    init() {
        this.createModeToggle();
        this.render();
    }

    setPages(pages) {
        this.images = pages;
    }

    createModeToggle() {
        const toggleContainer = document.createElement('div');
        toggleContainer.className = 'mode-toggle';

        const galleryBtn = document.createElement('button');
        galleryBtn.textContent = 'Gallery View';
        galleryBtn.className = `mode-btn ${this.currentMode === 'gallery' ? 'active' : ''}`;

        const singleBtn = document.createElement('button');
        singleBtn.textContent = 'Page View';
        singleBtn.className = `mode-btn ${this.currentMode === 'single' ? 'active' : ''}`;

        galleryBtn.onclick = () => this.switchMode('gallery');
        singleBtn.onclick = () => this.switchMode('single');

        toggleContainer.appendChild(galleryBtn);
        toggleContainer.appendChild(singleBtn);
        document.body.appendChild(toggleContainer);
    }

    switchMode(mode) {
        this.currentMode = mode;
        if (mode === 'single') {
            this.currentPage = 0;
        }
        this.render();
    }

    render() {
        const container = document.querySelector('.container');
        if (!container) return;

        container.innerHTML = '';

        if (this.currentMode === 'gallery') {
            this.renderGallery(container);
        } else {
            this.renderSinglePage(container);
        }
    }

    renderGallery(container) {
        container.classList.add('gallery-view');
        this.images.forEach((imageSrc, index) => {
            const img = document.createElement('img');
            img.src = imageSrc;
            img.className = 'comic-page gallery-page';
            // Gallery images are not clickable
            container.appendChild(img);
        });
    }

    renderSinglePage(container) {
        // Navigation buttons
        const navContainer = document.createElement('div');
        navContainer.className = 'nav-container';

        const prevBtn = document.createElement('button');
        prevBtn.textContent = '← Previous';
        prevBtn.className = `nav-btn ${this.currentPage === 0 ? 'disabled' : ''}`;
        prevBtn.onclick = () => {
            if (this.currentPage > 0) {
                this.currentPage--;
                this.render();
            }
        };

        // Page counter
        const counter = document.createElement('div');
        counter.className = 'page-counter';
        counter.textContent = `${this.currentPage + 1} / ${this.images.length}`;

        const nextBtn = document.createElement('button');
        nextBtn.textContent = 'Next →';
        nextBtn.className = `nav-btn ${this.currentPage === this.images.length - 1 ? 'disabled' : ''}`;
        nextBtn.onclick = () => {
            if (this.currentPage < this.images.length - 1) {
                this.currentPage++;
                this.render();
            }
        };

        navContainer.appendChild(prevBtn);
        navContainer.appendChild(counter);
        navContainer.appendChild(nextBtn);
        container.appendChild(navContainer);

        // Current image
        const img = document.createElement('img');
        img.src = this.images[this.currentPage];
        img.className = 'comic-page';
        img.onclick = () => {
            if (this.currentPage < this.images.length - 1) {
                this.currentPage++;
                this.render();
            }
        };
        container.appendChild(img);
    }
}

// Global function to populate pages and initialize reader
let readerInstance;

function populate_pages() {
    if (!readerInstance) {
        readerInstance = new ComicReader();
    }

    // Auto-discover pages by trying to load images until one fails
    const pages = [BOOK_PREFIX + 'wide_pages/cover.png'];
    let currentIndex = 1;
    let attemptsRemaining = 50; // Safety limit to prevent infinite loops

    const tryLoadPage = (pageIndex) => {
        const img = new Image();
        const pagePath = BOOK_PREFIX + `wide_pages/p${pageIndex}.png`;

        img.onload = () => {
            // Page exists, add it and try the next one
            pages.push(pagePath);
            if (attemptsRemaining > 0) {
                attemptsRemaining--;
                tryLoadPage(pageIndex + 1);
            } else {
                // Safety limit reached
                finishLoading();
            }
        };

        img.onerror = () => {
            // Page doesn't exist, stop here
            finishLoading();
        };

        img.src = pagePath;
    };

    const finishLoading = () => {
        readerInstance.setPages(pages);
        readerInstance.init();
    };

    // Start by trying to load page 1 (p1.png)
    tryLoadPage(currentIndex);
}

if (!readerInstance) {
    readerInstance = new ComicReader();
    readerInstance.init();
}

populate_pages();