document.addEventListener("DOMContentLoaded", function () {
    console.log("DOM fully loaded and parsed");

    const contentDiv = document.getElementById("doc-content");
    const darkModeToggle = document.querySelector(".dark-mode-toggle");

    if (!contentDiv) {
        console.error("Element with ID 'doc-content' not found!");
        return;
    }

    loadGoogleDoc();

    // Dark Mode Toggle
    darkModeToggle.addEventListener("click", function () {
        document.body.classList.toggle("dark-mode");
        darkModeToggle.textContent = document.body.classList.contains("dark-mode") ? "☀️" : "🌙";
    });
});

function loadGoogleDoc() {
    fetch("https://ics-timeline.onrender.com/get-doc") // Replace with your API endpoint
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.json();
        })
        .then(data => {
            console.log("Fetched data:", data);
            document.getElementById("doc-content").innerHTML = data.content || "<p style='color: gray;'>No content available.</p>";
        })
        .catch(error => {
            console.error("Error fetching Google Doc:", error);
            document.getElementById("doc-content").innerHTML = "<p style='color: red;'>Error loading content.</p>";
        });
}
