// Loading spinner component
function createLoadingSpinner() {
    const loadingSpinner = document.createElement('div');
    loadingSpinner.id = 'loading-spinner';
    loadingSpinner.className = 'spinner-border text-primary';
    loadingSpinner.style = "height: 4rem; width: 4rem;"
    loadingSpinner.attributes['role'] = "status";

    const screenReaderSpan = document.createElement('span');
    screenReaderSpan.className = 'sr-only';
    screenReaderSpan.innerText = 'Loading...';

    loadingSpinner.appendChild(screenReaderSpan);

    return loadingSpinner;
}