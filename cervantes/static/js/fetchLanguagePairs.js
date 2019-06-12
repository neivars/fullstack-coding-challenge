// Get the index page loaded first (for performance) then grab the
// available language pairs to populate the selects

// Wait for the DOM to load
document.addEventListener('DOMContentLoaded', embueLanguageSelects);

/* Whenever the #source-language select changes value, the #target-language
select needs to update its list as well. This function will set some
listeners and update the option elements accordingly. */
async function embueLanguageSelects() {
    const sourceLanguageSelect = document.querySelector('#source-language');
    const targetLanguageSelect = document.querySelector('#target-language');

    const languagePairs = await fetchLanguagePairs();

    // Function that populates the #target-language select with the
    // correct options
    function updateTargetLanguageSelect(sourceLanguage) {
        targetLanguageSelect.innerHTML = null;

        for (let targetLang of languageMappings[sourceLanguage]['target_languages']) {
            const option = new Option(
                targetLang['name'],
                targetLang['shortname'],
                // Default selection is Spanish (if available)
                targetLang['shortname'] === 'es',
                targetLang['shortname'] === 'es'
            );
            targetLanguageSelect.appendChild(option);
        }
    }

    /* Take the array of languagePairs and apply some functional magic to
    produce an object with the source languages as keys and a corresponding
    array of target languages. This will make it easier to update the selects. */
    const languageMappings = languagePairs.reduce(function (mapping, langPair, _i, currentArray) {
        const source_language = langPair.lang_pair.source_language;

        if (!mapping.hasOwnProperty(source_language.shortname)) {
            mapping[source_language.shortname] = {
                name: source_language.name,
                target_languages: currentArray.filter(function (innerLangPair) {
                    return innerLangPair.lang_pair.source_language.shortname === source_language.shortname;
                }).map(function (innerLangPair) {
                    return innerLangPair.lang_pair.target_language;
                })
            };
        }

        return mapping;
    }, {});

    for (let sourceLang in languageMappings) {
        const option = new Option(
            languageMappings[sourceLang]['name'],
            sourceLang,
            // Default selection is English
            sourceLang === 'en',
            sourceLang === 'en'
        );
        sourceLanguageSelect.appendChild(option);
    }

    // Seed the #target-language select
    updateTargetLanguageSelect('en');

    sourceLanguageSelect.removeAttribute('disabled');
    targetLanguageSelect.removeAttribute('disabled');

    // Whenever the #source-language select changes, update the
    // #target-language select with the corresponding options
    sourceLanguageSelect.addEventListener('change', function (event) {
        updateTargetLanguageSelect(event.target.value);
    });
}

// Async call to the server to get the latest language pairs
function fetchLanguagePairs() {
    const { origin } = window.location;

    return fetch(`${origin}/translations/language_pairs`
    ).then(response => {
        if (response.status !== 200) {
            document.querySelector('#alerts').appendChild(
                createDangerAlert('Uh oh - Unbabel isn\'t picking up the phone. Try again later, please.')
            );
            return;
        }

        return response.json();
    }).then(languagePairs => languagePairs
    ).catch(error => {
        console.error(error);
        document.querySelector('#alerts').appendChild(
            createDangerAlert('Uh oh - Unbabel isn\'t picking up the phone. Try again later, please.')
        );
    });
}