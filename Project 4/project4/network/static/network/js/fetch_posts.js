async function fetchPosts(options) {
    try {
        const urlParams = new URLSearchParams(window.location.search);
        
        if (options?.profileUserId) {
            urlParams.append('profile_user', options.profileUserId);
        } else if (options?.followerUserId) {
            urlParams.append('follower', options.followerUserId);
        }

        const APIURL = new URL(URLs.posts, window.location.origin);
        APIURL.search = urlParams;

        const response = await fetch(APIURL.toString());
        const data = await response.json();
        if (data.success) {
            return data;
        } else {
            throw new Error('Failed to fetch posts');
        }
    } catch (error) {
        console.error('Error fetching posts:', error);
        throw error;
    }
}

function createPosts(posts, user) {

    return posts.map(post => {
        const editButton = post.creator === user ? `<a class="edit-button" href="${URLs.edit + post.id}"><i class="fa-solid fa-pen"></i></a>` : '';
        const content = `<div class="post">
                <span class="post-header">
                    <a class="post-username" href="${URLs.profile}${post.creator}">${post.creator}</a>
                    <span class="like-info" data-post-id="${post.id}" data-has-liked="${post.has_liked ? 1 : 0}">
                        <span class="like-counter">${post.likes_count}</span>
                        <div class="like-button-container"></div>
                    </span>
                </span>
                <span class="post-content">${post.content}</span>
                <span class="post-created"><small>${post.created_at}</small></span>
                ${editButton}
            </div>`;
        return content;
    }).join('');
}

function navigatePosts(pageNumber, hasNext, hasPrevious) {
    if (!hasNext && !hasPrevious) return;

    const buttonContainer = document.querySelector('.nav-posts');

    const nextButton = document.createElement("a");
    nextButton.textContent = "Next";
    nextButton.className = 'nav-post-link';

    const prevButton = document.createElement("a");
    prevButton.textContent = "Previous";
    prevButton.className = 'nav-post-link';

    const urlParams = new URLSearchParams(window.location.search);
    const urlSearch = new URL(window.location.href);

    if (hasNext) {
        urlParams.set('page', pageNumber + 1);
        urlSearch.search = urlParams;
        nextButton.href = urlSearch.toString();
    }

    if (hasPrevious) {
        urlParams.set('page', pageNumber - 1);
        urlSearch.search = urlParams;
        prevButton.href = urlSearch.toString();
    }

    buttonContainer.append(prevButton, nextButton);
}

export {
    fetchPosts,
    createPosts,
    navigatePosts
};