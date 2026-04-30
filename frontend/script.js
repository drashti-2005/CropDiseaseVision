// Select elements from the DOM
const imageInput = document.getElementById('imageInput');
const imagePreview = document.getElementById('imagePreview');
const predictBtn = document.getElementById('predictBtn');
const loading = document.getElementById('loading');
const result = document.getElementById('result');
const diseaseNameSpan = document.getElementById('diseaseName');
const confidenceLevelSpan = document.getElementById('confidenceLevel');
const errorDiv = document.getElementById('error');

// Handle image upload and preview
imageInput.addEventListener('change', function(event) {
    const file = event.target.files[0];
    
    // Clear previous results/errors
    result.classList.add('hidden');
    errorDiv.classList.add('hidden');
    
    if (file) {
        // Read and show image preview
        const reader = new FileReader();
        reader.onload = function(e) {
            imagePreview.src = e.target.result;
            imagePreview.style.display = 'block';
        }
        reader.readAsDataURL(file);
        
        // Enable predict button
        predictBtn.disabled = false;
    } else {
        // Reset if no file selected
        imagePreview.style.display = 'none';
        predictBtn.disabled = true;
    }
});

// Handle 'Predict Disease' button click
predictBtn.addEventListener('click', async function() {
    const file = imageInput.files[0];
    
    if (!file) {
        showError("Please select an image first.");
        return;
    }
    
    // Create FormData object to send file to the backend
    const formData = new FormData();
    formData.append('file', file);
    
    // UI state updates: Disable button, show loading
    predictBtn.disabled = true;
    loading.classList.remove('hidden');
    result.classList.add('hidden');
    errorDiv.classList.add('hidden');
    
    try {
        // Prepare API call
        // Replace this URL with your actual backend URL if different
        const apiUrl = 'http://127.0.0.1:5000/predict';
        
        // Make POST request to backend
        const response = await fetch(apiUrl, {
            method: 'POST',
            body: formData
        });
        
        // Parse JSON response
        const data = await response.json();
        
        if (response.ok) {
            // Update UI with predictions
            diseaseNameSpan.textContent = data.disease;
            confidenceLevelSpan.textContent = data.confidence;
            
            // Show result block
            result.classList.remove('hidden');
        } else {
            // Show error returned from API
            showError(`Error: ${data.error || 'Prediction failed'}`);
        }
    } catch (err) {
        console.error('Fetch error:', err);
        showError('Failed to connect to the prediction server. Make sure the backend API is running at http://127.0.0.1:5000');
    } finally {
        // UI state updates: Hide loading, enable button
        loading.classList.add('hidden');
        predictBtn.disabled = false;
    }
});

// Helper function to show errors
function showError(message) {
    errorDiv.textContent = message;
    errorDiv.classList.remove('hidden');
}
