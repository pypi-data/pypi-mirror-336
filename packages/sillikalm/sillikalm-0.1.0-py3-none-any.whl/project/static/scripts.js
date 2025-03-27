// Summary: This JavaScript file defines the client-side functionality for the SillikaLM application.
// It includes functions for creating, listing, and deleting models, as well as fetching and displaying logs.
// The file also handles UI interactions such as enabling/disabling buttons and populating dropdowns.
// 
// Copyright (c) 2025 Krishnakanth Allika, speed-acorn-whiff@duck.com
// Licensed under the GNU General Public License v3 (GPLv3).
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// any later version.
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program. If not, see https://www.gnu.org/licenses/gpl-3.0-standalone.html.

async function createModels() {
    console.log('createModels function called');
    document.getElementById('installModelsButton').disabled = true; // Disable the button
    document.getElementById('response').innerHTML = ''; // Clear previous output
    document.getElementById('spinner').style.display = 'block'; // Show spinner
    const baseModel = document.getElementById('baseModelDropdown').value;
    console.log('Selected base model:', baseModel);
    const formData = new FormData();
    formData.append('base_model_info', baseModel);
    document.getElementById('installNote').style.display = 'block'; // Show the note
    const response = await fetch('/create_models', { method: 'POST', body: formData });
    const data = await response.json();
    console.log('Response from /create_models:', data);
    displayCreateModelsTable(data);
    document.getElementById('installNote').style.display = 'none'; // Hide the note
    document.getElementById('spinner').style.display = 'none'; // Hide spinner
    document.getElementById('baseModelDropdown').value = ''; // Reset dropdown to not selected state
    await populateModelDropdown(); // Populate the dropdown after installing models
    document.getElementById('installModelsButton').disabled = true; // Disable the button again
}

async function listModels() {
    console.log('listModels function called');
    document.getElementById('response').innerHTML = ''; // Clear previous output
    const response = await fetch('/list_models', { method: 'POST' });
    const data = await response.json();
    console.log('Response from /list_models:', data);
    displayListModelsTable(data.Models);
}

async function deleteModels() {
    console.log('deleteModels function called');
    document.getElementById('response').innerHTML = ''; // Clear previous output
    const modelName = document.getElementById('modelNameDropdown').value;
    console.log('Selected model to delete:', modelName);
    const formData = new FormData();
    formData.append('model_name', modelName);
    const response = await fetch('/delete_models', { method: 'POST', body: formData });
    const data = await response.json();
    console.log('Response from /delete_models:', data);

    let table = '<table><tr><th>Status</th></tr>';
    if (data["Model deletion status"]) {
        const status = data["Model deletion status"];
        table += `<tr><td>${status}</td></tr>`;
    }
    table += '</table>';

    document.getElementById('response').innerHTML = table;
    await populateModelDropdown(); // Populate the dropdown after deleting a model
}

async function deleteAllModels() {
    console.log('deleteAllModels function called');
    document.getElementById('response').innerHTML = ''; // Clear previous output
    const response = await fetch('/delete_all_models', { method: 'POST' });
    const data = await response.json();
    console.log('Response from /delete_all_models:', data);
    
    let table = '<table><tr><th>Model</th><th>Status</th></tr>';
    
    if (data["Models deletion status"]) {
        for (const [model, status] of Object.entries(data["Models deletion status"])) {
            table += `<tr><td>${model}</td><td>${status}</td></tr>`;
        }
    } else if (data["Model deletion status"]) {
        table += `<tr><td colspan="2">${data["Model deletion status"]}</td></tr>`;
    }
    
    table += '</table>';
    document.getElementById('response').innerHTML = table;
    await populateModelDropdown(); // Populate the dropdown after deleting all models
}

function displayCreateModelsTable(data) {
    console.log('displayCreateModelsTable function called with data:', data);
    let table = '<table><tr><th>Allika\'s Silly Language Model</th><th>Installation Status</th></tr>';
    if (data["Models import status"] === "Success") {
        data["Models added"].forEach(model => {
            table += `<tr><td>${model}</td><td>${data["Models import status"]}</td></tr>`;
        });
    } else if (data["Models import status"] === "Error") {
        table += `<tr><td colspan="2">Error: ${data["Error message"]}</td></tr>`;
    }
    table += '</table>';
    document.getElementById('response').innerHTML = table;
}

function displayListModelsTable(models) {
    console.log('displayListModelsTable function called with models:', models);
    let table = '<table><tr><th>Model Name</th><th>Size</th><th>Parameters</th><th>Quantization</th><th>Last Modified</th></tr>';
    models.forEach(model => {
        if (model["Model Name"].endsWith('_SillikaLM')) {
            table += `<tr>
                        <td>${model["Model Name"]}</td>
                        <td>${model["Size"]}</td>
                        <td>${model["Parameters"]}</td>
                        <td>${model["Quantization"]}</td>
                        <td>${model["Last Modified"]}</td>
                      </tr>`;
        }
    });
    table += '</table>';
    document.getElementById('response').innerHTML = table;
}

async function populateModelDropdown() {
    console.log('populateModelDropdown function called');
    const response = await fetch('/list_models', { method: 'POST' });
    const data = await response.json();
    console.log('Response from /list_models for dropdown:', data);
    const dropdown = document.getElementById('modelNameDropdown');
    dropdown.innerHTML = '<option value="" disabled selected>Select model to delete</option>'; // Reset dropdown
    data.Models.forEach(model => {
        if (model["Model Name"].endsWith('_SillikaLM')) {
            const option = document.createElement('option');
            option.value = model["Model Name"];
            option.textContent = model["Model Name"];
            dropdown.appendChild(option);
        }
    });
    document.getElementById('deleteModelButton').disabled = true; // Disable button initially
}

async function populateBaseModelDropdown() {
    console.log('populateBaseModelDropdown function called');
    try {
        const response = await fetch('/list_base_models', { method: 'GET' });
        if (!response.ok) {
            console.error('Failed to fetch base models:', response.statusText);
            return;
        }
        const data = await response.json();
        console.log('Response from /list_base_models for dropdown:', data);
        const dropdown = document.getElementById('baseModelDropdown');
        dropdown.innerHTML = '<option value="" disabled selected>Select base model</option>'; // Reset dropdown
        data.base_models.forEach(model => {
            const option = document.createElement('option');
            option.value = model;
            option.textContent = model;
            dropdown.appendChild(option);
        });
        document.getElementById('installModelsButton').disabled = true; // Disable button initially
    } catch (error) {
        console.error('Error populating base model dropdown:', error);
    }
}

// Ensure the function is called on page load
window.onload = async () => {
    console.log('Window onload event triggered');
    await populateBaseModelDropdown();
    await populateModelDropdown();

    // Modify the "Chat with SillikaLMs" button behavior
    const chatButton = document.getElementById('chatButton');
    if (chatButton) {
        let countdown = 59; // Start countdown from 59 seconds
        const initializingText = "Initializing Chat UI"; // Updated phrase

        // Set the initial button text
        chatButton.textContent = `${initializingText} (${countdown}s)`;

        const timerInterval = setInterval(() => {
            if (countdown > 0) {
                countdown--; // Decrease seconds
                chatButton.textContent = `${initializingText} (${countdown}s)`; // Update the button text with the timer
            } else {
                clearInterval(timerInterval); // Stop the timer
                chatButton.textContent = "Chat with SillikaLMs"; // Change to final text
                chatButton.disabled = false; // Enable the button
                console.log('Chat button enabled after 1 minute');
            }
        }, 1000); // Update every second
    }
};

async function fetchLogs() {
    const response = await fetch('/logs');
    const logs = await response.text();
    const formattedLogs = logs
        .replace(/\\n/g, '<br>')
        .replace(/^"|"$/g, '')
        .replace(/- INFO -/g, '- <span style="color:rgb(139, 204, 64);">INFO</span> -')
        .replace(/- DEBUG -/g, '- <span style="color: #ffcc00;">DEBUG</span> -');
    console.log('Logs fetched:', formattedLogs);
    const logOutput = document.getElementById('logOutput');
    logOutput.innerHTML = formattedLogs;
    logOutput.scrollTop = logOutput.scrollHeight; // Scroll to the bottom
}

function copyLogsToClipboard() {
    const logOutput = document.getElementById('logOutput').innerText;
    navigator.clipboard.writeText(logOutput).then(() => {
        console.log('Logs copied to clipboard');
    }).catch(err => {
        console.error('Failed to copy logs: ', err);
    });
}

async function shutdownSystem() {
    console.log('shutdownSystem function called');
    const response = await fetch('/shutdown', { method: 'POST' });
    const data = await response.json();
    console.log('Response from /shutdown:', data);
    alert(data.message);

    // Open the http://localhost:8086 URL in a new tab and close it
    const newTab = window.open('http://localhost:8086', '_blank');
    if (newTab) {
        newTab.close();
    }

    window.close(); // Close the current tab or window
}

async function startWebUI() {
    console.log('startWebUI function called');
    const response = await fetch('/start_webui', { method: 'POST' });
    const data = await response.json();
    console.log('Response from /start_webui:', data);
}

// Fetch logs every 5 seconds
setInterval(fetchLogs, 5000);

// Event listeners to enable/disable buttons based on dropdown selection
document.getElementById('baseModelDropdown').addEventListener('change', function() {
    console.log('baseModelDropdown changed:', this.value);
    document.getElementById('installModelsButton').disabled = !this.value;
});

document.getElementById('modelNameDropdown').addEventListener('change', function() {
    console.log('modelNameDropdown changed:', this.value);
    document.getElementById('deleteModelButton').disabled = !this.value;
});

document.getElementById('shutdownButton').addEventListener('click', shutdownSystem);

// Populate the base model dropdown and model dropdown on page load
window.onload = async () => {
    console.log('Window onload event triggered');
    await populateBaseModelDropdown();
    await populateModelDropdown();
};