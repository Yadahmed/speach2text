import pyaudio
import wave
import openai
import textwrap
import os
import networkx as nx
import numpy as np
from nltk.cluster.util import cosine_distance
from nltk.corpus import stopwords
import nltk
nltk.download("stopwords")

API_KEY = "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"
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

    return wrapped_text

def package_the_texts(original, summary):
    with open("package.txt", "a") as packaged_file:
        packaged_file.truncate(0)

        original = open(original, "r")
        packaged_file.write("Original:\n")
        packaged_file.write(original.read())

        summary = open(summary, "r")
        packaged_file.write("Summary:\n")
        packaged_file.write(summary.read())

        return packaged_file

def read_article(file_name):
    file = open(file_name, "r", encoding='utf-8')
    filedata = file.readlines()
    article = filedata[0].split(". ")
    sentences = []
    for sentence in article:
        sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" "))
    sentences.pop()
    return sentences

def sentence_similarity(sent1, sent2, stopwords=None):
    if stopwords is None:
        stopwords = []
    sent1 = [w.lower() for w in sent1]
    sent2 = [w.lower() for w in sent2]

    all_words = list(set(sent1+sent2))
    vector1 = [0]*len(all_words)
    vector2 = [0]*len(all_words)
    for w in all_words:
        if w in stopwords:
            continue
        vector1[all_words.index(w)] += 1
    for w in all_words:
        if w in stopwords:
            continue
        vector2[all_words.index(w)] += 1

    return 1-cosine_distance(vector1, vector2)

def gen_sim_matrix(sentences, stop_words):
    similarity_matrix = np.zeros((len(sentences), len(sentences)))
    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1 == idx2:
                continue
            similarity_matrix[idx1][idx2] = sentence_similarity(
                sentences[idx1], sentences[idx2], stop_words)

    return similarity_matrix

def generate_summary(file_name, top_n=5):
    stop_words = stopwords.words("english")  # fix this
    summurize_text = []
    sentences = read_article(file_name)
    sentence_similarity_matrix = gen_sim_matrix(sentences, stop_words)
    sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_matrix)
    scores = nx.pagerank(sentence_similarity_graph)
    ranked_sentences = sorted(
        ((scores[i], s)for i, s in enumerate(sentences)), reverse=True)
    for i in range(top_n):
        summurize_text.append(" ".join(ranked_sentences[i][1]))
    print("summary \n", ". ".join(summurize_text))


if __name__ == "__main__":
    # Define the callback function to display the text
    def display_text(text):
        # Print the text
        print(text)

    # Start the voice recording.
    originial = record_voice(display_text)
    summary = generate_summary(original)
    package_the_texts(original, summary)
