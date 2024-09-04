// home.js
const images = [
    'https://images.ctfassets.net/e5382hct74si/5XbQ9hAOyBLzQZRVhP8pLl/f456d9728cc7b3c7fef2f1fa77c70f6f/museum1.jpg',
    'https://images.ctfassets.net/e5382hct74si/4DRp7zxZrLWBXKtbGwLHGG/c8d2f65e8e8f7d2b9e6d02946f8d0fb7/museum2.jpg',
    'https://images.ctfassets.net/e5382hct74si/1Fy3Hy4qXYBq5sRZ2QZLXo/8f48e68a1c9c3ee4b378e4a62a3e909a/museum3.jpg',
];

let currentImage = 0;
const slideshowElement = document.querySelector('.image-slideshow');

function changeBackground() {
    slideshowElement.style.backgroundImage = `url(${images[currentImage]})`;
    currentImage = (currentImage + 1) % images.length;
}

// Set initial background
changeBackground();

// Change background every 5 seconds
setInterval(changeBackground, 5000);