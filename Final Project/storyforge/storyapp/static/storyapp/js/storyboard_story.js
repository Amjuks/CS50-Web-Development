document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('worldCover');
    const fileInputButton = document.getElementById('fileInputButton');
    const worldCoverPreview = document.getElementById('worldCoverPreview');

    fileInputButton.addEventListener('click', () => {
        fileInput.click();
    })

    fileInput.addEventListener('change', event => {
        const file = event.target.files[0];

        if (file) {
            const reader = new FileReader();
            
            reader.onload = function (e) {
                worldCoverPreview.src = e.target.result;
            };
            
            reader.readAsDataURL(file);
        }
    })
})