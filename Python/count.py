'''
from collections import Counter
import re

def get_top_words(file_path, top_n=10):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read().lower()  # Read file and convert to lowercase

    words = re.findall(r'\b\w+\b', text)  # Extract words using regex
    print(words)
    word_counts = Counter(words)  # Count occurrences of each word
    print(word_counts)
    return word_counts.most_common(top_n)  # Return top N words

# Example Usage
file_path = "sample.txt"  # Replace with your file path
top_words = get_top_words(file_path)

# Print Results
for word, count in top_words:
    print(f"{word}: {count}")
'''
import pandas as pd
import re

def get_top_words_pandas(file_path, top_n=10):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read().lower()  # Convert to lowercase

    words = re.findall(r'\b\w+\b', text)  # Extract words using regex
    print(words)
    # Using dictionary to count words
    word_counts = {}
    for word in words:
        word_counts[word] = word_counts.get(word, 0) + 1

    # Convert dictionary to pandas DataFrame
    df = pd.DataFrame(word_counts.items(), columns=['Word', 'Count'])

    # Sort and return top N words
    return df.sort_values(by='Count', ascending=False).head(top_n)

# Example Usage
file_path = "sample.txt"  # Replace with your file path
top_words_df = get_top_words_pandas(file_path)

# Print Results
print(top_words_df)