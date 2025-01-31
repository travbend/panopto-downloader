
const apiUrl = "https://pd.travbend.com/panopto-downloader/api/v1/convert-to-mp4";

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function downloadVideo() {
    let downloadText = document.getElementById("downloaderPopupText");
    downloadText.textContent = "Decoding file...";

    let container = document.getElementById("downloaderContainer");
    container.style.display = 'flex';

    try {
        let metaData = await getVideoMetadata();
        let taskId = await initiateDecode(metaData);

        let status = null;

        while (true) {
            status = await getDecodeStatus(taskId)

            if (status != "PENDING")
                break;

            await sleep(1000);
        }

        if (status != "COMPLETED")
            throw new Error("Failed to convert file");

        downloadText.textContent = "Downloading file...";

        let downloadUrl = await getDownloadUrl(taskId);
        await downloadFile(downloadUrl, metaData.fileName);
        await closeDownload(taskId);

    } catch (e) {
        console.error(e);
        alert("An error occurred while downloading the video. Please try again later.");
    } finally {
        container.style.display = 'none';
    }
}

async function getVideoMetadata() {
    const queryParams = new URLSearchParams(window.location.search);
    let deliveryId = queryParams.get('id') 
                     ?? Panopto.viewer.data?.playlist?.initialDeliveryId 
                     ?? Panopto.Embed?.instance?.deliveryId;

    if (deliveryId == null)
        throw new Error("Unable to get delivery Id");

    let params = new URLSearchParams();
    params.append("deliveryId", deliveryId);
    params.append("isLiveNotes", "false");
    params.append("refreshAuthCookie", "true");
    params.append("isActiveBroadcast", "false");
    params.append("isEditing", "false");
    params.append("isKollectiveAgentInstalled", "false");
    params.append("isEmbed", "false");
    params.append("responseType", "json");

    let request = {
        body: params,
        credentials: "include",
        headers: {
            "X-Csrf-Token": document.cookie.split("; csrfToken=")[1].split(";")[0]
        },
        method: "POST",
        signal: null
    }

    let response = await PanoptoApiClient.doFetch(PanoptoApiClient.getAppRootUrl() +  "/Pages/Viewer/DeliveryInfo.aspx", request);
    let responseBody = await response.json();

    let metaData = {
        fileName: responseBody.Delivery.Streams[0].Name,
        videoUrl: responseBody.Delivery.Streams[0].StreamHttpUrl
    };

    if (metaData.fileName == null)
        metaData.fileName = 'video_download.mp4';

    return metaData;
}

async function initiateDecode(metaData) {
    const url = apiUrl + '/initiate';
    const data = { 
        'video_url': metaData.videoUrl,
        'file_name': metaData.fileName
    };

    let response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });

    if (!response.ok || !response.body)
        throw new Error('Failed to convert the file');

    let responseBody = await response.json();

    return responseBody.task_id;
}

async function getDecodeStatus(taskId) {
    const url = apiUrl + '/status/' + taskId;

    let response = await fetch(url);

    if (!response.ok || !response.body)
        throw new Error('Failed to convert the file');

    let responseBody = await response.json();
    return responseBody.status;
}

async function getDownloadUrl(taskId) {
    const url = apiUrl + '/result/' + taskId;
    const response = await fetch(url);
    
    if (!response.ok || !response.body)
        throw new Error('Failed to download the file');

    let responseBody = await response.json();
    return responseBody.download_url;
}

async function downloadFile(url, fileName) {
    const response = await fetch(url);
    
    if (!response.ok || !response.body)
        throw new Error('Failed to download the file');

    const reader = response.body.getReader();
    let receivedLength = 0;
    const chunks = [];

    while (true) {
        const { done, value } = await reader.read();
        if (done)
            break;

        chunks.push(value);
        receivedLength += value.length;
    }

    let blob = new Blob(chunks);
    const downloadUrl = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = downloadUrl;
    a.download = fileName;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(downloadUrl);
}

async function closeDownload(taskId) {
    const url = apiUrl + '/close/' + taskId;
    const response = await fetch(url, { method: 'PUT' });
    
    if (!response.ok)
        throw new Error('Failed to download the file');
}

window.downloadVideo = downloadVideo;