import networkx as nx
import numpy as np
from nltk.cluster.util import cosine_distance
from nltk.corpus import stopwords
import nltk
nltk.download("stopwords")


def read_article(file_name):
    file = open(file_name, "r", encoding='utf-8')
    filedata = file.readlines()
    article = filedata[0].split(". ")
    sentences = []
    for sentence in article:
        sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" "))
    sentences.pop()
    return sentences


# def read_article(file_name):
#     with open(file_name, 'r', encoding='utf-8') as file:
#         filedata = file.readlines()
#     article = ' '.join(filedata)
#     sentences = split_into_sentences(article)
#     return sentences


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


# def generate_summary(file_name, top_n=5):
#     stop_words = stopwords.words("english")  # fix this
#     summurize_text = []
#     sentences = read_article(file_name)
#     sentence_similarity_matrix = gen_sim_matrix(sentences, stop_words)
#     sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_matrix)
#     scores = nx.pagerank(sentence_similarity_graph)
#     ranked_sentences = sorted(
#         ((scores[i], s)for i, s in enumerate(sentences)), reverse=True)
#     for i in range(top_n):
#         summurize_text.append(" ".join(ranked_sentences[i][1]))
#     print("summary \n", ". ".join(summurize_text))


def generate_summary(file_name, top_n=5):
    stop_words = stopwords.words("english")
    summurize_text = []
    sentences = read_article(file_name)
    sentence_similarity_matrix = gen_sim_matrix(sentences, stop_words)
    sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_matrix)
    scores = nx.pagerank(sentence_similarity_graph)
    ranked_sentences = sorted(
        ((scores[i], s) for i, s in enumerate(sentences)), reverse=True)
    for i in range(top_n):
        summurize_text.append(" ".join(ranked_sentences[i][1]))
    return summurize_text


def save_summary(summary_text):
    with open("summary.txt", 'w', encoding='utf-8') as summary_file:
        summary_file.write(". ".join(summary_text))


summary_text = generate_summary(
    "C:\\Users\\lanya\\Desktop\\Hproject\\output.txt", 2)
save_summary(summary_text)
