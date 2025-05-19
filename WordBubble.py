import nltk
from nltk.corpus import stopwords
import string
from collections import Counter
import string
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def remove_stopwords_from_txt(file_path):
    stop_words = set(stopwords.words('english'))

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    cleaned_lines = []

    for line in lines:
        words = line.strip().split()
        cleaned_words = []
        for word in words:
            # strip punctuation
            word_stripped = word.strip(string.punctuation).lower()
            if word_stripped not in stop_words and word_stripped != '':
                cleaned_words.append(word)
        cleaned_lines.append(' '.join(cleaned_words))

    # overwrite text file with new (stripped) text, stop words removed
    with open(file_path, 'w', encoding='utf-8') as f:
        for line in cleaned_lines:
            if line.strip():
                f.write(line + '\n')

    print(f"Stop words removed and file overwritten: {file_path}")

if __name__ == "__main__":
    remove_stopwords_from_txt("transcription.txt")

def count_words(file_path, output_path, min_count=10):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # tokenisation of words
    words = [word.strip(string.punctuation).lower() for word in text.split()]
    words = [w for w in words if w] 

    # frequency count
    counter = Counter(words)

    # sort desc
    sorted_words = [(word, count) for word, count in counter.most_common() if count >= min_count]

    # create output in format word, x (where x is count)
    with open(output_path, 'w', encoding='utf-8') as f:
        for word, count in sorted_words:
            f.write(f"{word}, {count}\n")

    print(f"Word counts (≥ {min_count}) saved to {output_path}")

if __name__ == "__main__":
    count_words("transcription.txt", "word_counts.txt", min_count=5)

def create_wordcloud_from_file(wordcounts_path, output_image_path):
    # open the word count file
    word_freq = {}
    with open(wordcounts_path, 'r', encoding='utf-8') as f:
        for line in f:
            word, count = line.strip().split(', ')
            word_freq[word] = int(count)

    # creating the word cloud canvas
    wc = WordCloud(width=800, height=600, background_color='white')

    # generate the cloud 
    wc.generate_from_frequencies(word_freq)

    wc.to_file(output_image_path)
    print(f"Word cloud saved to {output_image_path}")


if __name__ == "__main__":
    create_wordcloud_from_file("word_counts.txt", "word_bubble.png")