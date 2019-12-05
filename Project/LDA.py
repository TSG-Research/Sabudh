from create_corpus import *
# Build LDA model
lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                           id2word=id2word,
                                           num_topics=3,
                                           random_state=100,
                                           update_every=1,
                                           chunksize=100,
                                           passes=10,
                                           alpha='auto',
                                           per_word_topics=True)
doc_t = lda_model.get_document_topics(bow = corpus, minimum_probability=0.0)      
all_topics_csr = gensim.matutils.corpus2csc(doc_t)
all_topics_numpy = all_topics_csr.T.toarray()                                     