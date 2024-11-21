function setupImagePreview(fileInput, button, preview) {
    button.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', event => {
        const file = event.target.files[0];

        if (file) {
            const reader = new FileReader();

            reader.onload = function (e) {
                preview.src = e.target.result;
            };

            reader.readAsDataURL(file);
        }
    });
}

export {
    setupImagePreview
};