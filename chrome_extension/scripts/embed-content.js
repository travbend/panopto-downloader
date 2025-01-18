function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

(async () => {
    while (true) {
        await chrome.runtime.sendMessage({ type: "PANOPTO_DOWNLOADER_INITIATE_INSERT" });
        await sleep(1000);
    }
})();