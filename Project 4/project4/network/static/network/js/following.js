import { createLikeButton } from "./helpers.js";
import { fetchPosts, createPosts,navigatePosts } from "./fetch_posts.js";

document.addEventListener('DOMContentLoaded', async () => {
    const followerUserId = document.querySelector('#userId').value;
    const data = await fetchPosts({followerUserId: followerUserId});
    const postBody = document.querySelector('.posts-body');
    const userName = document.querySelector('#userName').value;

    postBody.innerHTML = createPosts(data.posts, userName);
    navigatePosts(data.page, data.has_next, data.has_previous);

    const likeContainer = document.querySelectorAll('.like-info');

    likeContainer.forEach(container => {
        const postId = Number.parseInt(container.getAttribute('data-post-id'));
        const hasLiked = container.getAttribute('data-has-liked') !== '0';

        createLikeButton(postId, hasLiked, container);
    });
})