import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
import { setupImagePreview } from "./image_preview.js";
import { toggleFlowchart } from "./flowchart.js";

mermaid.initialize({ startOnLoad: true });
  

document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('worldCover');
    const fileInputButton = document.getElementById('fileInputButton');
    const worldCoverPreview = document.getElementById('worldCoverPreview');

    const toggleStoryboard = document.getElementById('toggleStoryboard');
    const flowchart = document.querySelector('.flowchart-design');

    toggleFlowchart(toggleStoryboard, flowchart, 'Storyboard');

    setupImagePreview(fileInput, fileInputButton, worldCoverPreview);
})