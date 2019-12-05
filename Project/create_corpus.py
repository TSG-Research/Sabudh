from lematize import *
# Create Dictionary
id2word = corpora.Dictionary(df_lemmatized)

# Create Corpus
texts = df_lemmatized
corpus = [id2word.doc2bow(text) for text in texts]