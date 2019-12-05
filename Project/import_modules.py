import bz2
import codecs
# nltk.download()
import nltk
import lxml
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
import string 
import gensim
import numpy as np
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
from sklearn.cluster import KMeans