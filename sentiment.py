import pandas as pd
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

df = pd.read_csv("Bitcoin_from_2021-12-22_23-59-49_to_2021-10-04_18-01-43.csv")
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

for i in range(0, len(df['Text'][0:10])) :
    tweets = re.sub(combined_pat2,' ',df['Text'][i])
    tweets = tweets.lower()
    tweets = tweets.split()
    tweets = [ps.stem(word) for word in tweets if not word in set(stopwords.words('english'))]
    tweets = ' '.join(tweets)
    cleaned_tweets.append(tweets)

nltk.download('vader_lexicon')