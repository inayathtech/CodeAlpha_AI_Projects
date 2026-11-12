
import tkinter as tk
from tkinter import scrolledtext
import re
import math

faqs = [
    ("What is artificial intelligence?",
     "Artificial Intelligence is the ability of machines to perform tasks that normally require human intelligence."),
    ("What is machine learning?",
     "Machine Learning is a branch of AI that allows computers to learn from data."),
    ("What is Python?",
     "Python is a popular, easy-to-learn programming language."),
    ("What is an internship?",
     "An internship provides students with practical work experience."),
    ("What is CodeAlpha?",
     "CodeAlpha is a software development company that provides internship opportunities."),
    ("What is programming?",
     "Programming is the process of writing instructions for a computer."),
    ("What is a chatbot?",
     "A chatbot is a computer program that communicates with users through text or voice."),
    ("What is NLP?",
     "Natural Language Processing helps computers understand and process human language."),
    ("What is deep learning?",
     "Deep Learning is a type of machine learning based on artificial neural networks."),
    ("What is data science?",
     "Data Science involves collecting, processing and analyzing data to find useful information."),
    ("How are you?",
     "I am doing great! Thank you for asking."),
    ("Hello",
     "Hello! Welcome to our FAQ chatbot. How can I help you?"),
    ("What are your features?",
     "I can answer frequently asked questions about AI, Python, programming and internships."),
    ("Thank you",
     "You are welcome! Feel free to ask another question.")
]

stop_words = {
    "is", "the", "a", "an", "what", "are", "how",
    "of", "to", "for", "and", "in", "do", "does",
    "can", "i", "you", "your", "it", "about"
}

def preprocess(text):
    words = re.findall(r"[a-z]+", text.lower())
    return [word for word in words if word not in stop_words]

def cosine_similarity(words1, words2):
    all_words = set(words1) | set(words2)

    if not all_words:
        return 0

    dot = sum(words1.count(w) * words2.count(w)
              for w in all_words)

    magnitude1 = math.sqrt(sum(words1.count(w) ** 2
                               for w in all_words))
    magnitude2 = math.sqrt(sum(words2.count(w) ** 2
                               for w in all_words))

    if magnitude1 == 0 or magnitude2 == 0:
        return 0

    return dot / (magnitude1 * magnitude2)

def get_answer(user_question):
    user_words = preprocess(user_question)

    if not user_words:
        return "Please enter a meaningful question."

    best_score = 0
    best_answer = None

    for question, answer in faqs:
        faq_words = preprocess(question)
        score = cosine_similarity(user_words, faq_words)

        if score > best_score:
            best_score = score
            best_answer = answer

    if best_score < 0.15:
        return "Sorry, I could not find a matching answer. Please try another question."

    return best_answer

def send_message():
    question = entry.get().strip()

    if not question:
        return

    chat_area.config(state="normal")
    chat_area.insert(tk.END, "You: " + question + "\n")

    answer = get_answer(question)

    chat_area.insert(tk.END, "Bot: " + answer + "\n\n")
    chat_area.config(state="disabled")

    entry.delete(0, tk.END)
    chat_area.see(tk.END)

root = tk.Tk()
root.title("AI FAQ Chatbot")
root.geometry("650x550")
root.configure(bg="#eef3f8")

title = tk.Label(
    root,
    text="AI FAQ CHATBOT",
    font=("Arial", 21, "bold"),
    bg="#eef3f8",
    fg="#183153"
)
title.pack(pady=15)

subtitle = tk.Label(
    root,
    text="Ask me anything about AI, Python and internships!",
    font=("Arial", 11),
    bg="#eef3f8"
)
subtitle.pack()

chat_area = scrolledtext.ScrolledText(
    root,
    width=70,
    height=20,
    font=("Arial", 11),
    wrap=tk.WORD,
    state="disabled"
)
chat_area.pack(padx=15, pady=15)

bottom = tk.Frame(root, bg="#eef3f8")
bottom.pack(pady=10)

entry = tk.Entry(bottom, width=48, font=("Arial", 12))
entry.grid(row=0, column=0, padx=5)

send_button = tk.Button(
    bottom,
    text="SEND",
    command=send_message,
    bg="#2463a6",
    fg="white",
    font=("Arial", 11, "bold")
)
send_button.grid(row=0, column=1, padx=5)

entry.bind("<Return>", lambda event: send_message())

root.mainloop()
