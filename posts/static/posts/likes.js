function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}


document.addEventListener('DOMContentLoaded', function() {
        const likeIcons = document.querySelectorAll('.like-icon');

        likeIcons.forEach(icon => {
            icon.addEventListener('click', function() {
                const postId = this.id.split('-')[2];
                const likeSection = document.getElementById(`like-section-${postId}`);
                const likeIcon = document.getElementById(`like-icon-${postId}`);
                const likesCount = document.getElementById(`likes-count-${postId}`);

                fetch(`/post/${postId}/like/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCSRFToken(),
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({})
                })
                .then(response => response.json())
                .then(data => {
                    if (data.liked) {
                        likeIcon.src = "/static/posts/images/like-blue.png";
                    } else {
                        likeIcon.src = "/static/posts/images/like.png";
                    }
                    likesCount.textContent = data.likes_count;
                });
            });
        });
    });

