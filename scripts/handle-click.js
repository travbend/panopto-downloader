async function handleClick() {
    try {
        let deliveryId = Panopto.viewer.data.playlist.initialDeliveryId;

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
        let fileName = responseBody.Delivery.Streams[0].Name;
        let videoUrl = responseBody.Delivery.Streams[0].StreamHttpUrl;
    
        const videoData = [];
        const hls = new Hls();

        const video = document.createElement('video');
        document.body.appendChild(video);

        hls.attachMedia(video);
        hls.on(Hls.Events.MEDIA_ATTACHED, function () {
            console.log('Media attached.');
            hls.loadSource(videoUrl);
        });

        hls.on(Hls.Events.MANIFEST_PARSED, () => {
            console.log("Manifest Parsed");
        });

        hls.on(Hls.Events.FRAG_BUFFERED, () => {
            console.log("Fragment Buffered");
        });

        hls.on(Hls.Events.FRAG_LOADED, async (event, data) => {
            const response = await fetch(data.frag.url);
            const buffer = await response.arrayBuffer();
            videoData.push(buffer);

            if (videoData.length === hls.levels[hls.currentLevel].details.fragments.length) {
                const combinedBuffer = videoData.reduce((acc, buffer) => {
                    const tmp = new Uint8Array(acc.byteLength + buffer.byteLength);
                    tmp.set(new Uint8Array(acc), 0);
                    tmp.set(new Uint8Array(buffer), acc.byteLength);
                    return tmp.buffer;
                }, new ArrayBuffer(0));
    
                const blob = new Blob([combinedBuffer], { type: 'video/mp4' });
                const url = URL.createObjectURL(blob);
    
                const a = document.createElement('a');
                a.href = url;
                a.download = 'video.mp4';
                a.click();
    
                URL.revokeObjectURL(url);
            }
        });

    } catch (e) {
        alert("An error occurred while downloading the video.");
    }
}

window.DownloadVideo = handleClick;