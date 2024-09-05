# necessary imports

import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
import argparse
import os

# Function to generate and save word cloud
def generate_wordcloud(input_file, output_file):
    # Load stopwords from nltk
    stop_words = set(stopwords.words('english'))

    # Check if input file exists
    if not os.path.isfile(input_file):
        print(f"Error: The input file '{input_file}' does not exist.")
        return

    # Read the abstract from the input file
    with open(input_file, 'r') as f:
        abstract = f.read().replace('\n', '')

    # Generate the word cloud
    wc = WordCloud(stopwords=stop_words, background_color='white', colormap='viridis', width=800, height=400).generate(abstract)

    # Save the word cloud as an image file
    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')

    # Save the word cloud as a PNG file
    try:
        plt.savefig(output_file, format='png')
        print(f"Word cloud saved to {output_file}")
    except Exception as e:
        print(f"Error saving the file: {e}")
    finally:
        plt.close()  # Close the figure

# Set up argument parsing
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate a word cloud from an input text file.")
    parser.add_argument('input_file', type=str, help="Path to the input text file (e.g., abstract.txt)")
    parser.add_argument('output_file', type=str, help="Path to save the output word cloud image (e.g., wc.png)")

    args = parser.parse_args()

    # Call the function with command-line arguments
    generate_wordcloud(args.input_file, args.output_file)
