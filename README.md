# Student Monitoring & Keylogger Dashboard

This project is a comprehensive monitoring dashboard built using Python and Flask. It securely logs keystrokes, captures screenshots, and snaps images upon detecting flagged words. It implements multiple layers of security and provides a web interface to visualize and manage logged data.

## Features

- **Encrypted Keylogging**: Keystrokes are captured and securely encrypted before being saved (`cryptography` library).
- **Flagged Word Detection**: Automatically detects specific flagged words being typed (e.g., games, youtube, chatgpt) and triggers an image capture.
- **Screenshot & Image Capture**: Periodically captures screenshots and clicks webcam images during flagged events.
- **Role-based Web Dashboard**: Web interface for viewing logs, generated bar graphs (using `matplotlib`), and captured images. Includes role-based authentication (`Teacher`, `Principal`).
- **Data Visualization**: Graphs displaying the split between random words, random letters, and flagged words.

## Prerequisites

Python 3.x is required. Install the following key dependencies before running:

```bash
pip install flask cryptography pillow pynput matplotlib requests
```
*(Note: You may also need `opencv-python` depending on the webcam capture logic).*

## Folder Structure

- `backend/`: Contains the core application files.
  - `app.py`: The main Flask server and entry point.
  - `keystroke_logger.py`: Background thread for capturing keystrokes and detecting flagged words.
  - `encryption.py`: Uses Fernet symmetric encryption to securely store logs and images.
  - `visualization.py`: Generates bar graphs based on log analysis.
  - `screenshot.py` & `image_capture.py`: Background tasks for visual monitoring.
- `frontend/`: Contains `templates/` (HTML) and `static/` (CSS/JS) for the web interface.
- `keylogger/`: Automatically created to store generated logs, keys, encrypted screenshots, and graphs.

## How to Run

1. Navigate to the project root directory.
2. Ensure you have the required dependencies installed (ideally in a `venv` virtual environment).
3. Start the application:
   ```bash
   cd backend
   python app.py
   ```
4. Access the web dashboard by navigating to `http://localhost:5000` in your web browser.

## Authentication Details

Use the following default keys to access the system:
- **Username**: `admin`
- **Password**: `password`
- **Secret Code (Teacher)**: `Teacher123`
- **Secret Code (Principal)**: `Principal123`

## Note on Security & Privacy

**Disclaimer**: This software is designed for educational/local monitoring purposes. It implements a keylogger and screen/camera capture. Ensure you have appropriate consent and authorization from the users before deploying this software.
