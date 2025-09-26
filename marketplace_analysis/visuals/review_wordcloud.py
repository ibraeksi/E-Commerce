import re
from wordcloud import STOPWORDS
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def review_wordcloud(df):
    """
    Creates a wordcloud from order reviews
    df = Dataframe with orders
    """

    text = ' '.join(df['review_comment'].dropna().astype(str).tolist())
    text = re.sub(r'[^A-Za-z\s]', '', text)
    text = text.lower()

    stopwords = set(STOPWORDS)
    text = ' '.join(word for word in text.split() if word not in stopwords)

    wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='winter').generate(text)

    fig = plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')

    return fig
