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
from datetime import datetime
import shutil



nltk.download('stopwords')

#main app class
class RecorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Word Bubble Recorder")

        self.is_recording = False
        self.elapsed_time = 0
        self.transcript_file = "transcription.txt"
        self.wordcounts_file = "word_counts.txt"
        self.wordcloud_file = "word_bubble.png"
        self.wordcloud_file = "WordCloud/word_bubble.png"

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

        # transcript file gets cleared (maybe create option to continue transcript or start new)
        with open(self.transcript_file, 'w', encoding='utf-8') as f:
            f.write("")

        # timer start
        threading.Thread(target=self.update_timer, daemon=True).start()
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
                    continue
                except sr.UnknownValueError:
                    # skip line if cant infer what was said, unfortunately a big limitation of this voice recog. module
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
        #NLTK Stopwords
        NLTK_stop_words = set(stopwords.words('english'))

        #CUSTOM STOP WORDS (good idea to check word cloud after first use to see what words you would like to omit in future uses)
        self.custom_stopwords = set(["like", "oh", "get", "that's"])

        all_stopwords = NLTK_stop_words.union(self.custom_stopwords)
        words = text.split()
        filtered_words = [w for w in words if w.lower().strip(string.punctuation) not in all_stopwords]
        return ' '.join(filtered_words)

    def generate_word_map(self):
        try:

            #If folders aren't present, create them
            os.makedirs("Transcripts", exist_ok=True)  
            os.makedirs("WordCloud", exist_ok=True) 

            # saves original transcript as "transcriptdd-mm"
            today = datetime.today()
            dated_filename = today.strftime("%d-%m")
            original_path = f"Transcripts/transcript_{dated_filename}.txt"
            cleaned_path = f"Transcripts/transcriptCleaned_{dated_filename}.txt"
            shutil.copy(self.transcript_file, original_path)


            # read and clean transcript
            with open(self.transcript_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            

            cleaned_text = ""
            for line in lines:
                cleaned_line = self.remove_stopwords(line)
                cleaned_text += cleaned_line + "\n"

            # save cleaned transcript as transcriptCleaned.txt
            cleaned_file = "transcriptCleaned.txt"
            with open(cleaned_file, 'w', encoding='utf-8') as f:
                f.write(cleaned_text)

            # frequency count using cleaned file (free of stop words)
            words = []
            for line in cleaned_text.split('\n'):
                words += [w.lower().strip(string.punctuation) for w in line.split() if w]

            counter = Counter(words)
            # filter out low-frequency words (e.g., < 4 occurrences) Note*: change this parameter to your liking, 4 works well for a very filled word cloud
            filtered_counts = {w: c for w, c in counter.items() if c >= 4}

            if not filtered_counts:
                messagebox.showinfo("No words", "Not enough words with frequency >= 4 to generate word map.")
                return

            # save word counts to file (overwrite)
            with open("word_counts.txt", 'w', encoding='utf-8') as f:
                for word, count in sorted(filtered_counts.items(), key=lambda x: x[1], reverse=True):
                    f.write(f"{word}: {count}\n")

            # create and save word cloud
            wc = WordCloud(width=800, height=600, background_color='white')
            wc.generate_from_frequencies(filtered_counts)
            wc.to_file(self.wordcloud_file)

            messagebox.showinfo("Done", f"Word bubble saved as {self.wordcloud_file}")
            webbrowser.open(f"file://{os.path.abspath(self.wordcloud_file)}")

        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RecorderApp(root)
    root.mainloop()

