const viewHintClusterBtns = document.getElementsByClassName("viewHintCluster");
for(let i = 0; i < viewHintClusterBtns.length; i++) {
    viewHintClusterBtns[i].addEventListener("click", async function (event) {
        try {
            console.log(event.target);
            console.log(event.target.getAttribute("problemid"));
            const hintCluster = await fetch("/problems/cluster/?type=hint&problem=" + event.target.getAttribute("problemid").toString() + "&cluster=" + event.target.getAttribute("clusterid").toString() + "&json=true");
            const hintClusterData = await hintCluster.json();
            var listHints = document.createElement("ul");
            for(var idx in hintClusterData["hints"]) {
                var hint = hintClusterData["hints"][idx];
                var hintItem = document.createElement("li");
                hintItem.innerText = hint["text"];
                listHints.appendChild(hintItem);
            }
            var description = document.createElement("h3");
            description.appendChild(document.createTextNode("Viewing all hints of this cluster:"));
            document.getElementById("clusterModal").append(description);
            document.getElementById("clusterModal").append(listHints);
            document.getElementById("clusterModelOverlay").classList.add("visible");
        } catch (error) {
            console.error("Error:", error);
        }
    });
}
const viewInsightClusterBtns = document.getElementsByClassName("viewInsightCluster");
for(let i = 0; i < viewInsightClusterBtns.length; i++) {
    viewInsightClusterBtns[i].addEventListener("click", async function (event) {
        try {
            const insightCluster = await fetch("/problems/cluster/?type=insight&problem=" + event.target.getAttribute("problemid").toString() + "&cluster=" + event.target.getAttribute("clusterid").toString() + "&json=true");
            const insightClusterData = await insightCluster.json();
            var listInsights = document.createElement("ul");
            for(var idx in insightClusterData["insights"]) {
                var insight = insightClusterData["insights"][idx];
                var insightItem = document.createElement("li");
                insightItem.innerText = insight["text"];
                listInsights.appendChild(insightItem);
            }
            var description = document.createElement("h3");
            description.appendChild(document.createTextNode("Viewing all insights of this cluster:"));
            document.getElementById("clusterModal").append(description);
            document.getElementById("clusterModal").append(listInsights);
            document.getElementById("clusterModelOverlay").classList.add("visible");
        } catch (error) {
            console.error("Error:", error);
        }
    });
}