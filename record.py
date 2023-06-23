import pyaudio
import wave
import time
import os

def record_voice():
    # Create a PyAudio object.
    pa = pyaudio.PyAudio()

    counter = 1  # Counter for naming the recordings

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

        time.sleep(5)  # Wait for 5 seconds before the next recording

    pa.terminate()


if __name__ == "__main__":
    # Record the voice endlessly, saving files every 5 seconds.
    record_voice()