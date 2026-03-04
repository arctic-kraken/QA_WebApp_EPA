function add_clause() {
    clearMessages()
    let input = document.getElementById('js-add-clause');
    if (!input.value) {
        addMessage("error", "Clause must not be empty");
        return;
    }

    let div = document.getElementById('js-clauses');
    let html = "";

    html += `<div class="budget-tag">`;
    html += `<span class="budget-tag-text">${input.value}</span>`;
    html += `<span>`;
    html += `<button class="bin-btn" type="button" onclick="remove_clause(this);">
        <img class="icon bin-icon filter-dark-red">
    </button>`;
    html += `</span>`;
    html += `</div>`;

    div.innerHTML += html;

    prepare_clauses();
    addMessage("info", "Clause added successfully");
    input.value = ''
}

function remove_clause(sender) {
    clearMessages()
    let parent = sender.parentNode.parentNode;
    parent.remove();

    prepare_clauses();
}

function prepare_clauses() {
    let hiddenInput = document.getElementById("js-form-clauses");
    let texts = document.getElementsByClassName("budget-tag-text");
    var prepared_texts = [];

    for(var i = 0; i < texts.length; i++) {
        prepared_texts[i] = texts[i].innerHTML;
    }

    const new_obj = {
        clauses: prepared_texts
    };

    hiddenInput.value = JSON.stringify(new_obj);

//    console.log("debug: " + hiddenInput.value);
}