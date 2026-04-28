import os
import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend to avoid GUI issues
import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime
from keystroke_logger import LOGS_FOLDER
from encryption import decrypt_data

# Define the graphs folder path
GRAPHS_FOLDER = os.path.join("keylogger","graphs")

# Create the graphs folder if it doesn't exist
if not os.path.exists(GRAPHS_FOLDER):
    os.makedirs(GRAPHS_FOLDER)
    
    print(f"Created graphs folder at: {os.path.abspath(GRAPHS_FOLDER)}")

def analyze_keystrokes(LOGS_FOLDER):
    """
    Analyze keystroke logs to calculate the percentage of random letters, random words, and flagged words.
    """
    flagged_words = ["youtube", "instagram", "Games", 
                 "ipl","movies","webseries",
                 "anime","flipkart","chatgpt",
                 "vpn","answers","music"]   # Add your flagged words here
    random_letters = []
    random_words = []
    flagged_words_count = 0

    for filename in os.listdir(LOGS_FOLDER):
        file_path = os.path.join(LOGS_FOLDER, filename)
        if os.path.isfile(file_path):
            with open(file_path, "r") as file:
                encrypted_logs = file.readlines()
                for log in encrypted_logs:
                    decrypted_log = decrypt_data(log.strip())  # Decrypt the log
                    words = decrypted_log.split()
                    for word in words:
                        if word.lower() in flagged_words:
                            flagged_words_count += 1
                        elif len(word) == 1:  # Single character (random letter)
                            random_letters.append(word)
                        else:  # Random word
                            random_words.append(word)

    # Calculate percentages
    total = len(random_letters) + len(random_words) + flagged_words_count
    if total == 0:
        return None  # No data to analyze

    random_letters_percent = (len(random_letters) / total) * 100
    random_words_percent = (len(random_words) / total) * 100
    flagged_words_percent = (flagged_words_count / total) * 100

    return {
        "random_letters": random_letters_percent,
        "random_words": random_words_percent,
        "flagged_words": flagged_words_percent
    }

def generate_bar_graph(data, output_path):
    """
    Generate a bar graph and save it as an image.
    This function must be called from the main thread.
    """
    labels = ["Random Letters", "Random Words", "Flagged Words"]
    percentages = [data["random_letters"], data["random_words"], data["flagged_words"]]

    plt.figure(figsize=(8, 6))
    bars = plt.bar(labels, percentages, color=["blue", "green", "red"])
    plt.xlabel("Categories")
    plt.ylabel("Percentage")
    plt.title(f"Keystroke Analysis - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    plt.ylim(0, 100)  # Set y-axis limit to 100%
    plt.grid(axis='y', linestyle='--', alpha=0.7)  # Add grid lines

    # Add percentage labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height, f"{height:.2f}%", 
                 ha='center', va='bottom')

    plt.savefig(output_path)
    plt.close()

def generate_visualization(LOGS_FOLDER):
    """
    Generate a bar graph for keystroke analysis and save it as an image.
    The image is always saved as 'keystroke_analysis.png' to overwrite the previous graph.
    """
    try:
        data = analyze_keystrokes(LOGS_FOLDER)
        if not data:
            print("No data available for visualization.")
            return None

        # Save the graph as an image (always use the same filename)
        graph_filename = "keystroke_analysis.png"
        graph_path = os.path.join(GRAPHS_FOLDER, graph_filename)
        generate_bar_graph(data, graph_path)

        return graph_filename
    except Exception as e:
        print(f"Error generating visualization: {e}")
        return None