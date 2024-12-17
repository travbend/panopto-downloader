async function handleClick() {
    let deliveryId = crypto.randomUUID();

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

    let response = await PanoptoApiClient.doFetch("https://utexas.hosted.panopto.com/Panopto/Pages/Viewer/DeliveryInfo.aspx", request);
    console.log(response);
}

window.DownloadVideo = handleClick;