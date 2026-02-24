async function getNewInviteCode() {
    clearMessages();
    const url = `/account/newinvite`;
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`Response Status: ${response.status}`)
        }

        const result = await response.text();

        let element = document.getElementById("js-inviteCode");
        element.innerHTML = result;
        addMessage("info", "Got new invite code");
    } catch (error) {
        console.error(`error: ${error.message}`);
        addMessage("error", `Failed to get new invite code - ${error.message}`);
    }
}