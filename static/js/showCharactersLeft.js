if(document.getElementById("id_text") === null) {
    if(document.getElementById("id_hint") === null) {
        document.getElementById("id_insight").addEventListener("input", function(event) {
            document.getElementById("charactersLeft").innerText = 300 - document.getElementById("id_insight").value.length;
        });
    } else {
        document.getElementById("id_hint").addEventListener("input", function(event) {
            document.getElementById("charactersLeft").innerText = 300 - document.getElementById("id_hint").value.length;
        });
    }
} else {
    document.getElementById("id_text").addEventListener("input", function(event) {
        document.getElementById("charactersLeft").innerText = 300 - document.getElementById("id_text").value.length;
    });
}
window.addEventListener("DOMContentLoaded", function(event) {
    if(document.getElementById("id_text") === null) {
        if(document.getElementById("id_hint") === null) {
            document.getElementById("charactersLeft").innerText = 300 - document.getElementById("id_insight").value.length;
        } else {
            document.getElementById("charactersLeft").innerText = 300 - document.getElementById("id_hint").value.length;
        }
    } else {
        document.getElementById("charactersLeft").innerText = 300 - document.getElementById("id_text").value.length;
    }
});