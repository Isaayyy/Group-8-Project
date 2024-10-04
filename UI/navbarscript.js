// Grab the navbar element and create the underline element
const navbar = document.getElementById("navbar");
const navItems = document.querySelectorAll('.nav-item');

// Create the underline element and append it to the nav list
const underline = document.createElement('div');
underline.className = 'underline';
document.querySelector('.nav-list').appendChild(underline); // Append underline to nav list

// Function to handle scroll event
window.onscroll = function () {
    if (window.pageYOffset > 50) { // When scrolled 50px or more
        navbar.classList.add("scrolled"); // Add 'scrolled' class to the navbar
    } else {
        navbar.classList.remove("scrolled"); // Remove the class if back at the top
    }
};

// Set initial underline position
function setUnderline() {
    const activeItem = document.querySelector('.nav-item.active a'); // Get the anchor of the active item
    const { left, width } = activeItem.getBoundingClientRect(); // Get the active item dimensions
    const navList = document.querySelector('.nav-list');
    const navListOffset = navList.getBoundingClientRect().left; // Get the left offset of the nav list
    underline.style.transform = `translateX(${left - navListOffset}px)`; // Adjust position relative to the nav list
    underline.style.width = `${width}px`; // Set width of the underline
}

// Handle item click
navItems.forEach(item => {
    item.addEventListener('click', () => {
        navItems.forEach(i => i.classList.remove('active')); // Remove active class from all items
        item.classList.add('active'); // Add active class to the clicked item
        setUnderline(); // Update underline position
    });
});

// Initial position of the underline
setUnderline();

// Update underline position on window resize
window.addEventListener('resize', setUnderline);
