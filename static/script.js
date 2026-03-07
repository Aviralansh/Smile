const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const statusText = document.getElementById('status');
const walletInput = document.getElementById('wallet');
const send = document.getElementById('send')

async function startApp() {
        // 1. Ask user for Camera Access
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
    } catch (err) {
        alert("Camera access denied or not found!");
        return;
    }


    // 2. Start listening to the Microphone
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.onstart = function() {
        statusText.innerText = 'Listening... Say "Cheese"!';
    };


    recognition.onresult = function(event) {
        const transcript = event.results[event.results.length - 1][0].transcript.trim().toLowerCase();
        console.log("Heard: ", transcript);
        
        // If the user says "cheese" or "smile", snap the photo!
        if (transcript.includes("cheese") || transcript.includes("smile")) {
            statusText.innerText = "Captured! Analyzing smile...";
            captureAndSend();
        }
    };

    recognition.start();
}



function captureAndSend() {

    // Draw current video frame to canvas
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    // Convert to Base64 image
    const base64Image = canvas.toDataURL('image/jpeg');
    console.log(base64Image)
    // Send to FastAPI Backend
    fetch('http://localhost:8000/submit-smile', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            wallet_address: walletInput.value,
            image_data: base64Image
        })
    })

    .then(res => res.json())
    .then(data => {
        if(data.success) {
            statusText.innerText = "Smile Detected! Sending Toekn";
        } else {
            statusText.innerText = "No smile detected. Try again! 😐";
        }
    })

    .catch(err => console.error(err));
}

