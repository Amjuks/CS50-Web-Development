import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
mermaid.initialize({ startOnLoad: true });

document.addEventListener('DOMContentLoaded', () => {
    const toggleRelations = document.getElementById('toggleRelations');
    const flowchart = document.querySelector('.flowchart-design');

    toggleRelations.addEventListener('click', () => {
        const hidden = flowchart.classList.contains('hide');
        flowchart.classList.remove(hidden ? 'hide' : 'show');
        flowchart.classList.add(hidden ? 'show' : 'hide');
        toggleRelations.textContent = hidden ? 'Hide Relations' : 'Show Relations';
    })
})