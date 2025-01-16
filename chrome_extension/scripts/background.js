const tryCount = 60;

let pendingTabs = {};

function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === "PANOPTO_DOWNLOADER_INITIATE_INSERT") {
        if (!(sender.tab.id in pendingTabs)) {
            pendingTabs[sender.tab.id] = true;
            executeInsertScript(sender.tab.id);
        }
    }

    return false;
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === "PANOPTO_DOWNLOADER_COMPLETE_INSERT") {
        if (sender.tab.id in pendingTabs) {
            delete pendingTabs[sender.tab.id];
        }
    }

    return false;
});

async function executeInsertScript(tabId) {
    let frameIds = [];

    while (frameIds.length == 0) {
        const frames = await chrome.webNavigation.getAllFrames({ tabId: tabId });
        frameIds = frames.filter((f) => f.url.includes("hosted.panopto.com")).map((f) => f.frameId);
        if (frameIds.length == 0)
            await delay(1000);
    }

    console.log("Testing 123");


    for (let i = 0; i < tryCount; i++) {
        if (!(tabId in pendingTabs)) {
            break;
        }

        if (i != 0) {
            await delay(1000);
        }

        await chrome.scripting.executeScript({
            target: { tabId: tabId, frameIds: frameIds },
            function: createDownloadButton,
        });
    }

    if (tabId in pendingTabs) {
        delete pendingTabs[tabId];
    }
}

function createDownloadButton() {
    console.log("Testing 111");

    let navControls = document.getElementById("navigationControls");
    if (!navControls) {
        console.log("Testing 222");
        return;
    }

    if (document.getElementById("panopto-downloader-button") != null)
        return;

    console.log("Testing 444");

    let downloadButton = document.createElement("div");
    downloadButton.id = "panopto-downloader-button";
    downloadButton.classList.add("button-control");
    downloadButton.setAttribute("onclick", "window.downloadVideo()");

    var s = document.createElement('script');
    s.src = chrome.runtime.getURL('scripts/handle-click.js');
    s.onload = function() { this.remove(); };
    (document.head || document.documentElement).appendChild(s);

    const SVG_NS = "http://www.w3.org/2000/svg";

    const svgElement = document.createElementNS(SVG_NS, "svg");
    svgElement.setAttribute("width", "24");
    svgElement.setAttribute("height", "24");
    svgElement.setAttribute("viewBox", "0 0 512 512");
    svgElement.setAttribute("fill", "none");
    svgElement.setAttribute("xmlns", SVG_NS);

    const comment = document.createComment("<!--!Font Awesome Free 6.7.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2025 Fonticons, Inc.-->");

    const pathElement = document.createElementNS(SVG_NS, "path");
    pathElement.setAttribute("d", "M288 32c0-17.7-14.3-32-32-32s-32 14.3-32 32l0 242.7-73.4-73.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3l128 128c12.5 12.5 32.8 12.5 45.3 0l128-128c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L288 274.7 288 32zM64 352c-35.3 0-64 28.7-64 64l0 32c0 35.3 28.7 64 64 64l384 0c35.3 0 64-28.7 64-64l0-32c0-35.3-28.7-64-64-64l-101.5 0-45.3 45.3c-25 25-65.5 25-90.5 0L165.5 352 64 352zm368 56a24 24 0 1 1 0 48 24 24 0 1 1 0-48z");
    pathElement.setAttribute("fill", "currentColor");

    svgElement.appendChild(comment)
    svgElement.appendChild(pathElement);
    downloadButton.appendChild(svgElement)
    navControls.insertBefore(downloadButton, navControls.children[navControls.children.length - 1]);


    (async () => {
        try {
            const link = document.createElement("link");
            link.rel = "stylesheet";
            link.type = "text/css";
            link.href = chrome.runtime.getURL('scripts/embed-styles.css');
            document.head.appendChild(link);

            const response = await fetch(chrome.runtime.getURL('scripts/popup.html'));
            const html = await response.text();
            
            const container = document.createElement('div');
            container.id = "downloaderContainer";
            container.style.display = 'none';
            container.innerHTML = html;
            document.body.appendChild(container);
        } catch (error) {
            console.error('Error inserting HTML:', error);
        }

        chrome.runtime.sendMessage({ type: "PANOPTO_DOWNLOADER_COMPLETE_INSERT" });
    })();
}