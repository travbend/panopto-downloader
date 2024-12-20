
var s = document.createElement('script');
s.src = chrome.runtime.getURL('scripts/handle-click.js');
s.onload = function() { this.remove(); };
(document.head || document.documentElement).appendChild(s);

var s2 = document.createElement('script');
s2.src = "https://cdn.jsdelivr.net/npm/@ffmpeg/ffmpeg@0.12.10/dist/umd/ffmpeg.min.js";
s2.onload = function() { this.remove(); };
(document.head || document.documentElement).appendChild(s2);

let captionsButton = document.getElementById("captionsButton");

if (captionsButton) {
    console.log("Has Captions");

    let downloadButton = document.createElement("div");
    // downloadButton.style.width = "40 px"
    downloadButton.classList.add("transport-button");
    downloadButton.textContent = "Download";
    downloadButton.setAttribute("onclick", "window.DownloadVideo()");
    // downloadButton.onclick = handleClick;
    captionsButton.insertAdjacentElement("afterend", downloadButton);
} else {
    console.log("No Captions");
}
