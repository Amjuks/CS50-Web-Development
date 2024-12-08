function scrollElementToCenter(element) {
    const container = element.parentElement;

    const scrollLength = element.offsetLeft - container.offsetWidth / 2 + element.offsetWidth / 2;

    container.scrollTo({
        left: scrollLength,
        behavior: 'smooth'
    });
    console.log(element);
    console.log(scrollLength);
    console.log(container);
    console.log("scrolled");
}

function setFlowchartWidth(flowchart) {
    const diagram = flowchart.querySelector('.mermaid');
    
    const observer = new MutationObserver((mutationList) => {
        for (const mutation of mutationList) {
            if (
                mutation.type === 'attributes' &&
                mutation.attributeName === 'data-processed' &&
                diagram.getAttribute('data-processed') === 'true'
            ) {
                const svgObserver = new MutationObserver((svgMutations) => {
                    for (const svgMutation of svgMutations) {
                        if (
                            svgMutation.type === 'attributes' &&
                            svgMutation.attributeName === 'style'
                        ) {
                            const svg = svgMutation.target;
                            const maxWidth = svg.style.maxWidth;
                            if (maxWidth) {
                                svg.setAttribute('width', maxWidth);
                                scrollElementToCenter(diagram);
                                svgObserver.disconnect();
                            }
                        }
                    }
                });

                const svg = diagram.querySelector('svg');
                svgObserver.observe(svg, { attributes: true });
            }
        }
    });

    observer.observe(diagram, { attributes: true });
}

function toggleFlowchart(button, flowchart, text) {
    button.addEventListener('click', () => {
        const hidden = flowchart.classList.contains('hide');
        flowchart.classList.remove(hidden ? 'hide' : 'show');
        flowchart.classList.add(hidden ? 'show' : 'hide');
        button.textContent = hidden ? `Hide ${text}` : `Show ${text}`;
    })

    setFlowchartWidth(flowchart);
}

export { toggleFlowchart }