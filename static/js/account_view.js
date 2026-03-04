window.addEventListener("load", (event) => {
    filter_options(document.getElementById('js-select-year').value);
    document.getElementById('js-select-year').addEventListener("change", function() {
        filter_options(this.value);
        document.getElementById('js-select-month').value = '';
    });
});

function filter_options(exception_year) {
    document.getElementById('js-select-month').querySelectorAll("option").forEach(option => {
        option.style.display = 'none';
    });

    document.getElementById('js-select-month').querySelectorAll(`option.y-${exception_year}`).forEach(option => {
        option.style.display = 'block';
    });
}
