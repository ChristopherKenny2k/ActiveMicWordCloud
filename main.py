import speech_recognition as sr

recognizer = sr.Recognizer()
mic = sr.Microphone()

output_file = "transcription.txt"

print("Listening... (Press Ctrl+C to stop)\n")

with open(output_file, "a", encoding="utf-8") as f:
    try:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            while True:
                try:
                    # Adjust these as needed for responsiveness
                    audio = recognizer.listen(source, timeout=1, phrase_time_limit=4)
                    text = recognizer.recognize_google(audio)
                    print(text)
                    f.write(text + "\n")
                    f.flush()
                except sr.UnknownValueError:
                    pass  # skip unrecognized speech
                except sr.WaitTimeoutError:
                    pass  # skip if no speech detected quickly
                except sr.RequestError as e:
                    print(f"API request error: {e}")
    except KeyboardInterrupt:
        print("\nStopped by user.")
