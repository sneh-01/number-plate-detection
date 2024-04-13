document.addEventListener('DOMContentLoaded', function () {
    var form = document.getElementById('uploadForm');
    var fileInput = document.getElementById('fileInput');
    var outputDiv = document.getElementById('output');

    form.addEventListener('submit', function (e) {
        e.preventDefault();
        var formData = new FormData(form);

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.text())
        .then(data => {
            outputDiv.innerHTML = data;
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});
