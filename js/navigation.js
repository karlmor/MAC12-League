function initMobileNavigation() {
    const mobileNavToggle = document.querySelector('.mobile-nav-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (mobileNavToggle && navLinks) {
        mobileNavToggle.addEventListener('click', function() {
            navLinks.classList.toggle('active');
            mobileNavToggle.setAttribute('aria-expanded', 
                navLinks.classList.contains('active'));
        });

        // Close mobile menu when clicking outside
        document.addEventListener('click', function(event) {
            if (!event.target.closest('.nav-links') && 
                !event.target.closest('.mobile-nav-toggle')) {
                navLinks.classList.remove('active');
                mobileNavToggle.setAttribute('aria-expanded', 'false');
            }
        });
    }
}

// Initialize when the DOM is loaded
document.addEventListener('DOMContentLoaded', initMobileNavigation);

// Initialize when navigating between pages (for browsers that support this)
if (typeof window.onpageshow !== 'undefined') {
    window.onpageshow = function(event) {
        if (event.persisted) {
            initMobileNavigation();
        }
    };
} 