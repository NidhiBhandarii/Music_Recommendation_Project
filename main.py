import pandas as pd
import nltk
from nltk.stem.porter import PorterStemmer

global df


nltk.download('punkt')

#Preserving original ds 
df_original = pd.read_csv(r"C:\Users\Nidhi\OneDrive\Desktop\Internship projects  May 24\Music recommendation\archive\spotify_millsongdata.csv")
df = df_original.copy()

print(df.head())

print(df.shape)

print(df.isnull().sum())

df = df.sample(5000).drop('link', axis=1).reset_index(drop=True)

print(df.head())

print(df['text'][0])

# Preprocessing
df['text'] = df['text'].str.lower().replace(r'^\w\s', ' ').replace(r'\n', ' ', regex=True)
print(df.head())

print(df.tail)

stemmer = PorterStemmer()

def token(txt):
    tokens = nltk.word_tokenize(txt)
    a = [stemmer.stem(w) for w in tokens]
    return " ".join(a)

tk = token("you are beautiful, running, runs, run")
print(tk)


b = df['text'].apply(lambda x:token(x))

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

print (b)

tfid = TfidfVectorizer(analyzer='word', stop_words = 'english')
matrix = tfid.fit_transform(df['text'])
similar = cosine_similarity(matrix)
print(similar)

similar[0]

print(df.tail(10))

print(df[df['song'] == "It's You"].index[0])


# Recommender function
def recommender(song_name):
    idx = df[df['song'] == song_name]. index[0]
    distance = sorted(list(enumerate(similar[idx])), reverse = True, key = lambda x:x[1])
    song =[]
    for s_id in distance[1:11]:
        song.append(df.iloc[s_id[0]].song)
    return song


# Test the recommender function
recommended_songs = recommender("It's You")
print(recommended_songs)


# def recommender(song_name):
#     song_name = song_name.lower().strip()  # Ensure the song name is in the same format
#     if song_name in df['song'].values:
#         idx = df[df['song'] == song_name].index[0]
#         distance = sorted(list(enumerate(similar[idx])), reverse=True, key=lambda x: x[1])
#         song = []
#         for s_id in distance[1:10]:
#             song.append(df.iloc[s_id[0]].song)
#         return song
#     else:
#         return f"Song '{song_name}' not found in the dataset."

import pickle

pickle.dump(similar, open("similarity","wb"))
pickle.dump(df, open("df","wb"))

