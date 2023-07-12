document.addEventListener("DOMContentLoaded", function(event) {
    var scrollYPosition = localStorage.getItem("scrollYPosition");
    if(scrollYPosition === null) {
        scrollYPosition = 0;
    }
    window.scrollTo(0, scrollYPosition);
    document.addEventListener("scroll", function(event) {
        localStorage.setItem("scrollYPosition", window.pageYOffset);
    });
});