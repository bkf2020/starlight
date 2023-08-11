function setLightMode() {
    if(document.documentElement.classList.contains("dark")) {
        document.documentElement.classList.remove("dark");
    }
    localStorage.setItem("theme", "light");
}
function setDarkMode() {
    document.documentElement.classList.add("dark");
    localStorage.setItem("theme", "dark");
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