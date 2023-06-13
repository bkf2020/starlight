const viewHintClusterBtns = document.getElementsByClassName("viewHintCluster");
for(let i = 0; i < viewHintClusterBtns.length; i++) {
    viewHintClusterBtns[i].addEventListener("click", () => {
        openCluster(true);
    });
}

function openCluster(isHint) {
    document.getElementById("clusterModelOverlay").classList.remove("hidden");
}