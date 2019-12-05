
from data_decode import *
def clean_data():
    CLEAN = re.compile('<.*?>')
    titles = decode_data()
    new_text = [CLEAN.sub('', a.text).strip() for a in titles] 
    return new_text
clean_text = clean_data()
df=pd.DataFrame(clean_text,columns=["Description"])

def remove_punc(text):
    text_nopunct = "".join([char for char in text if char not in string.punctuation])
    return text_nopunct
df_clean = df.apply(lambda x: remove_punc(x.Description),axis=1)

def token(text):
    tokens = re.split('\W+', text)#w+ means that either a word character (A-Za-z-9_) or a dash (-) can go there.
    return tokens
df_tokens = df_clean.apply(lambda z: token(z.lower()))

stopwords = nltk.corpus.stopwords.words('english')
def remove_stopwords (tokenized_list):
    text = [word for word in tokenized_list if word not in stopwords]# to remove all stopwords
    return text
df_stopwords = df_tokens.apply(lambda a: remove_stopwords(a))
