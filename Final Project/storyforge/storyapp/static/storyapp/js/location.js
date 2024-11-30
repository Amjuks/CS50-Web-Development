import { setupImagePreview } from "./image_preview.js";

document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('locImage');
    const fileInputButton = document.getElementById('fileInputButton');
    const charPreview = document.getElementById('locCoverPreview');
    
    setupImagePreview(fileInput, fileInputButton, charPreview);
})