import tkinter as tk
from tkinter import messagebox
import threading
import time
import speech_recognition as sr
import nltk
from nltk.corpus import stopwords
from collections import Counter
import string
from wordcloud import WordCloud
import os
import webbrowser

nltk.download('stopwords')

class RecorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Word Bubble Recorder")

        self.is_recording = False
        self.elapsed_time = 0
        self.transcript_file = "transcription.txt"
        self.wordcounts_file = "word_counts.txt"
        self.wordcloud_file = "word_bubble.png"

        # UI Elements
        self.timer_label = tk.Label(root, text="Not Recording")
        self.timer_label.pack(pady=10)

        self.record_button = tk.Button(root, text="Record", command=self.start_recording)
        self.record_button.pack(pady=5)

        self.stop_button = tk.Button(root, text="Stop", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack(pady=5)

        self.generate_button = tk.Button(root, text="Generate Word Map", command=self.generate_word_map, state=tk.DISABLED)
        self.generate_button.pack(pady=20)

        self.recognizer = sr.Recognizer()

    def start_recording(self):
        if self.is_recording:
            return
        self.is_recording = True
        self.elapsed_time = 0
        self.record_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.generate_button.config(state=tk.DISABLED)
        self.timer_label.config(text="Listening for 0 seconds...")

        # Clear transcript file
        with open(self.transcript_file, 'w', encoding='utf-8') as f:
            f.write("")

        # Start timer thread
        threading.Thread(target=self.update_timer, daemon=True).start()
        # Start recording thread
        threading.Thread(target=self.record_mic, daemon=True).start()

    def update_timer(self):
        while self.is_recording:
            self.elapsed_time += 1
            self.timer_label.config(text=f"Listening for {self.elapsed_time} seconds...")
            time.sleep(1)

    def record_mic(self):
        mic = sr.Microphone()
        with mic as source:
            self.recognizer.adjust_for_ambient_noise(source)
            while self.is_recording:
                try:
                    audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=5)
                    text = self.recognizer.recognize_google(audio)
                    with open(self.transcript_file, 'a', encoding='utf-8') as f:
                        f.write(text + "\n")
                except sr.WaitTimeoutError:
                    # No speech detected within timeout, just continue listening
                    continue
                except sr.UnknownValueError:
                    # Can't understand audio, skip
                    continue
                except Exception as e:
                    print("Error:", e)
                    continue

    def stop_recording(self):
        if not self.is_recording:
            return
        self.is_recording = False
        self.record_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.generate_button.config(state=tk.NORMAL)
        self.timer_label.config(text=f"Stopped recording at {self.elapsed_time} seconds")

    def remove_stopwords(self, text):
        stop_words = set(stopwords.words('english'))
        words = text.split()
        filtered_words = [w for w in words if w.lower().strip(string.punctuation) not in stop_words]
        return ' '.join(filtered_words)

    def generate_word_map(self):
        try:
            # Read transcript and remove stop words
            with open(self.transcript_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            cleaned_text = ""
            for line in lines:
                cleaned_line = self.remove_stopwords(line)
                cleaned_text += cleaned_line + "\n"

            # Overwrite transcript with cleaned text
            with open(self.transcript_file, 'w', encoding='utf-8') as f:
                f.write(cleaned_text)

            # Count word frequencies
            words = []
            for line in cleaned_text.split('\n'):
                words += [w.lower().strip(string.punctuation) for w in line.split() if w]

            counter = Counter(words)
            # Filter words with count >=5
            filtered_counts = {w: c for w, c in counter.items() if c >= 5}

            if not filtered_counts:
                messagebox.showinfo("No words", "Not enough words with frequency >= 5 to generate word map.")
                return

            # Generate word cloud
            wc = WordCloud(width=800, height=600, background_color='white')
            wc.generate_from_frequencies(filtered_counts)
            wc.to_file(self.wordcloud_file)

            messagebox.showinfo("Done", f"Word bubble saved as {self.wordcloud_file}")
            # Open image with default viewer
            webbrowser.open(f"file://{os.path.abspath(self.wordcloud_file)}")

        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = RecorderApp(root)
    root.mainloop()
