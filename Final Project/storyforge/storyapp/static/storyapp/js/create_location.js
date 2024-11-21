import { setupImagePreview } from "./image_preview.js";

document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('locImage');
    const fileInputButton = document.getElementById('fileInputButton');
    const locPreview = document.getElementById('locPreview');

    setupImagePreview(fileInput, fileInputButton, locPreview);
})