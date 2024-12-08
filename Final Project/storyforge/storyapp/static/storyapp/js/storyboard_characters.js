import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
import { toggleFlowchart } from "./flowchart.js";

mermaid.initialize({ startOnLoad: true });

document.addEventListener('DOMContentLoaded', () => {
    const toggleRelations = document.getElementById('toggleRelations');
    const flowchart = document.querySelector('.flowchart-design');

    toggleFlowchart(toggleRelations, flowchart, 'Relations');
})