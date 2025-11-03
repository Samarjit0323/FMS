// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {

    const themeToggle = document.getElementById('theme-toggle');
    const htmlElement = document.documentElement;


    /**
     * Toggles the theme between 'light' and 'dark' and saves the preference.
     */
    function toggleTheme() {
        // Get the current theme
        const currentTheme = htmlElement.getAttribute('data-bs-theme');
        
        // Set the new theme
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        htmlElement.setAttribute('data-bs-theme', newTheme);
        
        // Save the new theme to localStorage
        localStorage.setItem('theme', newTheme);
    }

    // --- Event Listeners ---
    
    // 1. Apply the theme as soon as the page loads
    // (We also do this in the <script> tag in <head> to prevent flickering)
    loadTheme();

    // 2. Add click listener to the toggle button
    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
    }

});