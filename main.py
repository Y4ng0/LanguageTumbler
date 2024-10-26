import random
import requests
import tkinter as tk
from tkinter import messagebox

# Define the LibreTranslate API base URL
LIBRE_TRANSLATE_URL = "http://localhost:5000"


def get_languages():
    """Retrieve supported languages from LibreTranslate API."""
    url = f"{LIBRE_TRANSLATE_URL}/languages"
    headers = {
        "Accept": "application/json"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        languages = response.json()
        return [lang['code'] for lang in languages]
    except requests.RequestException as e:
        messagebox.showwarning("API Error", f"Failed to retrieve languages: {e}")
        return []


def random_translation_loop(text, rounds):
    """Translate text to random languages using LibreTranslate API and back to original language."""
    original_text = text
    language_list = get_languages()
    if not language_list:
        return "Error retrieving languages."

    last_language = 'en'
    for i in range(rounds):
        target_language = random.choice([lang for lang in language_list if lang != 'en'])
        translated_text = translate_text(text, target_language, last_language)
        if translated_text:
            text = translated_text
            last_language = target_language
        else:
            return "Translation error occurred."

    # Translate back to original language
    return translate_text(text, "en", last_language)


def translate_text(text, target_language, last_language):
    """Translate text to a specified target language using LibreTranslate API."""
    url = f"{LIBRE_TRANSLATE_URL}/translate"
    data = {
        "q": text,
        "source": last_language,
        "target": target_language,
        "format": "text"
    }
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        return response.json()['translatedText']
    except requests.RequestException as e:
        messagebox.showwarning("Translation Error", f"Error translating to {target_language}: {e}")
        return None


def start_translation():
    text = input_text.get("1.0", "end-1c")
    rounds = rounds_entry.get()
    if not text:
        messagebox.showwarning("Input Error", "Please enter text to translate.")
        return
    if not rounds.isdigit():
        messagebox.showwarning("Input Error", "Please enter a valid number of rounds.")
        return

    rounds = int(rounds)
    result = random_translation_loop(text, rounds)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, result)


# Setting up the main Tkinter window
root = tk.Tk()
root.title("LibreTranslate Translation Looper")

# Input text field
tk.Label(root, text="Enter Text to Translate:").pack()
input_text = tk.Text(root, height=4, width=50)
input_text.pack()

# Number of rounds field
tk.Label(root, text="Number of Translation Rounds:").pack()
rounds_entry = tk.Entry(root)
rounds_entry.pack()

# Start Translation button
translate_button = tk.Button(root, text="Start Translation", command=start_translation)
translate_button.pack(pady=5)

# Output text field
tk.Label(root, text="Final Translated Text:").pack()
output_text = tk.Text(root, height=4, width=50)
output_text.pack()

root.mainloop()
