var m_timer = null;
async function deleteRecord(url, id, confirm_text, success_text, fail_text, reload_page) {
    if (!confirm(confirm_text))
        return

    clearMessages();
    if (m_timer != null && reload_page)
        clearTimeout(m_timer)

    try {
        const response = await fetch(`${url}/${id}`, { method: "DELETE" });
        if (!response.ok) {
            throw new Error(`${response.text()}`)
        }
        if (reload_page) {
            m_timer = setTimeout(reloadPage, 3000);
        }
        addMessage("info", success_text);
    } catch (error) {
        console.error(`error: ${error.message}`);
        addMessage("error", `${fail_text} ${error.message}`);
    }
}

function reloadPage() {
    location.reload();
}