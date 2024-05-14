window.onload = function() {
    var loader = document.querySelector('.loader');
    var mainContent = document.querySelector('main');
    mainContent.style.opacity = 0;

    setTimeout(function() {
        loader.style.display = 'none';
        mainContent.style.transition = 'opacity 1s';
        mainContent.style.opacity = 1;
    }, 2000);
};
// window.onload = function() {
//     // Get the loader element
//     var loader = document.querySelector('.loader');

//     // Get the main content and the header
//     var mainContent = document.querySelector('main');

//     // Hide the main content and the header while loading
//     mainContent.style.opacity = 0;

//     // Set a timeout to hide the loader and show the main content and the header after 3 seconds
//     setTimeout(function() {
//         loader.style.display = 'none';

//         // Add the fade-in class to the main content and the header
//         mainContent.style.transition = 'opacity 1s';
//         mainContent.style.opacity = 1;
//     }, 3000);
// };
