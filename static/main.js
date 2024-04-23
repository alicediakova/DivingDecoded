window.addEventListener('resize', adjustTextPosition);
window.addEventListener('load', adjustTextPosition);

function adjustTextPosition() {
    const overlayText = document.getElementById('overlay-text');
    const image = document.querySelector('.results-character');
    const imagePosition = image.getBoundingClientRect();
    const imageLeft = imagePosition.left;

    // Check if the number is a single digit or double digits
    if (overlayText.textContent.length === 1) {
        // If it's a single digit, set the left position and width as needed
        overlayText.style.left = `${imageLeft + 40}px`;
        overlayText.style.transform = 'scaleX(1)'; // Reset to normal width
    } else {
        // If it's double digits, set the left position and width as needed
        overlayText.style.left = `${imageLeft - 15}px`;
        overlayText.style.transform = 'scaleX(0.8)'; // Make it 80% of the original width
    }

    // Set the vertical position
    overlayText.style.top = '40px';
}

function changeImage(origImage, imageName) {
    document.querySelector(`.${origImage}`).src = `static/images/${imageName}.png`;
}

window.onload = function() {
    document.getElementById('toggle-navbar').addEventListener('change', function() {
        var navbar = document.getElementById('navbar');
        var backButton = document.getElementById('back-button');
        if (this.checked) {
            navbar.style.display = 'block';
            backButton.style.display = 'block';
        } else {
            navbar.style.display = 'none';
            backButton.style.display = 'none';
        }
    });
};

window.onload = function() {
    var videoSwitch = document.getElementById('videoSwitch');
    var regularVideo = document.getElementById('regularVideo');
    var slowVideo = document.getElementById('slowVideo');

    videoSwitch.addEventListener('change', function() {
        if (this.checked) {
            regularVideo.style.display = 'none';
            slowVideo.style.display = 'block';
            if (!regularVideo.paused) {
                regularVideo.pause();
                slowVideo.play();
            }
        } else {
            regularVideo.style.display = 'block';
            slowVideo.style.display = 'none';
            if (!slowVideo.paused) {
                slowVideo.pause();
                regularVideo.play();
            }
        }
    });
};