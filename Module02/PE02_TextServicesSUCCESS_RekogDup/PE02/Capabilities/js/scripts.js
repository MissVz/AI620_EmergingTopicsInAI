// Get references to the form elements
const form = document.getElementById('uploadForm');
const fileInput = document.getElementById('file');
const uploadButton = document.getElementById('uploadButton');
const transcriptionText = document.getElementById('detectedText');
const translatedText = document.getElementById('translatedText');
const audioSource = document.getElementById('audioSource');
const translationAudio = document.getElementById('translationAudio');
const progressContainer = document.getElementById('progressContainer');
const progressBar = document.getElementById('progressBar');

// Get language settings
const fromLanguage = document.getElementById('fromLanguage');
const toLanguage = document.getElementById('toLanguage');

// Event listener to enable the upload button after selecting a file
fileInput.addEventListener('change', () => {
    if (fileInput.files && fileInput.files.length > 0) {
        uploadButton.classList.remove('upload-button-disabled');
        uploadButton.classList.add('upload-button-enabled');
        uploadButton.disabled = false;
    } else {
        uploadButton.classList.add('upload-button-disabled');
        uploadButton.classList.remove('upload-button-enabled');
        uploadButton.disabled = true;
    }
});

// Show the progress bar and animate it
function showProgressBar() {
    // Ensure the container is visible
    progressContainer.style.display = 'block';

    // Reset the progress bar width to 0% before starting the animation
    progressBar.style.width = '0%';

    // Start a simple animation for the progress bar
    let progress = 0;
    const interval = setInterval(() => {
        if (progress < 100) {
            progress += 10;
            progressBar.style.width = `${progress}%`;
        } else {
            clearInterval(interval);
        }
    }, 300); // Animate the progress every 300ms
}

// Hide the progress bar when done
function hideProgressBar() {
    // Hide the progress bar container
    progressContainer.style.display = 'none';
}

// Event listener for form submission (file upload)
form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const formData = new FormData(form);
        
    // Disable the upload button and change its text to indicate it's being clicked
    uploadButton.disabled = true;
    uploadButton.innerText = "Uploading...";

    // Show the progress bar when the upload starts
    showProgressBar();

    try {
        // 1. First, upload the image
        // Send the POST request to upload the file
        const uploadResponse = await fetch('http://127.0.0.1:8000/upload', {
            method: 'POST',
            body: formData
        });

        hideProgressBar();

        if (!uploadResponse.ok) {
            throw new Error('Failed to upload the image');
        }
        const uploadResult = await uploadResponse.json();
        const imageName = uploadResult.fileName;  // Get the image name from the upload response

        if (!imageName) {
            throw new Error('Image name is undefined');
        }

        // 2. Then, call the translation endpoint with the uploaded image name
        const translateResponse = await fetch(`http://127.0.0.1:8000/images/${imageName}/translate-text`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                fromLang: fromLanguage.value,  // Language selected for translation from
                toLang: toLanguage.value       // Language selected for translation to
            })
        });

        hideProgressBar();

        if (translateResponse.ok) {
            const translateResult = await translateResponse.json();

            // Display the success message
            document.getElementById('uploadSuccessMessage').innerText = translateResult.message || 'Translation completed successfully';

            // Display the detected text (transcription)
            detectedText.innerText = 'Detected Text: ' + (translateResult.transcription || 'No transcription found');

            // Display the translated text
            translatedText.innerText = 'Translation: ' + (translateResult.translatedText || 'No translation found');

            // Reset the button state
            uploadButton.innerText = "Upload";
            uploadButton.disabled = false;
        } else {
            throw new Error('Failed to translate the image');
        }
    } catch (error) {
        // Handle errors
        document.getElementById('uploadSuccessMessage').innerText = 'Error: ' + error.message;
        detectedText.innerText = '';
        translatedText.innerText = '';

        // Reset the button to its original state after an error
        uploadButton.innerText = "Upload";
        uploadButton.disabled = false; 

        // Hide the progress bar if an error occurs
        hideProgressBar();
    }        
});
