import openai
import textwrap
from fpdf import FPDF

API_KEY = "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"
openai.api_key = API_KEY

def transcribe_audio(audio_file_path):
    with open(audio_file_path, "rb") as audio_file:
        transcript = openai.Audio.translate("whisper-1", audio_file)
        wrapped_text = textwrap.fill(transcript["text"], width=95)

    return wrapped_text

def process_recording(audio_file_path):
    # Transcribe audio to text
    wrapped_text = transcribe_audio(audio_file_path)

    # Save the transcript to a text file
    transcript_file_path = audio_file_path.replace(".wav", ".txt")
    with open(transcript_file_path, 'w', encoding='utf-8') as file:
        file.write(wrapped_text)

    print(f"Transcription completed for {audio_file_path}.")

if __name__ == "__main__":
    # Process the recorded audio files
    while True:
        for i in range(1, 100):  # Adjust the range as needed
            audio_file_path = f"recording{i}.wav"
            process_recording(audio_file_path)
