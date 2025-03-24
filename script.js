document.addEventListener("DOMContentLoaded", function () {
    console.log("DOM fully loaded and parsed");

    const contentDiv = document.getElementById("doc-content");
    
    if (!contentDiv) {
        console.error("Element with ID 'doc-content' not found!");
        return;
    }

    loadGoogleDoc();
});

function loadGoogleDoc() {
    fetch("https://ics-timeline.onrender.com/get-doc")  // Correct endpoint
    // Replace with your actual API URL
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.json();
        })
        .then(data => {
            console.log("Fetched data:", data);
            document.getElementById("doc-content").innerHTML = data.content || "No content available.";
        })
        .catch(error => {
            console.error("Error fetching Google Doc:", error);
            document.getElementById("doc-content").innerHTML = "<p style='color: red;'>Error loading content.</p>";
        });
}
