###🎤 Active Mic Word Cloud
Active Mic Word Cloud is a speech-driven Python application that actively listens to your microphone, transcribes spoken words in real-time, filters out stop words, and generates a beautiful word cloud image based on the most frequently spoken terms.

✨ Features
🔊 Live Microphone Recording — Real-time speech recognition using your default microphone.

🧠 Intelligent Filtering — Automatically removes common stop words to highlight meaningful terms.

📊 Word Frequency Analysis — Sorts words by how often they were spoken.

☁️ Word Cloud Generation — Creates a high-quality word cloud image from the final transcript.

🖱️ Simple GUI — User-friendly interface with Start, Stop, and Generate Word Cloud buttons.

📄 Automatic File Handling — Saves transcript and word frequency results to text files.

📦 Packagable as .EXE — Easily wrap it into a Windows executable for simple sharing and usage.

🛠️ Tech Stack
Python 3.10+

SpeechRecognition

WordCloud

Tkinter

NLTK (for stop words)

Matplotlib (optional for inline preview)

🚀 How It Works
Click "Start Recording"
The app listens for speech input from your microphone.

Speak Freely
Say anything — your words are transcribed and logged to transcription.txt.

Click "Stop Recording"
End the session when you're done speaking.

Click "Generate Word Cloud"
The app:

Removes common stop words

Counts word frequency

Generates and saves a word_bubble.png based on top words

