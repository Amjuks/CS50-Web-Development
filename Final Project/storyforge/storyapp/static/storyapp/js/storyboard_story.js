import { setupImagePreview } from "./image_preview.js";

document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('worldCover');
    const fileInputButton = document.getElementById('fileInputButton');
    const worldCoverPreview = document.getElementById('worldCoverPreview');

    setupImagePreview(fileInput, fileInputButton, worldCoverPreview);
})