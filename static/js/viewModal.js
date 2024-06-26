var scrollYVal = 0;
async function populateHintPage(page, problemId, clusterId) {
    try {
        const hintCluster = await fetch("/problems/cluster/?type=hint&problem=" + problemId.toString() + "&cluster=" + clusterId.toString() + "&json=true&page=" + page.toString());
        const hintClusterData = await hintCluster.json();
        document.getElementById("clusterModalContent").replaceChildren();
        var listHints = document.createElement("ul");
        listHints.classList.add("list-disc");
        listHints.style.marginLeft = "20px";
        for(var idx in hintClusterData["new_page_obj"]["hints"]) {
            var hint = hintClusterData["new_page_obj"]["hints"][idx];
            var hintItem = document.createElement("li");
            hintItem.innerText = hint["text"] + " by " + hint["username"];
            listHints.appendChild(hintItem);
        }
        var description = document.createElement("h3");
        description.appendChild(document.createTextNode("Viewing all hints of this cluster:"));
        description.classList.add("text-lg", "font-bold");
        document.getElementById("clusterModalContent").append(description);
        if(hintClusterData["new_page_obj"]["hints"].length == 0) {
            var noHintsCurrently = document.createElement("h3");
            noHintsCurrently.appendChild(document.createTextNode("There are no hints currently in this cluster. Perhaps it was recently deleted"));
            description.appendChild(noHintsCurrently);
        }
        document.getElementById("clusterModalContent").append(listHints);
        var paginationDiv = document.createElement("div");
        if(hintClusterData["new_page_obj"]["has_previous"]) {
            var before = document.createElement("a");
            before.href = "#";
            before.appendChild(document.createTextNode("\u{02190}"));
            before.addEventListener('click', () => {
                renderHintPage(page - 1, problemId, clusterId, false);
            });
            before.classList.add("link", "text-blue-700", "dark:text-blue-300", "text-xl");
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
            after.classList.add("link", "text-blue-700", "dark:text-blue-300", "text-xl");
            paginationDiv.appendChild(after);
        }
        document.getElementById("clusterModalContent").appendChild(paginationDiv);
        document.getElementById("clusterModal").classList.add("!bg-base-100");
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
        renderHintPage(1, event.currentTarget.getAttribute("problemid"), event.currentTarget.getAttribute("clusterid"), true);
        scrollYVal = window.pageYOffset;
        document.body.style.top = "-" + scrollYVal.toString() + "px";
        document.body.style.position = "fixed";
        document.getElementById("clusterModelOverlay").classList.add("visible");
    });
}

async function populateInsightPage(page, problemId, clusterId) {
    try {
        const insightCluster = await fetch("/problems/cluster/?type=insight&problem=" + problemId.toString() + "&cluster=" + clusterId.toString() + "&json=true&page=" + page.toString());
        const insightClusterData = await insightCluster.json();
        document.getElementById("clusterModalContent").replaceChildren();
        var listInsights = document.createElement("div");
        for(var idx in insightClusterData["new_page_obj"]["insights"]) {
            var insight = insightClusterData["new_page_obj"]["insights"][idx];
            var insightDiv = document.createElement("div");
            insightDiv.classList.add("card", "max-w-2xl", "bg-base-100", "border", "dark:border-neutral-600", "p-3", "my-2");
            var insightUl = document.createElement("ul");
            insightUl.classList.add("list-disc");
            insightUl.style.marginLeft = "20px";
            var insightItem = document.createElement("li");
            insightItem.innerText = insight["text"] + " by " + insight["username"];
            var similarProblemsInsightList = document.createElement("ul");
            similarProblemsInsightList.classList.add("list-disc");
            similarProblemsInsightList.style.marginLeft = "20px";
            var similarProblemsInsight = document.createElement("li");
            var similarProblemsInsightLink = document.createElement("a");
            similarProblemsInsightLink.classList.add("link", "dark:text-blue-300", "text-blue-700");
            similarProblemsInsightLink.innerText = "View similar problems that share ONLY this INSIGHT";
            similarProblemsInsightLink.href = "/problems/problemsSimilarInsights/?type=individual&insight=" + insight["id"].toString();
            similarProblemsInsightLink.target = "_blank";
            similarProblemsInsightLink.rel = "noopener noreferrer";
            similarProblemsInsight.append(similarProblemsInsightLink);
            similarProblemsInsightList.append(similarProblemsInsight);
            insightItem.append(similarProblemsInsightList);
            insightUl.appendChild(insightItem);
            insightDiv.appendChild(insightUl);
            listInsights.append(insightDiv);
        }
        var description = document.createElement("div");
        var descriptionH3 = document.createElement("h3");
        descriptionH3.style.marginBottom = "0.3em";
        descriptionH3.classList.add("text-lg", "font-bold");
        descriptionH3.appendChild(document.createTextNode("Viewing all insights in this cluster:"));
        description.appendChild(descriptionH3);
        var similarProblemsButton = document.createElement("button");
        similarProblemsButton.classList.add("btn", "btn-small", "btn-outline", "btn-warning", "!min-h-9", "h-9", "mb-2");
        const problemIdAttribute = document.createAttribute("problemid");
        problemIdAttribute.value = problemId;
        similarProblemsButton.setAttributeNode(problemIdAttribute);
        const clusterIdAttribute = document.createAttribute("clusterid");
        clusterIdAttribute.value = clusterId;
        similarProblemsButton.setAttributeNode(clusterIdAttribute);
        similarProblemsButton.innerText = "Problems with insights similar to any one in this cluster";
        similarProblemsButton.addEventListener("click", function (event) {
            var clusterModelOverlay = document.getElementById("clusterModelOverlay");
            if(clusterModelOverlay.classList.contains("visible")) clusterModelOverlay.classList.remove("visible");
            if(clusterModelOverlay.classList.contains("visibleSlower")) clusterModelOverlay.classList.remove("visibleSlower");
            document.body.style.position = '';
            document.body.style.top = '';
            window.scrollTo(0, scrollYVal);
            event.currentTarget.disabled = true;
            scrollYVal = window.pageYOffset;
            document.body.style.top = "-" + scrollYVal.toString() + "px";
            document.body.style.position = "fixed";
            renderProblemPage(1, event.currentTarget.getAttribute("problemid"), event.currentTarget.getAttribute("clusterid"), true, event.currentTarget);
        });
        description.appendChild(similarProblemsButton);
        if(insightClusterData["new_page_obj"]["insights"].length == 0) {
            var noInsightsCurrently = document.createElement("h3");
            noInsightsCurrently.appendChild(document.createTextNode("There are no insights currently in this cluster. Perhaps it was recently deleted"));
            description.appendChild(noInsightsCurrently);
        }
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
            before.classList.add("link", "text-blue-700", "dark:text-blue-300", "text-xl");
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
            after.classList.add("link", "text-blue-700", "dark:text-blue-300", "text-xl");
            paginationDiv.appendChild(after);
        }
        document.getElementById("clusterModalContent").appendChild(paginationDiv);
        document.getElementById("clusterModal").classList.add("!bg-base-100");
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
        renderInsightPage(1, event.currentTarget.getAttribute("problemid"), event.currentTarget.getAttribute("clusterid"), true);
        scrollYVal = window.pageYOffset;
        document.body.style.top = "-" + scrollYVal.toString() + "px";
        document.body.style.position = "fixed";
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
        var listProblems = document.createElement("div");
        if(similarProblemsData.hasOwnProperty("not_all_similar")) {
            var description = document.createElement("div");
            var descriptionH3 = document.createElement("h3");
            descriptionH3.style.marginBottom = "0.3em";
            descriptionH3.appendChild(document.createTextNode("Viewing all problems with insights similar to any one in this cluster:"));
            descriptionH3.classList.add("text-lg", "font-bold");
            var pleaseWaitH3 = document.createElement("h3");
            pleaseWaitH3.classList.add("text-lg", "font-bold");
            pleaseWaitH3.appendChild(document.createTextNode("Please try again later... Not all similar problems have been considered. We are in the process of doing so"));
            description.appendChild(descriptionH3);
            description.appendChild(pleaseWaitH3);
            document.getElementById("clusterModalContent").appendChild(description);
            if(firstTime) document.getElementById("clusterModelOverlay").classList.add("visibleSlower");
            else document.getElementById("clusterModalContent").classList.add("fade");
            button.disabled = false;
            document.getElementById("clusterModal").style.height = null;
            document.getElementById("clusterModal").classList.add("!bg-base-100");
            return;
        }
        if(similarProblemsData.hasOwnProperty("none_in_cluster")) {
            var description = document.createElement("div");
            var descriptionH3 = document.createElement("h3");
            descriptionH3.style.marginBottom = "0.3em";
            descriptionH3.appendChild(document.createTextNode("Viewing all problems with insights similar to any one in this cluster:"));
            descriptionH3.classList.add("text-lg", "font-bold");
            var tryagainH3 = document.createElement("h3");
            tryagainH3.appendChild(document.createTextNode("The insight cluster has nothing in it! Perhaps all the insights were deleted recently. Please refresh the page."));
            tryagainH3.classList.add("text-lg", "font-bold");
            description.appendChild(descriptionH3);
            description.appendChild(tryagainH3);
            document.getElementById("clusterModalContent").appendChild(description);
            if(firstTime) document.getElementById("clusterModelOverlay").classList.add("visibleSlower");
            else document.getElementById("clusterModalContent").classList.add("fade");
            button.disabled = false;
            document.getElementById("clusterModal").style.height = null;
            document.getElementById("clusterModal").classList.add("!bg-base-100");
            return;
        }
        for(var idx in similarProblemsData["new_page_obj"]["problems"]) {
            var problem = similarProblemsData["new_page_obj"]["problems"][idx];
            if(problem["id"] == similarProblemsData["firstProblem"]["id"]) {
                continue;
            }
            var problemItemDiv = document.createElement("div");
            var problemItemUl = document.createElement("ul");
            var problemItem = document.createElement("li");
            var problemLink = document.createElement("a"); // TODO: SET font size to large
            problemItemUl.classList.add("list-disc");
            problemLink.href = problem["link"];
            problemLink.target = "_blank";
            problemLink.rel = "noopener noreferrer";
            problemLink.appendChild(document.createTextNode(problem["name"]));
            problemLink.classList.add("link", "text-blue-700", "dark:text-blue-300");
            var summaryLink = document.createElement("a");
            summaryLink.href = "/problems/viewAllSummary/?problem=" + problem["id"].toString() + "&type=insight";
            summaryLink.target = "_blank";
            summaryLink.rel = "noopener noreferrer";
            summaryLink.appendChild(document.createTextNode("View summary of insights of this problem"));
            summaryLink.classList.add("btn", "btn-sm", "btn-ghost", "btn-active", "mt-2", "!h-fit", "p-2");
            summaryLink.style.padding = "0.4em;";
            problemItem.appendChild(problemLink);
            var sharedInsightsDetails = document.createElement("details");
            var sharedInsightsSummary = document.createElement("summary");
            sharedInsightsSummary.appendChild(document.createTextNode("Shared similar insights from this problem:"));
            var sharedInsightsList = document.createElement("ul");
            sharedInsightsList.classList.add("list-disc");
            sharedInsightsList.style = "margin-left: 40px;";
            for(var idx in problem["insights_matched"]) {
                var sharedInsight = problem["insights_matched"][idx];
                var sharedInsightPoint = document.createElement("li");
                sharedInsightPoint.appendChild(document.createTextNode(sharedInsight.text + " by " + sharedInsight.username));
                sharedInsightsList.appendChild(sharedInsightPoint);
            }
            var sharedInsightsLink = document.createElement("a");
            sharedInsightsLink.href = "/problems/sharedInsights/?type=group&insightProblem=" + problemId + "&otherProblem=" + problem["id"].toString() + "&cluster=" + clusterId;
            sharedInsightsLink.target = "_blank";
            sharedInsightsLink.rel = "noopener noreferrer";
            sharedInsightsLink.classList.add("btn", "btn-sm", "btn-ghost", "btn-active", "!h-fit", "p-2");
            sharedInsightsLink.appendChild(document.createTextNode("View ALL insights of this problem that are shared with this cluster"));
            sharedInsightsDetails.append(sharedInsightsSummary);
            sharedInsightsDetails.append(sharedInsightsList);
            sharedInsightsDetails.appendChild(sharedInsightsLink);
            problemItem.appendChild(sharedInsightsDetails);
            problemItem.appendChild(summaryLink);
            problemItemUl.appendChild(problemItem);
            problemItemUl.style = "margin: 0px 0px 0px 20px;";
            problemItemDiv.appendChild(problemItemUl);
            problemItemDiv.classList.add("card", "max-w-2xl", "bg-base-100", "border", "dark:border-neutral-600", "p-3", "my-2");
            listProblems.appendChild(problemItemDiv);
        }
        var description = document.createElement("div");
        var descriptionH3 = document.createElement("h3");
        descriptionH3.style.marginBottom = "0.3em";
        descriptionH3.appendChild(document.createTextNode("Viewing all problems with insights similar to any one in this cluster:"));
		descriptionH3.classList.add("text-lg", "font-bold");
        var descriptionCluster = document.createElement("p");
        descriptionCluster.style.marginBottom = "0.2em";
        descriptionCluster.style.marginTop = "0.3em";
        descriptionCluster.appendChild(document.createTextNode("One insight of this cluster is: " + similarProblemsData["firstInsight"]["text"] + " by " + similarProblemsData["firstInsight"]["username"]));
        description.appendChild(descriptionH3);
        description.appendChild(descriptionCluster);
        var insightClusterButton = document.createElement("button");
		insightClusterButton.classList.add("btn", "btn-small", "btn-outline", "btn-warning", "!min-h-9", "h-9", "mb-2");
        const problemIdAttribute = document.createAttribute("problemid");
        problemIdAttribute.value = problemId;
        insightClusterButton.setAttributeNode(problemIdAttribute);
        const clusterIdAttribute = document.createAttribute("clusterid");
        clusterIdAttribute.value = clusterId;
        insightClusterButton.setAttributeNode(clusterIdAttribute);
        insightClusterButton.innerText = "View all insights in this cluster";
        insightClusterButton.addEventListener("click", function (event) {
            var clusterModelOverlay = document.getElementById("clusterModelOverlay");
            if(clusterModelOverlay.classList.contains("visible")) clusterModelOverlay.classList.remove("visible");
            if(clusterModelOverlay.classList.contains("visibleSlower")) clusterModelOverlay.classList.remove("visibleSlower");
            document.body.style.position = '';
            document.body.style.top = '';
            window.scrollTo(0, scrollYVal);
            renderInsightPage(1, event.currentTarget.getAttribute("problemid"), event.currentTarget.getAttribute("clusterid"), true);
            scrollYVal = window.pageYOffset;
            document.body.style.top = "-" + scrollYVal.toString() + "px";
            document.body.style.position = "fixed";
            document.getElementById("clusterModelOverlay").classList.add("visible");
        });
        description.appendChild(insightClusterButton);
        if(similarProblemsData["new_page_obj"]["problems"].length == 0) {
            var noProblemsCurrently = document.createElement("h3");
            noProblemsCurrently.appendChild(document.createTextNode("There are no problems currently that are similar to this one with these conditions. Try refreshing maybe."));
            description.appendChild(noProblemsCurrently);
        }
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
            before.classList.add("link", "text-blue-700", "dark:text-blue-300", "text-xl");
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
            after.classList.add("link", "text-blue-700", "dark:text-blue-300", "text-xl");
            paginationDiv.appendChild(after);
        }
        document.getElementById("clusterModalContent").appendChild(paginationDiv);
        document.getElementById("clusterModal").style.height = null;
        document.getElementById("clusterModal").classList.add("!bg-base-100");
        if(firstTime) document.getElementById("clusterModelOverlay").classList.add("visibleSlower");
        else document.getElementById("clusterModalContent").classList.add("fade");
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
        event.currentTarget.disabled = true;
        scrollYVal = window.pageYOffset;
        document.body.style.top = "-" + scrollYVal.toString() + "px";
        document.body.style.position = "fixed";
        renderProblemPage(1, event.currentTarget.getAttribute("problemid"), event.currentTarget.getAttribute("clusterid"), true, event.currentTarget);
    });
}
document.getElementById("closeModalButton").classList.add("btn", "btn-small", "btn-error", "!min-h-9", "h-9", "mb-2");
document.getElementById("closeModalButton").addEventListener("click", function (event) {
    var clusterModelOverlay = document.getElementById("clusterModelOverlay");
    if(clusterModelOverlay.classList.contains("visible")) clusterModelOverlay.classList.remove("visible");
    if(clusterModelOverlay.classList.contains("visibleSlower")) clusterModelOverlay.classList.remove("visibleSlower");
    document.body.style.position = '';
    document.body.style.top = '';
    window.scrollTo(0, scrollYVal);
});
