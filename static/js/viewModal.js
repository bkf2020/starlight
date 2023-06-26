async function populateHintPage(page, problemId, clusterId) {
    try {
        const hintCluster = await fetch("/problems/cluster/?type=hint&problem=" + problemId.toString() + "&cluster=" + clusterId.toString() + "&json=true&page=" + page.toString());
        const hintClusterData = await hintCluster.json();
        document.getElementById("clusterModalContent").replaceChildren();
        var listHints = document.createElement("ul");
        for(var idx in hintClusterData["new_page_obj"]["hints"]) {
            var hint = hintClusterData["new_page_obj"]["hints"][idx];
            var hintItem = document.createElement("li");
            hintItem.innerText = hint["text"];
            listHints.appendChild(hintItem);
        }
        var description = document.createElement("h3");
        description.appendChild(document.createTextNode("Viewing all hints of this cluster:"));
        document.getElementById("clusterModalContent").append(description);
        document.getElementById("clusterModalContent").append(listHints);
        var paginationDiv = document.createElement("div");
        if(hintClusterData["new_page_obj"]["has_previous"]) {
            var before = document.createElement("a");
            before.href = "#";
            before.appendChild(document.createTextNode("\u{02190}"));
            before.addEventListener('click', () => {
                renderHintPage(page - 1, problemId, clusterId, false);
            });
            before.classList.add("paginationLink");
            before.classList.add("paginationArrow");
            paginationDiv.appendChild(before);
        }
        var spanInformation = document.createElement("span");
        spanInformation.appendChild(document.createTextNode("Page " + hintClusterData["new_page_obj"]["number"].toString() + " of " + hintClusterData["new_page_obj"]["num_pages"]));
        paginationDiv.append(spanInformation);
        if(hintClusterData["new_page_obj"]["has_next"]) {
            var after = document.createElement("a");
            after.href = "#";
            after.appendChild(document.createTextNode("\u{02192}"));
            after.addEventListener('click', () => {
                renderHintPage(page + 1, problemId, clusterId, false);
            });
            after.classList.add("paginationLink");
            after.classList.add("paginationArrow");
            paginationDiv.appendChild(after);
        }
        document.getElementById("clusterModalContent").appendChild(paginationDiv);
    } catch (error) {
        console.error("Error:", error);
    }
}
function renderHintPage(page, problemId, clusterId, firstTime) {
    if(firstTime) {
        populateHintPage(page, problemId, clusterId);
        return;
    }
    document.getElementById("clusterModalContent").classList.remove("fade");
    setTimeout(() => {
        requestAnimationFrame(() => {
            populateHintPage(page, problemId, clusterId);
            document.getElementById("clusterModalContent").classList.add("fade");
        });
    }, 100);
}

const viewHintClusterBtns = document.getElementsByClassName("viewHintCluster");
for(let i = 0; i < viewHintClusterBtns.length; i++) {
    viewHintClusterBtns[i].addEventListener("click", async function (event) {
        if(document.getElementById("clusterModelOverlay").classList.contains("visible")) return;
        renderHintPage(1, event.target.getAttribute("problemid"), event.target.getAttribute("clusterid"), true);
        document.getElementById("clusterModelOverlay").classList.add("visible");
    });
}

async function populateInsightPage(page, problemId, clusterId) {
    try {
        const insightCluster = await fetch("/problems/cluster/?type=insight&problem=" + problemId.toString() + "&cluster=" + clusterId.toString() + "&json=true&page=" + page.toString());
        const insightClusterData = await insightCluster.json();
        document.getElementById("clusterModalContent").replaceChildren();
        var listInsights = document.createElement("ul");
        for(var idx in insightClusterData["new_page_obj"]["insights"]) {
            var insight = insightClusterData["new_page_obj"]["insights"][idx];
            var insightItem = document.createElement("li");
            insightItem.innerText = insight["text"];
            listInsights.appendChild(insightItem);
        }
        var description = document.createElement("h3");
        description.appendChild(document.createTextNode("Viewing all insights of this cluster:"));
        document.getElementById("clusterModalContent").append(description);
        document.getElementById("clusterModalContent").append(listInsights);
        var paginationDiv = document.createElement("div");
        if(insightClusterData["new_page_obj"]["has_previous"]) {
            var before = document.createElement("a");
            before.href = "#";
            before.appendChild(document.createTextNode("\u{02190}"));
            before.addEventListener('click', () => {
                renderInsightPage(page - 1, problemId, clusterId, false);
            });
            before.classList.add("paginationLink");
            before.classList.add("paginationArrow");
            paginationDiv.appendChild(before);
        }
        var spanInformation = document.createElement("span");
        spanInformation.appendChild(document.createTextNode("Page " + insightClusterData["new_page_obj"]["number"].toString() + " of " + insightClusterData["new_page_obj"]["num_pages"]));
        paginationDiv.append(spanInformation);
        if(insightClusterData["new_page_obj"]["has_next"]) {
            var after = document.createElement("a");
            after.href = "#";
            after.appendChild(document.createTextNode("\u{02192}"));
            after.addEventListener('click', () => {
                renderInsightPage(page + 1, problemId, clusterId, false);
            });
            after.classList.add("paginationLink");
            after.classList.add("paginationArrow");
            paginationDiv.appendChild(after);
        }
        document.getElementById("clusterModalContent").appendChild(paginationDiv);
    } catch {
        console.error("Error:", error);
    }
}

function renderInsightPage(page, problemId, clusterId, firstTime) {
    if(firstTime) {
        populateInsightPage(page, problemId, clusterId);
        return;
    }
    document.getElementById("clusterModalContent").classList.remove("fade");
    setTimeout(() => {
        requestAnimationFrame(() => {
            populateInsightPage(page, problemId, clusterId);
            document.getElementById("clusterModalContent").classList.add("fade");
        });
    }, 100);
}
const viewInsightClusterBtns = document.getElementsByClassName("viewInsightCluster");
for(let i = 0; i < viewInsightClusterBtns.length; i++) {
    viewInsightClusterBtns[i].addEventListener("click", async function (event) {
        if(document.getElementById("clusterModelOverlay").classList.contains("visible")) return;
        renderInsightPage(1, event.target.getAttribute("problemid"), event.target.getAttribute("clusterid"), true);
        document.getElementById("clusterModelOverlay").classList.add("visible");
    });
}

async function populateProblemPage(page, problemId, clusterId, firstTime, button) {
    try {
        document.getElementById("clusterModal").style.height = "calc(" + document.getElementById("clusterModal").offsetHeight.toString() + "px" + " - 2em)";
        document.getElementById("clusterModalContent").replaceChildren();
        problemId = problemId.toString(); clusterId = clusterId.toString();
        const similarProblems = await fetch("/problems/problemsSimilarInsights/?type=group&problem=" + problemId + "&cluster=" + clusterId + "&page=" + page.toString() + "&json=true");
        const similarProblemsData = await similarProblems.json();
        var listProblems = document.createElement("ul");
        for(var idx in similarProblemsData["new_page_obj"]["problems"]) {
            var problem = similarProblemsData["new_page_obj"]["problems"][idx];
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
        document.getElementById("clusterModalContent").append(description);
        document.getElementById("clusterModalContent").append(listProblems);
        var paginationDiv = document.createElement("div");
        if(similarProblemsData["new_page_obj"]["has_previous"]) {
            var before = document.createElement("a");
            before.href = "#";
            before.appendChild(document.createTextNode("\u{02190}"));
            before.addEventListener('click', () => {
                renderProblemPage(page - 1, problemId, clusterId, false, button);
            });
            before.classList.add("paginationLink");
            before.classList.add("paginationArrow");
            paginationDiv.appendChild(before);
        }
        var spanInformation = document.createElement("span");
        spanInformation.appendChild(document.createTextNode("Page " + similarProblemsData["new_page_obj"]["number"].toString() + " of " + similarProblemsData["new_page_obj"]["num_pages"]));
        paginationDiv.append(spanInformation);
        if(similarProblemsData["new_page_obj"]["has_next"]) {
            var after = document.createElement("a");
            after.href = "#";
            after.appendChild(document.createTextNode("\u{02192}"));
            after.addEventListener('click', () => {
                renderProblemPage(page + 1, problemId, clusterId, false, button);
            });
            after.classList.add("paginationLink");
            after.classList.add("paginationArrow");
            paginationDiv.appendChild(after);
        }
        document.getElementById("clusterModalContent").appendChild(paginationDiv);
        document.getElementById("clusterModal").style.height = null;
        if(firstTime) document.getElementById("clusterModelOverlay").classList.add("visibleSlower");
        else document.getElementById("clusterModalContent").classList.add("fade");
        console.log(button);
        button.disabled = false;
    } catch (error) {
        console.error("Error:", error);
    }
}
function renderProblemPage(page, problemId, clusterId, firstTime, button) {
    if(firstTime) {
        populateProblemPage(page, problemId, clusterId, firstTime, button);
        return;
    }
    document.getElementById("clusterModalContent").classList.remove("fade");
    setTimeout(() => {
        requestAnimationFrame(() => {
            populateProblemPage(page, problemId, clusterId, firstTime, button);
        });
    }, 100);
}
const viewSimilarProblemsBtns = document.getElementsByClassName("viewSimilarProblems");
for(let i = 0; i < viewSimilarProblemsBtns.length; i++) {
    viewSimilarProblemsBtns[i].addEventListener("click", function (event) {
        if(document.getElementById("clusterModelOverlay").classList.contains("visibleSlower")) return;
        event.target.disabled = true;
        renderProblemPage(1, event.target.getAttribute("problemid"), event.target.getAttribute("clusterid"), true, event.target);
    });
}