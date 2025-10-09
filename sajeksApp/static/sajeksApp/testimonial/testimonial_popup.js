// NOTE: This file now relies on getCookie and setCookie from cookie_consent.js

// ------------------------------------------------------
// CORE TESTIMONIAL LOGIC - This is the function the cookie script will call
// ------------------------------------------------------
function startTestimonialLogic() {
    // This function must be globally available (not inside a DOMContentLoaded block)
    const modal = document.getElementById('testimonial-popup-modal');
    const hasRated = getCookie('has_rated'); // Requires getCookie() from the other file
    
    if (modal && !hasRated) {
        const intervalTime = 10000; // 2 minutes
        
        console.log("Starting testimonial timer (2 min delay)...");
        let timer = setInterval(function() {
            clearInterval(timer); 
            modal.style.display = 'flex'; 
        }, intervalTime);
    } else if (hasRated) {
        console.log("Testimonial popup suppressed: User has already rated.");
    }
}

// Function to handle the actual AJAX submission (Keep this separate)
function handleTestimonialSubmission(event) {
    // ... (All the submission logic, which remains the same)
}

function closeTestimonialPopup() {
    document.getElementById('testimonial-popup-modal').style.display = 'none';
}

// Attach submission handler when the DOM is ready (needed for the form)
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('#testimonial-popup-modal form');
    if (form) {
        form.addEventListener('submit', handleTestimonialSubmission);
    }
});

// IMPORTANT: The startTestimonialLogic() function is now called externally 
// by cookie_consent.js, NOT by this file's DOMContentLoaded event.


// // your_app/static/js/popup.js

// document.addEventListener('DOMContentLoaded', function() {
//     const modal = document.getElementById('testimonial-popup-modal');
//     // Key to prevent the popup from showing multiple times per browser session
//     const hasBeenShown = sessionStorage.getItem('testimonial_popup_shown');
    
//     // 2 minutes in milliseconds
//     const intervalTime = 120000; 

//     if (modal && !hasBeenShown) {
//         let timer = setInterval(function() {
//             clearInterval(timer); // Stop the timer once the time is reached
            
//             // Show the modal
//             modal.style.display = 'flex'; 
            
//             // Note: We set the session storage flag when the user CLOSES the modal
//             // via the closeTestimonialPopup function, not when it opens.

//         }, intervalTime);
//     }
// });

// function closeTestimonialPopup() {
//     document.getElementById('testimonial-popup-modal').style.display = 'none';
//     // Set flag so the modal won't show again in this session
//     sessionStorage.setItem('testimonial_popup_shown', 'true');
// }


// your_app/static/sajeksApp/testimonial/testimonial_popup.js

// document.addEventListener('DOMContentLoaded', function() {
//     const modal = document.getElementById('testimonial-popup-modal');
//     // REMOVE this line: const hasBeenShown = sessionStorage.getItem('testimonial_popup_shown');

//     const intervalTime = 120000; // 2 minutes

//     // Change the if condition to only check for the modal element
//     if (modal) { 
//         let timer = setInterval(function() {
//             clearInterval(timer); 
//             modal.style.display = 'flex'; 
//         }, intervalTime);
//     }
// });

// // You can still keep this function, but it only hides the modal now:
// function closeTestimonialPopup() {
//     document.getElementById('testimonial-popup-modal').style.display = 'none';
//     // REMOVE this line: sessionStorage.setItem('testimonial_popup_shown', 'true'); 
// }