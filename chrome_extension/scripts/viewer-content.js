var s = document.createElement('script');
s.src = chrome.runtime.getURL('scripts/handle-click.js');
s.onload = function() { this.remove(); };
(document.head || document.documentElement).appendChild(s);

let downloadButton = document.createElement("div");
downloadButton.style.width = "60px"
downloadButton.classList.add("transport-button");
downloadButton.textContent = "Download";
downloadButton.setAttribute("onclick", "window.downloadVideo()");

let captionsButton = document.getElementById("captionsButton");
if (captionsButton) {
    captionsButton.insertAdjacentElement("afterend", downloadButton);
} else {
    let navControls = document.getElementById("navigationControls");
    navControls.appendChild(downloadButton);
}

(async () => {
    try {
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
})();