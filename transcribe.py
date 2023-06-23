import openai
import textwrap
import os

API_KEY = "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"
openai.api_key = API_KEY

def transcribe_audio(file_path):
    audio_file = open(file_path, "rb")
    transcript = openai.Audio.translate("whisper-1", audio_file)
    wrapped_text = textwrap.fill(transcript["text"], width=95)
    audio_file.close()

    with open(f"{file_path}.txt", 'w', encoding='utf-8') as file:
        file.write(wrapped_text)

    for char in wrapped_text:
        print(char, end='', flush=True)
        # time.sleep(0.001)


if __name__ == "__main__":
    # Transcribe the recorded audio files
    directory = os.getcwd()
    while True:
        for file in os.listdir(directory):
            if file.endswith(".wav"):
                file_path = os.path.join(directory, file)
                transcribe_audio(file_path)
