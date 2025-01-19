import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Download the VADER lexicon if not already done
nltk.download('vader_lexicon')

# Initialize the sentiment analyzer
sia = SentimentIntensityAnalyzer()

def is_question(text):
    """Determine if the text is a question."""
    # Check if the text ends with a question mark
    if text.strip().endswith('?'):
        return True
    
    # Check for common questioning patterns
    questioning_words = ['do', 'does', 'did', 'is', 'are', 'was', 'were', 'can', 'could', 'should', 'would', 'will', 'shall', 'why', 'how', 'what', 'where', 'when', 'who']
    words = text.lower().split()
    if any(words[0] == q_word for q_word in questioning_words):  # Match the first word
        return True
    
    return False

def analyze_sentiment(text):
    """Analyze the sentiment of the given text with special handling for questions."""
    if is_question(text):  # Check if it's a question
        return "Question"

    # Perform sentiment analysis using VADER
    scores = sia.polarity_scores(text)
    if scores['compound'] > 0.05:
        return "Positive"
    elif scores['compound'] < -0.05:
        return "Negative"
    else:
        return "Neutral"
