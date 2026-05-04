// public/home_script.js (or public/script.js)

// Google Translate initialization function - must be globally accessible
function googleTranslateElementInit() {
    new google.translate.TranslateElement(
        { pageLanguage: 'en', includedLanguages: 'en,hi,gu,bn,ta,te,ml,kn,pa,mr', layout: google.translate.TranslateElement.InlineLayout.SIMPLE },
        'google_translate_element'
    );
}

window.addEventListener('pageshow', function(event) {
    // Ensure the body is visible whether it's a fresh load or from bfcache
    document.body.style.opacity = '1';
    document.body.style.transition = 'opacity 0.5s ease-in';
    document.body.classList.add('loaded');
});