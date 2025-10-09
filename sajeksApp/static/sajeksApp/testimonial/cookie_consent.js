// Helper function to get a cookie
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

// Function to set a cookie for a given number of days
function setCookie(name, value, days) {
    const d = new Date();
    d.setTime(d.getTime() + (days * 24 * 60 * 60 * 1000));
    const expires = "expires=" + d.toUTCString();
    document.cookie = `${name}=${value}; ${expires}; path=/`;
}

// ------------------------------------------------------
// INITIALIZATION AND CONSENT CHECK 
// ------------------------------------------------------
document.addEventListener('DOMContentLoaded', function() {
    const banner = document.getElementById('cookie-consent-banner');
    const acceptBtn = document.getElementById('accept-cookies-btn');
    
    const consentGiven = getCookie('cookie_consent');

    console.log("Cookie Consent Script Loaded. Status:", consentGiven);

    if (consentGiven) {
        // Consent is present, start the testimonial logic immediately
        if (typeof startTestimonialLogic === 'function') {
             startTestimonialLogic();
        }
    } else if (banner) {
        // No consent, show the banner
        console.log("Displaying cookie consent banner."); 
        banner.style.display = 'block'; 
        
        if (acceptBtn) {
            acceptBtn.addEventListener('click', function() {
                console.log("Accept button clicked. Setting cookie.");
                // 1. Hide the banner
                banner.style.display = 'none';
                
                // 2. Set the consent cookie (for 90 days)
                setCookie('cookie_consent', 'true', 90);
                
                // 3. Start the testimonial timer logic
                if (typeof startTestimonialLogic === 'function') {
                    startTestimonialLogic();
                }
            });
        }
    } else {
        console.error("Cookie banner HTML element not found.");
    }
});