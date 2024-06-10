function setLightMode() {
    if(document.documentElement.classList.contains("dark")) {
        document.documentElement.classList.remove("dark");
    }
    document.documentElement.setAttribute("data-theme", "light");
    localStorage.setItem("theme", "light");
}
function setDarkMode() {
    document.documentElement.classList.add("dark");
    localStorage.setItem("theme", "dark");
    document.documentElement.setAttribute("data-theme", "dark");
}
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
