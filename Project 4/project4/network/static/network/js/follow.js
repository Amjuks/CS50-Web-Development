document.addEventListener('DOMContentLoaded', () => {
    const profileActions = document.querySelector('.profile-actions');
    const followButton = document.querySelector('#followButton');
    const followCount = document.querySelector('.follower-count');
    const followerText = document.querySelector('.followers-text');
    const profileUser = Number.parseInt(profileActions.getAttribute('data-profile-user-id'));

    followButton.addEventListener('click', () => {
        const follows = Number.parseInt(profileActions.getAttribute('data-follows')) === 1;

        fetch(URLs.follow, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrf_token,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                profileUser: profileUser,
                followAction: !follows
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const following = data.follow_action ? true : false;
                profileActions.setAttribute('data-follows', following ? '1' : '0');
                followButton.textContent = following ? "Unfollow" : "Follow";

                followCount.textContent = data.follow_count;

                if (data.follow_count === 0) {
                    followerText.textContent = 'No Followers';
                } else if (data.follow_count === 1) {
                    followerText.textContent = 'Follower';
                } else {
                    followerText.textContent = 'Followers';
                }
            }
        })
    })
})