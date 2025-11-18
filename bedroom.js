document.addEventListener('DOMContentLoaded', function () {
    const toggleBtn = document.getElementById('toggle-btn');
    const screenContainer = document.querySelector('.screen-container');

    toggleBtn.addEventListener('click', function () {
        screenContainer.classList.toggle('fullscreen');
        toggleBtn.classList.toggle('fullscreen-btn');
    });
});
