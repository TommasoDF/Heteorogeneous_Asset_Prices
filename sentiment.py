import pandas as pd
import re
import nltk
import numpy as np
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

df = pd.read_csv("results\Bitcoin_from_2021-12-22_23-59-49_to_2021-10-04_18-01-43.csv")
df = df.set_index('Datetime')
df.index = pd.to_datetime(df.index)

### Data Cleaning
pat1 = r'@[A-Za-z0-9]+' # this is to remove any text with @....
pat2 = r'https?://[A-Za-z0-9./]+'  # this is to remove the urls
combined_pat = r'|'.join((pat1, pat2)) 
pat3 = r'[^a-zA-Z]' # to remove every other character except a-z & A-Z
combined_pat2 = r'|'.join((combined_pat,pat3)) # we combine pat1, pat2 and pat3 to pass it in the cleaning steps

### Starting the cleaning
ps = PorterStemmer()
cleaned_tweets = []
df_short = df[0:10]
for i in range(0, len(df_short)) :
    if( (i+1)%10000 == 0 ):
        print("Tweets %d of %d has been processed" % ( i+1, len(df['Text'][0:10]) ))
    tweets = re.sub(combined_pat2,' ',df['Text'][i])
    tweets = tweets.lower()
    tweets = tweets.split()
    tweets = [ps.stem(word) for word in tweets if not word in set(stopwords.words('english'))]
    tweets = ' '.join(tweets)
    cleaned_tweets.append(tweets)


nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Instantiate the sentiment intensity analyzer
vader = SentimentIntensityAnalyzer()

df_short['cleaned_tweets'] = np.array(cleaned_tweets)
scores = df_short['cleaned_tweets'].apply(vader.polarity_scores).tolist()

# Convert the 'scores' list of dicts into a DataFrame
scores_df = pd.DataFrame(scores, index=df_short.index)# Join the DataFrames of the news and the list of dicts
parsed_and_scored_news = df_short.join(scores_df)