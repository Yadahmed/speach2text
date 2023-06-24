import tkinter as tk
import threading
import pyaudio
import wave
import openai
import textwrap
import os
from googletrans import Translator
from google.cloud import translate_v2 as translate

max_line_length = 95
max_tokens = 50  # Adjust the value as per your requirements
API_KEY = "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"
openai.api_key = API_KEY

translator = Translator()
translate_client = translate.Client()

transcribed_text = ""
current_language = "ku"  # Default language is Kurdish
counter = 1

def transcribe_audio(audio_file):
    global transcribed_text, current_language

    transcript = openai.Audio.translate("whisper-1", audio_file)
    original_text = transcript["text"]
    wrapped_text = textwrap.fill(original_text, width=max_line_length)

    if current_language == "ku":
        translated_text = translate_text("en", original_text)  # Translate to English
    else:
        translated_text = original_text

    transcribed_text += translated_text + "\n"  # Append the new text to the existing text

    # Update the text in the GUI
    text_area.config(state='normal')
    text_area.delete('end - 2 lines', tk.END)  # Clear the last two lines
    text_area.insert(tk.END, translated_text + "\n")  # Insert the new text
    text_area.config(state='disabled')

def translate_text(target: str, text: str) -> str:
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    if isinstance(text, bytes):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target)

    return result["translatedText"]

def record_voice():
    global counter

    # Create a PyAudio object
    pa = pyaudio.PyAudio()

    while True:
        # List of file paths to delete
        file_paths = [f"recording{counter - 1}.wav", f"recording{counter - 1}.txt"]

        for file_path in file_paths:
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    print(f"File '{file_path}' deleted successfully.")
                except OSError as e:
                    print(f"Error deleting file '{file_path}': {e}")
            else:
                print(f"File '{file_path}' does not exist.")

        # Open a microphone input stream
        in_stream = pa.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=44100,
                            input=True,
                            frames_per_buffer=1024)

        # Start recording
        frames = []
        for _ in range(int(44100 / 1024 * 5)):
            # Get the audio data from the microphone
            data = in_stream.read(1024)
            frames.append(data)

        # Stop recording
        in_stream.stop_stream()
        in_stream.close()

        # Save the recorded audio to a WAV file
        wave_file = wave.open(f"recording{counter}.wav", "wb")
        wave_file.setnchannels(1)
        wave_file.setsampwidth(pa.get_sample_size(pyaudio.paInt16))
        wave_file.setframerate(44100)
        wave_file.writeframes(b''.join(frames))
        wave_file.close()

        # Create a separate thread for transcription
        audio_file = open(f"recording{counter}.wav", "rb")
        transcribe_thread = threading.Thread(target=transcribe_audio, args=(audio_file,))
        transcribe_thread.start()

        counter += 1  # Increment the counter for the next recording

    pa.terminate()

def save_transcribed_text():
    with open("output.txt", 'w', encoding='utf-8') as output_file:
        output_file.write(transcribed_text)

def start_recording():
    thread = threading.Thread(target=record_voice)
    thread.start()

def toggle_language():
    global current_language, transcribed_text

    # Toggle the current language
    current_language = "en" if current_language == "ku" else "ku"

    # Translate the existing transcribed text to the new language
    if current_language == "ku":
        translated_text = translate_text("ku", transcribed_text)  # Translate to Kurdish
    else:
        translated_text = translate_text("en", transcribed_text)  # Translate to English

    # Update the text in the GUI
    text_area.config(state='normal')
    text_area.delete('1.0', tk.END)  # Clear the previous content
    text_area.insert(tk.END, translated_text)
    text_area.config(state='disabled')

def close_program():
    save_transcribed_text()
    window.destroy()

    # Delete all audio files
    for file_name in os.listdir():
        if file_name.endswith(".wav"):
            os.remove(file_name)

    # Stop the program execution
    os._exit(0)

# Create the GUI window
window = tk.Tk()
window.title("Voice Transcription")
window.geometry("800x600")

# Create a text area to display the transcribed text
text_area = tk.Text(window, state='disabled')
text_area.pack(fill=tk.BOTH, expand=True)

# Create a button to start the voice recording
start_button = tk.Button(window, text="Start Recording", command=start_recording)
start_button.pack()

# Create a button to toggle the language
toggle_button = tk.Button(window, text="Toggle Language", command=toggle_language)
toggle_button.pack()

# Create a button to close the program and save the transcribed text
close_button = tk.Button(window, text="Close and Save", command=close_program)
close_button.pack()

window.mainloop()
