import { adjustTextarea } from "./textarea.js";

document.addEventListener('DOMContentLoaded', () => {
    const postTextarea = document.querySelector('textarea.post-content');
    const editButton = document.querySelector('#editButton');
    const postContent = document.querySelector('textarea#postContent');
    const errorText = document.querySelector('.error-message');

    // Adapt text area height interactively
    postTextarea.setSelectionRange(postTextarea.value.length, postTextarea.value.length);
    adjustTextarea(postTextarea, 10);

    editButton.addEventListener('click', () => {
        const content = postContent.value.trim();

        if (!content) {
            errorText.textContent = 'Please enter the text content';
            return;
        }

        fetch(window.location.href, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrf_token,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                content: content,
            })
        })           
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.replace(URLs.index);
            } else {
                errorText.textContent = data.error;
            }
        })
    })
})