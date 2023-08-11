function setLightModeIcon() {
    document.getElementById("colorModeInd").src = "/static/img/darkmode.png";
}
function setDarkModeIcon() {
    document.getElementById("colorModeInd").src = "/static/img/lightmode.png";
}
if(localStorage.getItem("theme") === null) {
    if(window.matchMedia("(prefers-color-scheme: dark)").matches) {
        setDarkModeIcon();
    } else {
        setLightModeIcon();
    }
} else {
    if(localStorage.getItem("theme") === "light") {
        setLightModeIcon();
    } else {
        setDarkModeIcon();
    }
}
document.getElementById("colorModeIndBtn").addEventListener("click", function() {
    if(localStorage.getItem("theme") === "dark") {
        setLightMode();
        setLightModeIcon();
    } else {
        setDarkMode();
        setDarkModeIcon();
    }
});
window.addEventListener("storage", function(event) {
    if(localStorage.getItem("theme") === "light") {
        setLightMode();
        setLightModeIcon();
    } else {
        setDarkMode();
        setDarkModeIcon();
    }
});