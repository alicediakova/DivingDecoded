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

    // Set the height
    overlayText.style.height = '200px'; // Adjust this value as needed
}

function changeImage(origImage, imageName) {
    document.querySelector(`.${origImage}`).src = `static/images/${imageName}.png`;
}
