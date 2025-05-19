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
            # Remove punctuation from the word for stop word matching
            word_stripped = word.strip(string.punctuation).lower()
            if word_stripped not in stop_words and word_stripped != '':
                cleaned_words.append(word)
        cleaned_lines.append(' '.join(cleaned_words))

    # Overwrite the original file with cleaned text
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

    # Tokenize words (split by whitespace), clean punctuation & lowercase
    words = [word.strip(string.punctuation).lower() for word in text.split()]
    words = [w for w in words if w]  # Remove empty strings

    # Count frequencies
    counter = Counter(words)

    # Sort by frequency descending and filter by min_count
    sorted_words = [(word, count) for word, count in counter.most_common() if count >= min_count]

    # Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        for word, count in sorted_words:
            f.write(f"{word}, {count}\n")

    print(f"Word counts (≥ {min_count}) saved to {output_path}")

if __name__ == "__main__":
    count_words("transcription.txt", "word_counts.txt", min_count=5)

def create_wordcloud_from_file(wordcounts_path, output_image_path):
    # Read word counts file
    word_freq = {}
    with open(wordcounts_path, 'r', encoding='utf-8') as f:
        for line in f:
            word, count = line.strip().split(', ')
            word_freq[word] = int(count)

    # Create word cloud object
    wc = WordCloud(width=800, height=600, background_color='white')

    # Generate word cloud from frequencies
    wc.generate_from_frequencies(word_freq)

    # Save to file
    wc.to_file(output_image_path)
    print(f"Word cloud saved to {output_image_path}")

    # Optional: show the image inline (if running interactively)
    # plt.imshow(wc, interpolation='bilinear')
    # plt.axis('off')
    # plt.show()

if __name__ == "__main__":
    create_wordcloud_from_file("word_counts.txt", "word_bubble.png")