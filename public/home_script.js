// public/home_script.js (or public/script.js)

// Google Translate initialization function - must be globally accessible
function googleTranslateElementInit() {
    new google.translate.TranslateElement(
        { pageLanguage: 'en', includedLanguages: 'en,hi,gu,bn,ta,te,ml,kn,pa,mr', layout: google.translate.TranslateElement.InlineLayout.SIMPLE },
        'google_translate_element'
    );
}

// Function to re-insert and re-initialize Google Translate
function loadGoogleTranslate() {
    const container = document.querySelector('.language-selector-container');
    let translateDiv = document.getElementById('google_translate_element');

    // Remove existing translate elements and scripts
    if (translateDiv) {
        translateDiv.remove();
    }
    const existingScript = document.querySelector('script[src*="//translate.google.com/translate_a/element.js"]');
    if (existingScript) {
        existingScript.remove();
    }

    // Re-create the div
    translateDiv = document.createElement('div');
    translateDiv.id = 'google_translate_element';
    container.appendChild(translateDiv);

    // Re-create and append the Google Translate script
    const script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = '//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';
    document.body.appendChild(script);
}

// Add a pageshow listener to handle back/forward cache and clear hash
window.addEventListener('pageshow', function(event) {
    // Ensure the body is visible whether it's a fresh load or from bfcache
    document.body.style.opacity = '1';
    document.body.style.transition = 'opacity 0.5s ease-in';
    document.body.classList.add('loaded');

    // Reload/re-initialize Google Translate whenever the page is shown
    // This is crucial for bfcache
    loadGoogleTranslate();

    // --- Implement a setInterval to repeatedly clear the hash (for Google Translate's hash issue) ---
    let hashClearInterval;
    const checkDuration = 5000; // Total duration to keep checking (5 seconds)
    const checkInterval = 100; // How often to check (every 100ms)
    let elapsed = 0;

    hashClearInterval = setInterval(() => {
        // If a hash exists in the URL, remove it
        if (window.location.hash) {
            // Using history.replaceState keeps the browser history clean
            // and prevents the back button from going through hash changes.
            history.replaceState('', document.title, window.location.pathname + window.location.search);
        }

        elapsed += checkInterval;
        // Stop checking after the specified duration
        if (elapsed >= checkDuration) {
            clearInterval(hashClearInterval);
        }
    }, checkInterval);
    // --- END hash clear interval ---
});

// Initial DOMContentLoaded for other scripts (animations, etc.)
document.addEventListener('DOMContentLoaded', function() {
    // Initial fade-in trigger
    document.body.classList.add('loaded');

    // Animation observer logic (as already present in your files)
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    document.querySelectorAll('.feature').forEach(feature => {
        feature.style.opacity = '0';
        feature.style.transform = 'translateY(20px)';
        feature.style.transition = 'all 0.6s ease-out';
        observer.observe(feature);
    });

    // If there are .info-item elements (from home.html)
    document.querySelectorAll('.info-item').forEach(item => {
        item.style.opacity = '0';
        item.style.transform = 'translateY(20px)';
        item.style.transition = 'all 0.6s ease-out 0.2s';
        observer.observe(item);
    });
});