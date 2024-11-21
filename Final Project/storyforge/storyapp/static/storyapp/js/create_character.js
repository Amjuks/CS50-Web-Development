import { setupImagePreview } from "./image_preview.js";

document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('charImage');
    const fileInputButton = document.getElementById('fileInputButton');
    const charPreview = document.getElementById('charPreview');

    setupImagePreview(fileInput, fileInputButton, charPreview);
})