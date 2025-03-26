# Persian Sentiment Analyzer

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

A Python library for sentiment analysis of Persian (Farsi) text, capable of classifying opinions as "recommended", "not_recommended", or "no_idea".

## Features

- **Text Preprocessing**: Normalization, tokenization, stemming, and stopword removal for Persian text
- **Word Embeddings**: Built-in Word2Vec implementation for Persian language
- **Sentiment Classification**: Logistic Regression classifier trained on Persian sentiment data
- **Model Persistence**: Save and load trained models for future use
- **Batch Processing**: Analyze sentiment for multiple texts at once

## Installation

```bash
pip install persian-sentiment-analyzer
```

## Dependencies
- Python 3.6+

- hazm

- gensim

- scikit-learn

- numpy

- pandas

## Usage

### Basic Usage

``` bash
from persian_sentiment_analyzer import SentimentAnalyzer

# Initialize with a pre-trained model
analyzer = SentimentAnalyzer(model_path="path/to/pretrained_model")

# Predict sentiment
result = analyzer.predict("این محصول بسیار عالی است")
print(result)  # Output: 'recommended'
```

### Training Your Own Model

``` bash
from persian_sentiment_analyzer import SentimentAnalyzer
import pandas as pd

# Load your dataset
data = pd.read_csv("persian_reviews.csv")
texts = data['text'].tolist()
labels = data['label'].values  # 0: not_recommended, 1: recommended, 2: no_idea

# Initialize analyzer
analyzer = SentimentAnalyzer()

# Preprocess and tokenize texts
tokenized_texts = [analyzer.preprocessor.preprocess_text(text) for text in texts]

# Train Word2Vec model
analyzer.train_word2vec(tokenized_texts, vector_size=100)

# Prepare feature vectors
X = np.array([analyzer.sentence_vector(tokens) for tokens in tokenized_texts])

# Train classifier
analyzer.train_classifier(X, labels)

# Save the trained model
analyzer.save_model("my_persian_model")
```

### Batch Processing

```bash
from persian_sentiment_analyzer import predict_sentiments_for_file

# Process a CSV file containing Persian comments
results_summary = predict_sentiments_for_file(
    analyzer,
    input_file="comments.csv",
    output_file="results.csv",
    summary_file="summary.csv"
)

print(results_summary)
```

## Model Architecture
1- Text Preprocessing:

- Normalization (Hazm)

- Tokenization

- Stemming

- Stopword removal

2- Feature Extraction:

- Word2Vec embeddings (100 dimensions)

- Sentence vectors (average of word vectors)

3- Classification:

- Logistic Regression with L2 regularization

## Performance
The pre-trained model achieves the following performance on our test set:

Metric	Value
Accuracy	85.2%
Precision	84.7%
Recall	85.0%
F1-score	84.8%

License
This project is licensed under the MIT [License](https://github.com/RezaGooner/Sentiment-Survey-Analyzer/blob/main/LICENSE) - see the LICENSE file for details


> Github : RezaGooner