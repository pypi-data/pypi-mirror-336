import pandas as pd
from tqdm import tqdm

def predict_sentiments_for_file(analyzer, input_file, output_file, summary_file, model_accuracy=None):
    try:
        comments_df = pd.read_csv(input_file, header=None, names=['comment'])
    except Exception as e:
        raise Exception(f"Error reading input file: {e}")
    
    results = []
    error_count = 0
    
    for comment in tqdm(comments_df['comment'], desc="Predicting sentiments"):
        try:
            sentiment = analyzer.predict(comment)
            results.append({'comment': comment, 'sentiment': sentiment})
        except Exception as e:
            print(f"Error predicting sentiment for '{comment}'. : {e}")
            results.append({'comment': comment, 'sentiment': 'error'})
            error_count += 1
    
    results_df = pd.DataFrame(results)
    
    sentiment_counts = results_df['sentiment'].value_counts()
    total_comments = len(results_df)
    
    summary_data = {
        'Sentiment': [
            'number of comments',
            'recommended',
            'not recommended', 
            'no idea',
            'number of errors',
            'model accuracy (%)'
        ],
        'Number': [
            total_comments,
            sentiment_counts.get('recommended', 0),
            sentiment_counts.get('not_recommended', 0),
            sentiment_counts.get('no_idea', 0),
            error_count,
            '-' 
        ],
        'Percentage': [
            100,
            round(sentiment_counts.get('recommended', 0) / total_comments * 100, 2),
            round(sentiment_counts.get('not_recommended', 0) / total_comments * 100, 2),
            round(sentiment_counts.get('no_idea', 0) / total_comments * 100, 2),
            round(error_count / total_comments * 100, 2),
            round(model_accuracy * 100, 2) if model_accuracy is not None else '-'
        ]
    }
    
    summary_df = pd.DataFrame(summary_data)
    
    try:
        results_df.to_csv(output_file, index=False, encoding='utf-8-sig')
        summary_df.to_csv(summary_file, index=False, encoding='utf-8-sig')
        return summary_df
    except Exception as e:
        raise Exception(f"Error saving results: {e}")