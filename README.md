#  Smile-to-Earn Verification System

A lightweight web application that rewards users for **smiling** after passing a **voice challenge**.  
The system uses a **FastAPI backend** with **DeepFace emotion detection**, and a **vanilla JavaScript frontend** to capture webcam frames and detect spoken triggers.

---


## ⚙️ Features

- **Voice Challenge Verification:** User must say a trigger word like `"cheese"` or `"smile"` before capture.  
- **Smile Detection:** Backend uses **DeepFace** to detect emotion from the webcam frame.  
- **Reward Eligibility:** If a user is smiling (happiness score > 70), they are eligible for a reward.  
- **Lightweight & Modular:** Backend and frontend are separated for clarity and easy deployment.  
- **Fast Processing:** Response times within 1–2 seconds for most requests.  

---

## 🖥 Frontend Workflow

1. User opens the webpage (`index.html`).  
2. Browser asks for **camera access**.  
3. Frontend listens for **voice trigger words** using **Web Speech API**.  
4. When user says `"cheese"` or `"smile"`, a webcam frame is captured.  
5. Captured frame is sent as **base64** to the backend via HTTP POST request.  

---

## 🖥 Backend Workflow

1. The backend receives a **POST request** at `/verify-smile` with a JSON payload containing:
   - `voice_verified`: whether the user passed the voice challenge
   - `image`: the captured webcam frame encoded in base64

2. It first checks if the voice challenge is verified.  
   - If not, it immediately responds that the voice challenge failed.

3. The base64 image is decoded and reconstructed for processing.

4. The backend analyzes the face and emotion using **DeepFace** to detect if the user is smiling.

5. The happiness score is extracted:
   - If the score exceeds the smile threshold (e.g., 70%), the user is **smile verified**.
   - Otherwise, the user is not verified for a smile.

6. The backend returns a JSON response indicating:
   - Whether a face was detected
   - Whether the smile was verified
   - Whether the user is eligible for a reward

---

##  Tech Stack

- **Frontend:** HTML, CSS, JavaScript (Webcam + Web Speech API)  
- **Backend:** Python, FastAPI, DeepFace, NumPy  
- **Server:** Uvicorn for running FastAPI locally  
- **Libraries/Dependencies:** `fastapi`, `uvicorn`, `deepface`, `numpy`, `python-multipart`
