from LDA import *
from sklearn.cluster import KMeans
clustering=KMeans(n_clusters=5, random_state=5)
clustering.fit(all_topics_numpy)
df_new['Labels'] = clustering.labels_