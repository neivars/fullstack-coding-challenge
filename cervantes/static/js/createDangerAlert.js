// Error alert component
function createDangerAlert(text) {
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-danger';
    alertDiv.innerText = text;
    return alertDiv;
}