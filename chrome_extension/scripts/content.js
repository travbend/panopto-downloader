var s = document.createElement('script');
s.src = chrome.runtime.getURL('scripts/handle-click.js');
s.onload = function() { this.remove(); };
(document.head || document.documentElement).appendChild(s);

let captionsButton = document.getElementById("captionsButton");

if (captionsButton) {
    let downloadButton = document.createElement("div");
    // downloadButton.style.width = "40 px"
    downloadButton.classList.add("transport-button");
    downloadButton.textContent = "Download";
    downloadButton.setAttribute("onclick", "window.GetVideoUrl()");
    captionsButton.insertAdjacentElement("afterend", downloadButton);
}