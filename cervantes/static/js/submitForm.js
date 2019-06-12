const translateForm = document.querySelector('#translate-form');
const translationHistory = document.querySelector('#translation-history');

translateForm.addEventListener('submit', function () {
    translationHistory.innerHTML = null;
    translationHistory.appendChild(createLoadingSpinner());
});