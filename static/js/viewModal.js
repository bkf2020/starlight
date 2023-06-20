const viewHintClusterBtns = document.getElementsByClassName("viewHintCluster");
for(let i = 0; i < viewHintClusterBtns.length; i++) {
    viewHintClusterBtns[i].addEventListener("click", async function (event) {
        if(document.getElementById("clusterModelOverlay").classList.contains("visible")) return;
        try {
            document.getElementById("clusterModal").replaceChildren();
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
        if(document.getElementById("clusterModelOverlay").classList.contains("visible")) return;
        try {
            document.getElementById("clusterModal").replaceChildren();
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
const viewSimilarProblemsBtns = document.getElementsByClassName("viewSimilarProblems");
for(let i = 0; i < viewSimilarProblemsBtns.length; i++) {
    viewSimilarProblemsBtns[i].addEventListener("click", async function (event) {
        if(document.getElementById("clusterModelOverlay").classList.contains("visibleSlower")) return;
        try {
            document.getElementById("clusterModal").replaceChildren();
            const problemId = event.target.getAttribute("problemid").toString(), clusterId = event.target.getAttribute("clusterid").toString();
            const similarProblems = await fetch("/problems/problemsSimilarInsights/?type=insight&problem=" + problemId + "&cluster=" + clusterId + "&json=true");
            const similarProblemsData = await similarProblems.json();
            var listProblems = document.createElement("ul");
            for(var idx in similarProblemsData["problems"]) {
                var problem = similarProblemsData["problems"][idx];
                if(problem["id"] == similarProblemsData["firstProblem"]["id"]) {
                    continue;
                }
                var problemItem = document.createElement("li");
                var problemLink = document.createElement("a");
                problemLink.href = problem["link"];
                problemLink.appendChild(document.createTextNode(problem["name"]));
                problemItem.appendChild(problemLink);
                var sharedInsightsDetails = document.createElement("details");
                var sharedInsightsSummary = document.createElement("summary");
                sharedInsightsSummary.appendChild(document.createTextNode("Shared similar insights from this problem:"));
                var sharedInsightsList = document.createElement("ul");
                try {
                    const sharedInsights = await fetch("/problems/sharedInsights/?type=group&insightProblem=" + problemId + "&otherProblem=" + problem["id"].toString() + "&cluster=" + clusterId + "&json=true");
                    const sharedInsightsData = await sharedInsights.json();
                    for(var idx in sharedInsightsData["shared_insights"]) {
                        var sharedInsight = sharedInsightsData["shared_insights"][idx];
                        var sharedInsightPoint = document.createElement("li");
                        sharedInsightPoint.appendChild(document.createTextNode(sharedInsight.text));
                        sharedInsightsList.appendChild(sharedInsightPoint);
                    }
                } catch (error) {
                    console.error("Error:", error);
                }
                sharedInsightsDetails.append(sharedInsightsSummary);
                sharedInsightsDetails.append(sharedInsightsList);
                problemItem.appendChild(sharedInsightsDetails);
                listProblems.appendChild(problemItem);
            }
            var description = document.createElement("h3");
            description.appendChild(document.createTextNode("Viewing all problems with insights similar to any one in this cluster:"));
            document.getElementById("clusterModal").append(description);
            document.getElementById("clusterModal").append(listProblems);
            document.getElementById("clusterModelOverlay").classList.add("visibleSlower");
        } catch (error) {
            console.error("Error:", error);
        }
    });
}