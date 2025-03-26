from setuptools import setup, find_packages

setup(
    name="persian_sentiment_analyzer",
    version="0.1.0",
    description="A Persian sentiment analysis library",
    author="RezaGooner",
    author_email="RezaAsadiProgrammer@Gmail.com",
    packages=find_packages(),
    install_requires=[
        'hazm',
        'gensim',
        'scikit-learn',
        'pandas',
        'numpy',
        'tqdm'
    ],
    package_data={
        'persian_sentiment_analyzer': ['data/*'],
    },
)