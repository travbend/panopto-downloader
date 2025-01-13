
const apiUrl = "https://pd.travbend.com/panopto-downloader/api/v1/convert-to-mp4"

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function downloadVideo() {
    let downloadText = document.getElementById("downloaderPopupText");
    downloadText.textContent = "Decoding file...";

    let container = document.getElementById("downloaderContainer");
    container.style.display = 'flex';

    try {
        const queryParams = new URLSearchParams(window.location.search);
        let deliveryId = queryParams.get('id') ?? Panopto.viewer.data.playlist.initialDeliveryId;

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
    
        let initResponse = await PanoptoApiClient.doFetch(PanoptoApiClient.getAppRootUrl() +  "/Pages/Viewer/DeliveryInfo.aspx", request);
        let responseBody = await initResponse.json();
        let fileName = responseBody.Delivery.Streams[0].Name;
        let videoUrl = responseBody.Delivery.Streams[0].StreamHttpUrl;

        const initiateUrl = apiUrl + '/initiate';
        const data = { 
            'video_url': videoUrl,
            'file_name': fileName
        };

        let initiateResponse = await fetch(initiateUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (!initiateResponse.ok || !initiateResponse.body) {
            throw new Error('Failed to convert the file');
        }

        let initiateRBody = await initiateResponse.json();

        const statusUrl = apiUrl + '/status/' + initiateRBody.task_id;

        let status = null;

        while (true) {
            let statusResponse = await fetch(statusUrl);

            if (!statusResponse.ok || !statusResponse.body) {
                throw new Error('Failed to convert the file');
            }

            let statusRBody = await statusResponse.json();
            status = statusRBody.status;

            if (statusRBody.status != "PENDING")
                break;

            await sleep(1000);
        }

        if (status != "COMPLETED")
            throw new Error("Failed to convert file");

        downloadText.textContent = "Downloading file...";

        const resultUrl = apiUrl + '/result/' + initiateRBody.task_id;
        const resultResponse = await fetch(resultUrl);
        
        if (!resultResponse.ok || !resultResponse.body) {
            throw new Error('Failed to download the file');
        }

        const reader = resultResponse.body.getReader();
        let receivedLength = 0;
        const chunks = [];

        while (true) {
            const { done, value } = await reader.read();
            if (done) {
                break;
            }
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

    } catch (e) {
        alert("An error occurred while downloading the video. Please try again later.");
    } finally {
        container.style.display = 'none';
    }
}

window.downloadVideo = downloadVideo;