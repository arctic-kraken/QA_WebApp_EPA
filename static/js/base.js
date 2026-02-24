function addMessage(level, content) {
    let html = "";

    html += `<div class='message ${level}'>`;
    html += `<img class="icon ${level}-icon" style="margin-right: 5px;">`;
    html += `<div>${content}</div>`;
    html += `</div>`;

    let el = document.getElementsByClassName("message-container")[0];
    el.innerHTML += html;
}

function clearMessages() {
    let el = document.getElementsByClassName("message-container")[0];
    el.innerHTML = "";
}

function copyToClipboard(id) {
    clearMessages();
    let el = document.querySelector(id);

    var range = document.createRange();
    range.selectNode(el);
    window.getSelection().addRange(range);

    try {
        var success = document.execCommand('copy');
        var msg = success ? "successful" : "unsuccessful";
        if (msg == 'successful')
            addMessage("info", "Invite Code copied to clipboard!");
        else
            throw new Error();
    } catch (error) {
        addMessage("error", "Failed to copy to clipboard");
    }

    window.getSelection().removeAllRanges();
}