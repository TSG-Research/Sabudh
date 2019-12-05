from data_cleaning import *
wn = nltk.WordNetLemmatizer() #wordnet is a dictionary
def lemmatizing (tokenized_text):
    text = [wn.lemmatize(word) for word in tokenized_text]
    return text
df_lemmatized = df_stopwords.apply(lambda c: lemmatizing(c))
df_new = df_lemmatized.str.join(" ")
df_new= pd.DataFrame(df_new, columns=['Description'])