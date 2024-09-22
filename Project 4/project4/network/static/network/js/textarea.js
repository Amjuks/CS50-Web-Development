function adjustTextarea(textarea, maxLines) {
    const lineHeight = parseFloat(getComputedStyle(textarea).lineHeight);
    
    const maxHeight = maxLines ? lineHeight * maxLines : Infinity;

    function updateHeight() {
        textarea.style.height = 'auto';
        textarea.style.height = `${Math.min(textarea.scrollHeight, maxHeight)}px`;
    }

    updateHeight();

    textarea.addEventListener('input', updateHeight);
}


export { adjustTextarea };