function createLikeButton(postId, hasLiked, container) {
    const button = document.createElement('button');
    const icon = document.createElement('i');

    button.className = 'like-button';
    button.appendChild(icon);

    icon.className = hasLiked ? 'fa-solid fa-heart' : 'fa-regular fa-heart';

    button.addEventListener('mouseover', () => {
        icon.className = hasLiked ? 'fa-regular fa-heart' : 'fa-solid fa-heart';
    });

    button.addEventListener('mouseleave', () => {
        icon.className = hasLiked ? 'fa-solid fa-heart' : 'fa-regular fa-heart';
    });

    button.addEventListener('click', async () => {
        const { success, count } = await updateLike(postId, !hasLiked);
        if (success) {
            container.querySelector('.like-counter').textContent = count;
            createLikeButton(postId, !hasLiked, container);
        }
    });

    const buttonContainer = container.querySelector('.like-button-container');
    buttonContainer.innerHTML = "";
    buttonContainer.appendChild(button);
}

async function updateLike(postId, liked) {
    try {
        const response = await fetch(URLs.like, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrf_token,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                post: postId,
                liked: liked
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();

        return {
            success: data.success,
            count: data.success ? data.count : null
        };
        
    } catch (error) {
        console.error('Error updating like:', error);

        return {
            success: false,
            count: null
        };
    }
}

export { createLikeButton };