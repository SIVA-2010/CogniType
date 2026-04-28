// Add cache-busting query string to CSS and JS files
const cacheBuster = "?v=1.0";
let decryptionKeys = {
    logs: null,
    screenshots: null,
    flagged_images: null
};

document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("login-form");
    if (loginForm) {
        loginForm.addEventListener("submit", function (event) {
            event.preventDefault();
            const username = document.getElementById("username").value;
            const password = document.getElementById("password").value;
            const role = document.getElementById("role").value;
            const secret_code = document.getElementById("secret_code").value;

            fetch("/login", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({username, password, role, secret_code}),
            })
            .then(response => {
                if (!response.ok) throw new Error("Login failed");
                return response.json();
            })
            .then(data => {
                if (data.redirect) window.location.href = data.redirect;
            })
            .catch(error => {
                console.error("Error:", error);
                alert("Invalid credentials");
            });
        });
    }

    // Dashboard button handlers
    document.querySelectorAll(".actions .btn").forEach(button => {
        button.addEventListener("click", () => {
            const sectionId = button.getAttribute("onclick").match(/'(.*?)'/)[1];
            showContent(sectionId);
        });
    });

    showContent("flagged_images");
});

async function getDecryptionKey(type) {
    if (!decryptionKeys[type]) {
        const key = prompt(`Enter the decryption key to view ${type.replace('_', ' ')}:`);
        if (!key) {
            alert("Decryption key is required.");
            return null;
        }
        decryptionKeys[type] = key;
    }
    return decryptionKeys[type];
}

function showContent(type) {
    const contentDiv = document.getElementById("content");
    if (!contentDiv) return;
    contentDiv.innerHTML = "";

    switch(type) {
        case "logs": fetchLogs(); break;
        case "flagged_images": fetchFlaggedImages(); break;
        case "screenshots": fetchScreenshots(); break;
        case "login_logs": fetchLoginLogs(); break;
        case "visualization": generateVisualization(); break;
    }
}

async function fetchLogs() {
    const decryptionKey = await getDecryptionKey("logs");
    if (!decryptionKey) return;

    try {
        const response = await fetch("/logs", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({decryption_key: decryptionKey}),
        });
        if (!response.ok) throw new Error(`Failed to fetch logs: ${response.statusText}`);

        const logs = await response.json();
        const contentDiv = document.getElementById("content");
        contentDiv.innerHTML = "<h2>Logs</h2>";
        logs.forEach(log => {
            contentDiv.innerHTML += `<p><strong>${log.filename}:</strong> ${log.content}</p>`;
        });
    } catch (error) {
        console.error("Error:", error);
        document.getElementById("content").innerHTML = "<p>Failed to load logs. Please try again later.</p>";
    }
}

async function fetchFlaggedImages() {
    const decryptionKey = await getDecryptionKey("flagged_images");
    if (!decryptionKey) return;

    try {
        const response = await fetch("/flagged_images", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({decryption_key: decryptionKey}),
        });
        if (!response.ok) throw new Error(`Failed to fetch flagged images: ${response.statusText}`);

        const images = await response.json();
        const contentDiv = document.getElementById("content");
        contentDiv.innerHTML = "<h2>Flagged Images</h2>";

        const container = document.createElement("div");
        container.className = "flagged-images-container";

        images.forEach(image => {
            const imageDiv = document.createElement("div");
            imageDiv.className = "flagged-image";
            imageDiv.innerHTML = `
                <img src="/images/${image.filename}" alt="${image.filename}" width="400" height="300">
                <p><strong>Flagged Word:</strong> ${image.flagged_word}</p>
                <p><strong>Flagged Message:</strong> ${image.flagged_message}</p>
                <p><strong>Timestamp:</strong> ${image.timestamp}</p>
            `;
            container.appendChild(imageDiv);
        });

        contentDiv.appendChild(container);
    } catch (error) {
        console.error("Error:", error);
        document.getElementById("content").innerHTML = "<p>Failed to load flagged images. Please try again later.</p>";
    }
}

async function fetchScreenshots() {
    const decryptionKey = await getDecryptionKey("screenshots");
    if (!decryptionKey) return;

    try {
        const response = await fetch("/screenshots", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({decryption_key: decryptionKey}),
        });
        if (!response.ok) throw new Error(`Failed to fetch screenshots: ${response.statusText}`);

        const screenshots = await response.json();
        const contentDiv = document.getElementById("content");
        contentDiv.innerHTML = "<h2>Screenshots</h2>";

        const container = document.createElement("div");
        container.className = "screenshots-container";

        screenshots.forEach(screenshot => {
            const screenshotDiv = document.createElement("div");
            screenshotDiv.className = "screenshot";
            screenshotDiv.innerHTML = `<img src="/screenshots/${screenshot}" alt="Screenshot" width="800">`;
            container.appendChild(screenshotDiv);
        });

        contentDiv.appendChild(container);
    } catch (error) {
        console.error("Error:", error);
        document.getElementById("content").innerHTML = "<p>Failed to load screenshots. Please try again later.</p>";
    }
}

async function fetchLoginLogs() {
    // Check if current user is principal
    try {
        const response = await fetch("/check_role");
        const data = await response.json();
        
        if (!response.ok || data.role !== "Principal") {
            throw new Error("Only principals can view login logs");
        }

        // Proceed with fetching logs if principal
        const logsResponse = await fetch("/login_logs");
        if (!logsResponse.ok) throw new Error(`Failed to fetch login logs: ${logsResponse.statusText}`);

        const logs = await logsResponse.json();
        const contentDiv = document.getElementById("content");
        
        let tableHTML = `
            <h2>Login Logs</h2>
            <table border="1" cellpadding="10" cellspacing="0">
                <thead><tr><th>Username</th><th>Role</th><th>Timestamp</th></tr></thead>
                <tbody>`;
        
        logs.forEach(log => {
            tableHTML += `<tr><td>${log.username}</td><td>${log.role}</td><td>${log.timestamp}</td></tr>`;
        });

        contentDiv.innerHTML = tableHTML + `</tbody></table>`;
    } catch (error) {
        console.error("Error:", error);
        document.getElementById("content").innerHTML = `<p class="error">${error.message}</p>`;
    }
}

async function generateVisualization() {
    try {
        const response = await fetch("/generate_visualization");
        if (!response.ok) throw new Error(`Failed to generate visualization: ${response.statusText}`);

        const data = await response.json();
        if (data.graph_filename) {
            const graphImage = document.getElementById("graphImage");
            graphImage.src = `/graphs/${data.graph_filename}?t=${new Date().getTime()}`;
            document.getElementById("visualization").style.display = "block";
        } else {
            alert("No data available for visualization.");
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Failed to generate visualization. Please try again later.");
    }
}