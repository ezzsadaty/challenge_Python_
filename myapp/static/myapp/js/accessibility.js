
function adjustFontSize(size) {
    document.body.classList.remove('small-font', 'large-font');
    if (size === 'increase') {
        document.body.classList.add('large-font');
        localStorage.setItem('fontSize', 'large-font');
    } else if (size === 'decrease') {
        document.body.classList.add('small-font');
        localStorage.setItem('fontSize', 'small-font');
    } else {
        localStorage.setItem('fontSize', '');
    }
}

// Apply saved font size preference on page load
document.addEventListener('DOMContentLoaded', () => {
    const savedFontSize = localStorage.getItem('fontSize');
    if (savedFontSize) {
        document.body.classList.add(savedFontSize);
    }
});


function toggleHighContrast() {
    document.body.classList.toggle('high-contrast');
    if (document.body.classList.contains('high-contrast')) {
        localStorage.setItem('highContrast', 'enabled');
    } else {
        localStorage.removeItem('highContrast');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const highContrastEnabled = localStorage.getItem('highContrast');
    if (highContrastEnabled === 'enabled') {
        document.body.classList.add('high-contrast');
    }
});
