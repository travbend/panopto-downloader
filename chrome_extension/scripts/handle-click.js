
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
    
        let initResponse = await PanoptoApiClient.doFetch(PanoptoApiClient.getAppRootUrl() +  "/Pages/Viewer/DeliveryInfo.aspx", request);
        let responseBody = await initResponse.json();
        let fileName = responseBody.Delivery.Streams[0].Name;
        let videoUrl = responseBody.Delivery.Streams[0].StreamHttpUrl;

    } catch (e) {
        alert("An error occurred while downloading the video.");
    }
}

window.DownloadVideo = handleClick;