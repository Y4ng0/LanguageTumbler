import random
import requests
import tkinter as tk
from tkinter import messagebox

# Define the LibreTranslate API base URL
LIBRE_TRANSLATE_URL = "http://localhost:5000"


def get_languages():
    """Retrieve supported languages from LibreTranslate API with necessary headers."""
    url = f"{LIBRE_TRANSLATE_URL}/languages"
    headers = {
        "Accept": "application/json"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        languages = response.json()
        lang_dict = {language['code']: {'name':language['name'], 'target':language['targets']} for language in languages}
        return lang_dict
        #return [lang['code'] for lang in languages]
    except requests.RequestException as e:
        messagebox.showwarning("API Error", f"Failed to retrieve languages: {e}")
        return []


def random_translation_loop(text, rounds):
    """Translate text to random languages using LibreTranslate API and back to original language."""
    original_text = text

    lang_dict = get_languages()

    if not lang_dict:
        return "Error retrieving languages."

    language_list = lang_dict.keys()

    # Clear intermediate translations display
    intermediate_textbox.delete("1.0", tk.END)

    from_language = "en"
    for i in range(rounds):
        target_language = random.choice(lang_dict[from_language]['target'])
        translated_text = translate_text(text, target_language, from_language)
        if translated_text:
            text = translated_text
            from_language = target_language
            # Append each translation to the intermediate text box
            intermediate_textbox.insert(tk.END, f"Round {i + 1} ({target_language}): {text}\n\n")
            intermediate_textbox.see(tk.END)  # Scroll to the latest translation
        else:
            return "Translation error occurred."

    # Translate back to original language
    final_text = translate_text(text, "en", from_language)
    return final_text


def translate_text(text, target_language, from_language="en"):
    """Translate text to a specified target language using LibreTranslate API."""
    url = f"{LIBRE_TRANSLATE_URL}/translate"
    data = {
        "q": text,
        "source": from_language,
        "target": target_language,
        "format": "text"
    }
    headers = {
        "Accept": "application/json"
    }
    try:
        response = requests.post(url, headers=headers, data=data)
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

# Intermediate translations field
tk.Label(root, text="Intermediate Translations:").pack()
intermediate_textbox = tk.Text(root, height=10, width=50, wrap="word")
intermediate_textbox.pack()

# Output text field
tk.Label(root, text="Final Translated Text:").pack()
output_text = tk.Text(root, height=4, width=50)
output_text.pack()

root.mainloop()
