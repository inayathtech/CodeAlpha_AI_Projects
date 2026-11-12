
import tkinter as tk
from tkinter import ttk, messagebox
import urllib.request
import urllib.parse
import json

def translate_text():
    text = input_text.get("1.0", tk.END).strip()

    if not text:
        messagebox.showwarning("Warning", "Please enter some text!")
        return

    source = source_lang.get()
    target = target_lang.get()

    try:
        url = "https://api.mymemory.translated.net/get?" + urllib.parse.urlencode({
            "q": text,
            "langpair": source + "|" + target
        })

        request = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        with urllib.request.urlopen(request, timeout=20) as response:
            data = json.loads(response.read().decode("utf-8"))

        result = data["responseData"]["translatedText"]

        output_text.config(state="normal")
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, result)
        output_text.config(state="disabled")

    except Exception as error:
        messagebox.showerror(
            "Translation Error",
            "Translation failed. Check your internet connection and try again.\n\n"
            + str(error)
        )

def copy_translation():
    result = output_text.get("1.0", tk.END).strip()
    if result:
        root.clipboard_clear()
        root.clipboard_append(result)
        messagebox.showinfo("Copied", "Translation copied!")

root = tk.Tk()
root.title("Language Translation Tool")
root.geometry("650x600")
root.configure(bg="#eef3f8")

title = tk.Label(
    root,
    text="LANGUAGE TRANSLATION TOOL",
    font=("Arial", 20, "bold"),
    bg="#eef3f8",
    fg="#183153"
)
title.pack(pady=20)

tk.Label(root, text="Enter your text:", font=("Arial", 12),
         bg="#eef3f8").pack()

input_text = tk.Text(root, height=6, width=65, font=("Arial", 11))
input_text.pack(pady=10)

languages = {
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Arabic": "ar",
    "Japanese": "ja"
}

frame = tk.Frame(root, bg="#eef3f8")
frame.pack(pady=15)

tk.Label(frame, text="From:", bg="#eef3f8",
         font=("Arial", 11)).grid(row=0, column=0, padx=8)

source_lang = ttk.Combobox(
    frame, values=list(languages.keys()), state="readonly", width=15
)
source_lang.set("English")
source_lang.grid(row=0, column=1, padx=8)

tk.Label(frame, text="To:", bg="#eef3f8",
         font=("Arial", 11)).grid(row=0, column=2, padx=8)

target_lang = ttk.Combobox(
    frame, values=list(languages.keys()), state="readonly", width=15
)
target_lang.set("Hindi")
target_lang.grid(row=0, column=3, padx=8)

source_lang.bind(
    "<<ComboboxSelected>>",
    lambda event: None
)

def translate_text():
    text = input_text.get("1.0", tk.END).strip()

    if not text:
        messagebox.showwarning("Warning", "Please enter some text!")
        return

    source = languages[source_lang.get()]
    target = languages[target_lang.get()]

    try:
        url = "https://api.mymemory.translated.net/get?" + urllib.parse.urlencode({
            "q": text,
            "langpair": source + "|" + target
        })

        req = urllib.request.Request(
            url, headers={"User-Agent": "Mozilla/5.0"}
        )

        with urllib.request.urlopen(req, timeout=20) as response:
            data = json.loads(response.read().decode("utf-8"))

        result = data["responseData"]["translatedText"]

        output_text.config(state="normal")
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, result)
        output_text.config(state="disabled")

    except Exception as error:
        messagebox.showerror("Error", str(error))

tk.Button(
    root, text="TRANSLATE",
    command=translate_text,
    bg="#2463a6", fg="white",
    font=("Arial", 12, "bold"),
    width=20
).pack(pady=10)

tk.Label(root, text="Translated Text:",
         font=("Arial", 12), bg="#eef3f8").pack()

output_text = tk.Text(
    root, height=6, width=65,
    font=("Arial", 11), state="disabled"
)
output_text.pack(pady=10)

tk.Button(
    root, text="COPY TRANSLATION",
    command=copy_translation,
    bg="#23865a", fg="white",
    font=("Arial", 11, "bold"),
    width=20
).pack(pady=10)

root.mainloop()
