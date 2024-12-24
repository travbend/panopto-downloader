
let script = document.createElement('script');
script.src = chrome.runtime.getURL('scripts/ffmpeg.js');
script.onload = () => {
  script.remove(); // Clean up after script injection
};
document.documentElement.appendChild(script);

// script = document.createElement('script');
// script.src = chrome.runtime.getURL('scripts/814.ffmpeg.js');
// script.onload = () => {
//   script.remove(); // Clean up after script injection
// };
// document.documentElement.appendChild(script);

// script = document.createElement('script');
// script.src = chrome.runtime.getURL('scripts/ffmpegutil.js');
// script.onload = () => {
//   script.remove(); // Clean up after script injection
// };
// document.documentElement.appendChild(script);

async function downloadVideo() {
    let videoUrl = "https://d2y36twrtb17ty.cloudfront.net:443/sessions/81a498b9-55f2-49fa-b77b-b1cb0133a245/cca0e7df-04ae-4a66-bcc5-b1cb0133a254-8a0df6b1-10f8-46f1-a3c1-b1cb013b86d3.hls/master.m3u8?InvocationID=4534a3a7-6fbe-ef11-a9f7-0a1a827ad0ec&tid=00000000-0000-0000-0000-000000000000&StreamID=5d2ec785-d06e-45f2-80eb-b1cb0133a314&ServerName=utexas.hosted.panopto.com";

    const ffmpeg = new FFmpegWASM.FFmpeg()

    const baseURL = 'https://unpkg.com/@ffmpeg/core@0.12.6/dist/umd';
    let coreURL = await FFmpegUtil.toBlobURL(`${baseURL}/ffmpeg-core.js`, 'text/javascript');
    let wasmURL = await FFmpegUtil.toBlobURL(`${baseURL}/ffmpeg-core.wasm`, 'application/wasm');
    let classWorkerURL = await FFmpegUtil.toBlobURL('https://unpkg.com/@ffmpeg/ffmpeg@0.12.10/dist/umd/814.ffmpeg.js', 'text/javascript');
    let test = await fetch(coreURL);
    await ffmpeg.load({
        coreURL: coreURL,
        wasmURL: wasmURL,
        classWorkerURL: classWorkerURL
    });

    await ffmpeg.writeFile('master.m3u8', await FFmpegUtil.fetchFile(videoUrl));
    await ffmpeg.exec(['-i', 'master.m3u8', 'output.mp4']);
    const data = await ffmpeg.readFile('output.mp4');

    // Create a downloadable link
    const blob = new Blob([data.buffer], { type: 'video/mp4' });
    const url = URL.createObjectURL(blob);

    // Create and trigger a download
    const a = document.createElement('a');
    a.href = url;
    a.download = 'output.mp4';
    a.click();
    URL.revokeObjectURL(url);
}

downloadVideo();


var s = document.createElement('script');
s.src = chrome.runtime.getURL('scripts/handle-click.js');
s.onload = function() { this.remove(); };
(document.head || document.documentElement).appendChild(s);

// var s2 = document.createElement('script');
// s2.src = chrome.runtime.getURL('scripts/ffmpeg.min.js');
// s2.onload = function() { this.remove(); };
// (document.head || document.documentElement).appendChild(s2);

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
