import { setupImagePreview } from "./image_preview.js";


document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('world_cover');
    const fileInputButton = document.getElementById('fileInputButton');
    const coverPreview = document.getElementById('worldCoverPreview');

    setupImagePreview(fileInput, fileInputButton, coverPreview);
})