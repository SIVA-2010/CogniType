# 🛡️ CogniType: Advanced Monitoring & Analytics Dashboard

**CogniType** is a sophisticated monitoring and security auditing system designed for educational and administrative environments. It combines stealthy background data collection with a powerful Flask-based web dashboard to provide real-time insights into user activity and potential security breaches.

---

## ✨ Core Features

*   **🔒 Encrypted Data Logging**: All captured keystrokes are encrypted on-the-fly using AES (via the `cryptography` library), ensuring data remains secure even if the logs are accessed by unauthorized parties.
*   **⚠️ Intelligent Flagged Word Detection**: Monitors input for specific keywords (e.g., *games*, *chatgpt*, *unauthorized sites*) and automatically triggers specialized events.
*   **📸 Dynamic Visual Monitoring**:
    *   **Flagged Snapshots**: Automatically captures webcam images when suspicious keywords are detected.
    *   **Periodic Screenshots**: Regularly records screen activity for a comprehensive audit trail.
*   **📊 Insightful Analytics Dashboard**:
    *   **Role-Based Access Control**: Secure logins for **Teachers** and **Principals** with unique verification codes.
    *   **Data Visualization**: Integrated graphs (powered by `Matplotlib`) analyze the ratio of productive vs. flagged activity.
*   **📂 Structured Storage**: Efficiently manages encrypted logs, captured images, and metadata in a structured local repository.

---

## 🛠️ Technology Stack

*   **Backend**: Python, Flask
*   **Security**: Cryptography (Fernet symmetric encryption)
*   **Data Processing**: Pynput (Keystroke Monitoring), OpenCV (Image Capture), Pillow (Image Handling)
*   **Visualization**: Matplotlib
*   **Frontend**: HTML5, Vanilla CSS3, JavaScript

---

## 🚀 Quick Start

### 1. Prerequisites
Ensure you have Python 3.8+ installed. It is highly recommended to use a virtual environment.

### 2. Installation
Clone the repository and install the required dependencies:

```bash
# Clone the repository
git clone https://github.com/SIVA-2010/CogniType.git
cd CogniType

# Create and activate virtual environment
python -m venv venv
source venv/Scripts/activate  # On Windows

# Install dependencies
pip install flask cryptography pillow pynput matplotlib requests opencv-python
```

### 3. Running the Application
Start the monitoring service and web server:

```bash
cd backend
python app.py
```
Visit `http://localhost:5000` to access the dashboard.

---

## 🔐 Administrative Access

| Role | Username | Password | Secret Code |
| :--- | :--- | :--- | :--- |
| **Principal** | `admin` | `password` | `Principal123` |
| **Teacher** | `admin` | `password` | `Teacher123` |

---

## 📂 Project Architecture

```text
├── backend/
│   ├── app.py                 # Main Flask Application
│   ├── keystroke_logger.py     # Background Monitoring Thread
│   ├── encryption.py          # Security & Cryptography Layer
│   ├── visualization.py       # Analytics & Graph Generation
│   └── screenshot.py          # Screen Capture Service
├── frontend/
│   ├── static/                # CSS, JS, and Brand Assets
│   └── templates/             # HTML Dashboard Templates
└── .gitignore                 # Secure File Exclusions
```

---

## ⚖️ Legal Disclaimer & Ethical Use

**IMPORTANT**: This software is intended for educational purposes, internal auditing, and authorized monitoring only. The use of keyloggers without explicit user consent is illegal in many jurisdictions. By using this software, you agree to comply with all local laws and ethical guidelines regarding privacy and data collection.

