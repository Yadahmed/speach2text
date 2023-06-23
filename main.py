import tkinter as tk
import threading
import pyaudio
import wave
import openai
import textwrap
import os

max_line_length = 95
max_tokens = 50  # Adjust the value as per your requirements
API_KEY = "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"
openai.api_key = API_KEY

transcribed_text = ""
is_recording = True

def transcribe_audio(audio_file):
    global transcribed_text

    transcript = openai.Audio.translate("whisper-1", audio_file)
    wrapped_text = textwrap.fill(transcript["text"], width=max_line_length)

    transcribed_text += wrapped_text + "\n"

    # Update the text in the GUI
    text_area.config(state='normal')
    text_area.delete('1.0', tk.END)  # Clear the previous content
    text_area.insert(tk.END, transcribed_text)
    text_area.config(state='disabled')

def save_transcribed_text():
    with open("output.txt", 'w') as output_file:
        output_file.write(transcribed_text)

def record_voice():
    global is_recording

    # Create a PyAudio object
    pa = pyaudio.PyAudio()

    counter = 1  # Counter for naming the recordings

    while is_recording:
        # List of file paths to delete
        file_paths = [f"recording{counter-1}.wav", f"recording{counter-1}.txt"]

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

def save_and_quit():
    save_transcribed_text()
    window.quit()

def close_program():
    global is_recording
    is_recording = False
    save_transcribed_text()
    window.quit()

# Create the GUI window
window = tk.Tk()
window.title("Voice Transcription")
window.geometry("800x600")

# Create a text area to display the transcribed text
text_area = tk.Text(window, state='disabled')
text_area.pack(fill=tk.BOTH, expand=True)

def start_recording():
    thread = threading.Thread(target=record_voice)
    thread.start()

# Create a button to start the voice recording
start_button = tk.Button(window, text="Start Recording", command=start_recording)
start_button.pack()

# Create a button to close the program and save the transcribed text
close_button = tk.Button(window, text="Close Program", command=close_program)
close_button.pack()

window.protocol("WM_DELETE_WINDOW", save_and_quit)

window.mainloop()