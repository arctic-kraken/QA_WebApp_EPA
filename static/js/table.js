var m_timer = null;
async function deleteRecord(url, id, confirm_text) {
    if (!confirm(confirm_text))
        return

    clearMessages();
    if (m_timer != null)
        clearTimeout(m_timer)

    try {
        const response = await fetch(`${url}/${id}`, { method: "DELETE" });
        if (!response.ok) {
            throw new Error(`${response.text()}`)
        }
        m_timer = setTimeout(reloadPage, 2000);
        addMessage("info", "Successfully revoked access");
    } catch (error) {
        console.error(`error: ${error.message}`);
        addMessage("error", `Failed to revoke access - ${error.message}`);
    }
}

function reloadPage() {
    location.reload();
}