from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from deepface import DeepFace
import cv2
import numpy as np
import base64
import subprocess

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class SmileRequest(BaseModel):
    wallet_address: str
    image_data: str


def send_smile_tokens(receiver_wallet_address):
    token_mint_address = "BQen5jjxswUZtPSmp5sv3PXdyRcwoo73ttKZefAyCVco"
    command = [
        "spl-token", "transfer", token_mint_address, "10", receiver_wallet_address,
        "--fund-recipient", "--allow-unfunded-recipient"
    ]
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print("Blockchain Error:", e.stderr)
        return False

@app.post("/submit-smile")
async def process_smile(request: SmileRequest):
    if not request.wallet_address:
        return {"success": False, "message": "Wallet address required."}

    # 1. Decode the Base64 image from the frontend
    encoded_data = request.image_data.split(',')[1]
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # 2. Analyze the emotion using DeepFace
    try:
        # enforce_detection=False prevents crashes if the face is blurry
        analysis = DeepFace.analyze(img, actions=['emotion'], enforce_detection=False)
        
        # DeepFace returns a list of faces. We grab the dominant emotion of the first face.
        dominant_emotion = analysis[0]['dominant_emotion']
        print(f"Detected emotion: {dominant_emotion}")

        # 3. If happy, trigger Solana transfer!
        if dominant_emotion == 'happy':
            tx_success = send_smile_tokens(request.wallet_address)
            if tx_success:
                return {"success": True, "message": "Tokens sent!"}
            else:
                return {"success": False, "message": "Transaction failed on blockchain."}
        else:
            return {"success": False, "message": f"Looked like you were {dominant_emotion}. Smile harder!"}

    except Exception as e:
        print(f"Error analyzing image: {e}")
        return {"success": False, "message": "AI could not process the image."}

