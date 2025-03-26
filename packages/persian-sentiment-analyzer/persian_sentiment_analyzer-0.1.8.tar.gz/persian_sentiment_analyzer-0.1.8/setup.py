from setuptools import setup, find_packages

setup(
    name="persian_sentiment_analyzer",
    version="0.1.8",
    packages=find_packages(),
    install_requires=[
        'hazm>=0.7.0',
        'gensim>=4.0.0',
        'scikit-learn>=1.0.0',
        'numpy>=1.20.0'
    ],
    author="RezaGooner",
    author_email="RezaAsadiProgrammer@Gmail.com",
    description="Persian Sentiment Analysis Library",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/RezaGooner/Sentiment-Survey-Analyzer/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
)
