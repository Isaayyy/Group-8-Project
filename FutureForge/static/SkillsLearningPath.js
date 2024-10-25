document.addEventListener("DOMContentLoaded", function() {
    fetch('/navbar')
        .then(response => response.text())
        .then(data => {
            document.getElementById('navbar').innerHTML = data;
        });
});

let activeDiamond = null; // Track the currently active diamond

function expandDiamond(element) {
    // Get the current background color of the diamond
    const currentColor = element.style.backgroundColor;
    
    // Check if the clicked diamond is the active one
    if (activeDiamond && activeDiamond !== element) {
        // Reset the previously active diamond
        activeDiamond.style.width = '100px'; // Original width
        activeDiamond.style.height = '100px'; // Original height
        const activeText = activeDiamond.querySelector('.diamond-text');
        activeText.style.fontSize = '40px'; // Original text size

        // Reset the bottom line color
        const activeBottomLine = activeDiamond.nextElementSibling; // Select the corresponding bottom line
        activeBottomLine.style.borderBottom = `7px solid ${activeDiamond.style.backgroundColor}`; // Reset to original color

        // Reset the diamond container gradient
        const activeContainer = activeBottomLine.parentElement; // Get the container
        activeContainer.style.background = ''; // Reset gradient

        // Reset box shadow
        element.style.boxShadow = ''; // Reset box shadow
    }

    // Toggle the clicked diamond
    if (element.style.width === '130px') {
        // If the diamond is already enlarged, reset it
        element.style.width = '100px'; // Original width
        element.style.height = '100px'; // Original height
        const diamondText = element.querySelector('.diamond-text');
        diamondText.style.fontSize = '40px'; // Original text size

        // Reset the bottom line color
        const bottomLine = element.nextElementSibling;
        bottomLine.style.borderBottom = `7px solid ${element.style.backgroundColor}`; // Reset to original color
        
        // Reset the diamond container gradient
        const container = bottomLine.parentElement; // Get the container
        container.style.background = ''; // Reset gradient

        // Reset activeDiamond
        activeDiamond = null; // No active diamond

        // Reset box shadow
        element.style.boxShadow = ''; // Reset box shadow
    } else {
        // Otherwise, enlarge the clicked diamond
        element.style.width = '130px'; // New width
        element.style.height = '130px'; // New height
        
        // Change the text size
        const diamondText = element.querySelector('.diamond-text');
        diamondText.style.fontSize = '50px'; // New text size

        // Change the color of the bottom line to match the diamond
        const bottomLine = element.nextElementSibling;
        bottomLine.style.borderBottom = `0 solid ${currentColor}`; // Use the current diamond color

        // Set the current diamond as the active one
        activeDiamond = element; // Update activeDiamond

        // Apply linear gradient to the diamond container
        const container = bottomLine.parentElement; // Get the container
        container.style.background = `linear-gradient(to top, ${currentColor}, transparent)`; // Set gradient

        // Add white shadow to the diamond
        element.style.boxShadow = `0 4px 10px rgba(255, 255, 255, 0.5)`;
    }
}