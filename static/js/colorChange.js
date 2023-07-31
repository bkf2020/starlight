function setLightMode() {
    document.getElementById("colorModeInd").src = "/static/img/darkmode.png";
    document.getElementById("lightDarkStylesheet").href = "/static/css/main-light.css";
    if(document.getElementById("lightDarkModalStylesheet")) {
        document.getElementById("lightDarkModalStylesheet").href = "/static/css/modal-light.css";
    }
    localStorage.setItem("theme", "light");
}
function setDarkMode() {
    document.getElementById("colorModeInd").src = "/static/img/lightmode.png";
    document.getElementById("lightDarkStylesheet").href = "/static/css/main-dark.css";
    if(document.getElementById("lightDarkModalStylesheet")) {
        document.getElementById("lightDarkModalStylesheet").href = "/static/css/modal-dark.css";
    }
    localStorage.setItem("theme", "dark");
}
document.addEventListener("DOMContentLoaded", function(event) {
    if(localStorage.getItem("theme") === null) {
        if(window.matchMedia("(prefers-color-scheme: dark)").matches) {
            setDarkMode();
        } else {
            setLightMode();
        }
    } else {
        if(localStorage.getItem("theme") === "light") {
            setLightMode();
        } else {
            setDarkMode();
        } 
    }
});
document.getElementById("colorModeIndBtn").addEventListener("click", function() {
    if(localStorage.getItem("theme") === "dark") {
        setLightMode();
    } else {
        setDarkMode();
    }
});
window.addEventListener("storage", function(event) {
    if(localStorage.getItem("theme") === "light") {
        setLightMode();
    } else {
        setDarkMode();
    } 
});