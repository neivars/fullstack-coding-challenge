// Get the index page loaded first (for performance) then grab the
// translation history asynchronously

// Wait for the DOM to load
document.addEventListener('DOMContentLoaded', fetchTranslations);

function fetchTranslations() {
    const { origin } = window.location;
    const translationHistoryDiv = document.querySelector('#translation-history');

    fetch(`${origin}/translations/`
    ).then(response => {
        if (response.status !== 200) {
            document.querySelector('#alerts').appendChild(
                createDangerAlert('Uh oh - Unbabel isn\'t picking up the phone. Try again later, please.')
            );
            return;
        }

        return response.text();
    }).then(text => translationHistoryDiv.innerHTML = text
    ).catch(error => {
        console.error(error);
        document.querySelector('#alerts').appendChild(
            createDangerAlert('Uh oh - Unbabel isn\'t picking up the phone. Try again later, please.')
        );
    });
}