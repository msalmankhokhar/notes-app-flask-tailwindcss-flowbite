const themeToggleButton = document.getElementById('theme-toggle');
const themeToggleIcon = document.getElementById('theme-toggle-icon');
const headers = { Accept : 'application/json' }

function toggleDarkMode() {
    const htmlElement = document.documentElement;
    if (htmlElement.hasAttribute('data-mode')) {
        htmlElement.removeAttribute('data-mode')
        return false;
    } else {
        htmlElement.setAttribute('data-mode', 'dark');
        return true
    }
}

themeToggleButton.addEventListener('click', async () => {
    let currentTheme = toggleDarkMode();
    // if(currentTheme){ 
    //     themeToggleIcon.classList.replace('fa-moon', 'fa-sun') 
    // } else { 
    //     themeToggleIcon.classList.replace('fa-sun', 'fa-moon') 
    // }
    fetch(`/theme?value=${currentTheme}`, { headers: headers }).catch((error)=>{
        console.log(error)
    });
});