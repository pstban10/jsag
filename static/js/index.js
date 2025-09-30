document.addEventListener('DOMContentLoaded', function () {
    // Video Modal
    const openVideoModalBtn = document.getElementById('open-video-modal');
    const closeVideoModalBtn = document.getElementById('close-video-modal');
    const videoModal = document.getElementById('video-modal');
    const youtubeVideo = document.getElementById('youtube-video');
    const videoSrc = youtubeVideo.src;

    if (openVideoModalBtn) {
        openVideoModalBtn.addEventListener('click', () => {
            videoModal.style.display = 'flex';
            youtubeVideo.src = videoSrc + '&autoplay=1';
        });
    }

    const closeVideoModal = () => {
        videoModal.style.display = 'none';
        youtubeVideo.src = videoSrc;
    };

    if (closeVideoModalBtn) {
        closeVideoModalBtn.addEventListener('click', closeVideoModal);
    }

    if (videoModal) {
        videoModal.addEventListener('click', (e) => {
            if (e.target === videoModal) {
                closeVideoModal();
            }
        });
    }
});
