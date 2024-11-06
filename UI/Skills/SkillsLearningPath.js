document.addEventListener("DOMContentLoaded", function() {
    // Load the navbar
    fetch('../Navbar/navbar.html')
        .then(response => response.text())
        .then(data => {
            document.getElementById('navbar').innerHTML = data;
        });

    // Automatically click the first diamond to set it as active
    const firstDiamond = document.querySelector('.diamond');
    if (firstDiamond) {
        expandDiamond(firstDiamond);
    }
});

let activeDiamond = null; // Track the currently active diamond
let activeContent = null; // Track the currently active content container

function expandDiamond(element) {
    // Check if the clicked diamond is already active, and if so, do nothing
    if (element === activeDiamond) return;

    // If there is an active diamond and it is not the clicked one, reset it
    if (activeDiamond) {
        activeDiamond.style.width = '100px'; // Original width
        activeDiamond.style.height = '100px'; // Original height
        const activeText = activeDiamond.querySelector('.diamond-text');
        activeText.style.fontSize = '40px'; // Original text size

        // Reset the bottom line color
        const activeBottomLine = activeDiamond.nextElementSibling;
        activeBottomLine.style.borderBottom = `7px solid ${activeDiamond.style.backgroundColor}`;

        // Reset the diamond container gradient
        const activeContainer = activeBottomLine.parentElement;
        activeContainer.style.background = '';

        // Reset box shadow
        activeDiamond.style.boxShadow = '';

        // Hide the previously active content container
        if (activeContent) {
            activeContent.style.display = 'none';
        }
    }

    // Enlarge the clicked diamond
    element.style.width = '130px';
    element.style.height = '130px';
    
    // Change the text size
    const diamondText = element.querySelector('.diamond-text');
    diamondText.style.fontSize = '50px';

    // Change the color of the bottom line to match the diamond
    const bottomLine = element.nextElementSibling;
    bottomLine.style.borderBottom = `0 solid ${element.style.backgroundColor}`;

    // Set the current diamond as the active one
    activeDiamond = element;

    // Apply linear gradient to the diamond container
    const container = bottomLine.parentElement;
    container.style.background = `linear-gradient(to top, ${element.style.backgroundColor}, transparent)`;

    // Add white shadow to the diamond
    element.style.boxShadow = `0 4px 10px rgba(255, 255, 255, 0.5)`;

    // Show the corresponding content container based on the diamond clicked
    const diamondIndex = Array.from(document.querySelectorAll('.diamond')).indexOf(element);
    const contentContainers = document.querySelectorAll('.content-container');
    
    if (contentContainers[diamondIndex]) {
        activeContent = contentContainers[diamondIndex];
        activeContent.style.display = 'block'; // Show the content container
    }
}

function openCity(evt, cityName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(cityName).style.display = "block";
    evt.currentTarget.className += " active";
  }

  // Function to dynamically load courses based on selected tab
async function loadCourses(tab) {
    // Clear previous active classes
    document.querySelectorAll(".tab button").forEach(button => button.classList.remove("active"));
    tab.classList.add("active");

    const category = tab.getAttribute("data-category"); // Get category (e.g., Recommended, Required)

    // Fetch course data based on category
    const response = await fetch(`/api/courses?category=${category}`);
    const courses = await response.json(); // Assuming you get an array of courses
    
    // Build HTML content based on courses data
    const contentContainer = document.getElementById("courses-content");
    contentContainer.innerHTML = ''; // Clear previous content

    courses.forEach(course => {
        contentContainer.innerHTML += `
            <div class="column-container">
                <div class="content-container" style="background-color: ${course.color}; border: 4px solid ${course.borderColor};">
                    <div class="content-inside-container" onclick="openModal('${course.title}', '${course.image}', '${course.state}', '${course.description}')">
                        <div class="content-column-container">
                            <div class="title-container">
                                <img src="Images/titledesign.png">
                                <h2>${course.platform}</h2>
                            </div>
                            <img src="${course.image}" alt="${course.title}">
                        </div>
                        <div class="content-column-container">
                            <h1>${course.title}</h1>
                            <h3>${course.state}</h3>
                            <p>${course.description}</p>
                        </div>
                    </div>
                </div>
            </div>
        `;
    });
}

// Set "Required" as the default load for the tab
document.addEventListener("DOMContentLoaded", () => {
    const defaultTab = document.querySelector('.tab button[data-category="Required"]');
    loadCourses(defaultTab);
});

