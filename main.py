import pyaudio
import wave
import openai
import textwrap
import os


API_KEY = "API_KEY"
openai.api_key = API_KEY


def record_voice(callback):
    # Create a PyAudio object.
    pa = pyaudio.PyAudio()

    counter = 1  # Counter for naming the recordings
    output_file = "output.txt"  # Name of the output file

    # Open the output file in append mode
    with open(output_file, 'a', encoding='utf-8') as file:
        while True:

            # List of file paths to delete
            file_paths = [f"recording{counter-1}.wav"]

            for file_path in file_paths:
                if os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                        print(f"File '{file_path}' deleted successfully.")
                    except OSError as e:
                        print(f"Error deleting file '{file_path}': {e}")
                else:
                    print(f"File '{file_path}' does not exist.")

            # Open a microphone input stream.
            in_stream = pa.open(format=pyaudio.paInt16,
                                channels=1,
                                rate=44100,
                                input=True,
                                frames_per_buffer=1024)

            # Start recording.
            frames = []
            for _ in range(int(44100 / 1024 * 5)):
                # Get the audio data from the microphone.
                data = in_stream.read(1024)
                frames.append(data)

            # Stop recording.
            in_stream.stop_stream()
            in_stream.close()

            # Save the recorded audio to a WAV file.
            wave_file = wave.open(f"recording{counter}.wav", "wb")
            wave_file.setnchannels(1)
            wave_file.setsampwidth(pa.get_sample_size(pyaudio.paInt16))
            wave_file.setframerate(44100)
            wave_file.writeframes(b''.join(frames))
            wave_file.close()

            counter += 1  # Increment the counter for the next recording

            audio_file = open(f"recording{counter-1}.wav", "rb")
            transcript = openai.Audio.translate("whisper-1", audio_file)
            wrapped_text = textwrap.fill(transcript["text"], width=95)
            audio_file.close()

            # Append the generated text to the output file
            file.write(wrapped_text)

            callback(wrapped_text)


if __name__ == "__main__":
    # Define the callback function to display the text
    def display_text(text):
        # Print the text
        print(text)

    # Start the voice recording loop with the callback function
    record_voice(display_text)
