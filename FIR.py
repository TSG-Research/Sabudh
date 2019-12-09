import fasttext
import io
import os
from pdf2image import convert_from_path
import pandas as pd
from tesserocr import PyTessBaseAPI
from PIL import Image
import sys
from os import path
from cltk.stop.punjabi.stops import STOPS_LIST
import re
from inltk.inltk import get_embedding_vectors
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import os
from pdf2image import convert_from_path
from inltk.inltk import tokenize
import string
import pandas as pd
from nltk.corpus import wordnet  # for english words
import os
import tesserocr
from tesserocr import PyTessBaseAPI
import os
import re

try:
    from PIL import Image
except ImportError:
    import Image
    import pytesseract

class Preprocessing:

# pdftoimage function is used to convert FIR's present in form of PDF to images by using pdf2image
    def pdftoimage(self):

        # folders where images are kept
        rootdir = ['/home/nitpreet/Documents/Fir/FIR/FEB-2019/', '/home/nitpreet/Documents/Fir/FIR/JAN-2019/',
                   '/home/nitpreet/Documents/Fir/FIR/March-2019/']
        file_paths = []  # will contain the paths of the file
        file_name = []  # will contain the name of the file
        for values in rootdir:
            os.mkdir(
                '/home/nitpreet/Desktop/' + values[33:36])  # for making the folder in desktop with the name FEB, JAN, Mar
            os.chdir('/home/nitpreet/Desktop/' + values[33:36])  # for changing the directory to those created folders
            for subdir, dirs, files in os.walk(values):
                for file in files:
                    if file.lower().endswith(".pdf"):  # checking the entire folder for the files ending with pdf

                        file_paths.append(subdir + '/' + file)
                        file_name.append(file)
            file_des = dict(zip(file_paths, file_name))  # creating the dictionary of filepaths and file names

            for key, value in file_des.items():
                pages = convert_from_path(key)
                image_counter = 1
                for page in pages:
                    filename = value.replace(".pdf", "") + "_" + str(image_counter) + ".jpg"
                    page.save(filename, 'JPEG')
                    image_counter = image_counter + 1
            return

#Image2Text Function is used to convert Punjabi FIR images extracted from PDF to Punjabi text
    def Image2Text(ImgFiles,ImageFileSplitted,FIRDf):
        ImageFileSplitted=set(ImageFileSplitted)
        with PyTessBaseAPI(path='C:/Users/Aman/Documents/Python Scripts/tesserocr-master/tessdata/.',
                           lang='script/Gurmukhi+eng') as api:
            for img in ImageFileSplitted:

                FIRCompContent = ""

                if img.lower().__contains__(', dated'):
                    ImagesDtLoc = img.split(', dated')[1]
                elif img.lower().__contains__(',dated'):
                    ImagesDtLoc = img.split(',dated')[1]
                else:
                    ImagesDtLoc = img.split(',')[1]

                if ImagesDtLoc.lower().__contains__('-19 '):
                    ImageLocation=ImagesDtLoc.split('-19 ',1)[1]
                elif ImagesDtLoc.lower().__contains__('19-'):
                    ImageLocation = ImagesDtLoc.split('19-', 1)[1]
                elif ImagesDtLoc.lower().__contains__('-2019 '):
                    ImageLocation = ImagesDtLoc.split('-2019 ', 1)[1]

                ImageDt=ImagesDtLoc.split(ImageLocation,1)[0]

                for iter in range(3,9):
                    ImageNminPNG=img + '_' + str(iter) + '.jpg'
                    Textdata=[]

                    if(path.exists(ImageNminPNG))==True:
                        print(ImageNminPNG)
                        column = Image.open(ImageNminPNG)
                        gray = column.convert('L')
                        blackwhite = gray.point(lambda x: 0 if x < 200 else 255, '1')
                        blackwhite.save(ImageNminPNG)
                        api.SetImageFile(ImageNminPNG)
                        Text=api.GetUTF8Text()

                        Textdata.append(Text)
                        FIRDf,FIRCompContent = Preprocessing.Text2Dataframe(FIRDf, Textdata,FIRCompContent)
                    else:
                        break
                FIRDf = FIRDf.append({'First_Information_Contents': FIRCompContent,'Date_and_Location': ImagesDtLoc,'FIR_Location': ImageLocation,'FIR_Date':ImageDt,'PDF_Name': img}, ignore_index=True)
                #FIRDf = FIRDf.append({'Date_and_Location': ImagesDtLoc}, ignore_index=True)
                #FIRDf = FIRDf.append({}, ignore_index=True)

        return FIRDf


#Text2Dataframe function is used to convert Punjabi text data present in First Information content to DataFrame
    def Text2Dataframe(FIRDf,Textdata,FIRCompContent):

        listToStr = ' '.join(map(str, Textdata))
        FIRContentPresent=0

        if listToStr.lower().__contains__('first information contents'):
            FIRContentPresent = 1
            Content = listToStr.lower().split('first information contents')[1]
        elif(listToStr.lower().__contains__('12') ):
            FIRContentPresent = 1
            Content = listToStr.lower().split('12',1)[1]
            if type(Content) == list:
                Content=str(Content)
                print (Content,"HAVE TO WORK ON THIS")

        elif ((listToStr.lower().__contains__('13')) and (listToStr.lower().__contains__('Action'))):
            FIRContentPresent = 1
            Content = listToStr.lower().split('13')[0]
        if(FIRContentPresent==1):
            FIRCompContent = FIRCompContent + Content



        return FIRDf,FIRCompContent


#FileNamesinList is a function used to store the names of png and jpg files at a specified path
    def FileNamesinList(files):

        ImgFiles = []
        ImageFileSplitted=[]
        arr = os.listdir()
        for i in arr:
            if '.txt' in i:
                files.append(i)

            if '.jpg' in i.lower() or '.png' in i.lower():
                if i.__contains__('_'):
                    ImageFileSplitted.append(i.split('_')[0])
                ImgFiles.append(i)

        return files, ImgFiles, ImageFileSplitted


# removeStopWords is a function built to remove punjabi stop words from dataframe
    def removeStopWords(dataFrame):

        for index,document in enumerate(dataFrame):

            document=str(document).split(' ')
            DocWithoutStopwrds = [word for word in document if not word in STOPS_LIST]

            dataFrame[index]=DocWithoutStopwrds

        return dataFrame


    def stopwords_manual_list(data):

        f2 = open("/home/nitpreet/Documents/Sabudh Projects/stopwords_pun_updated.txt", "r")
        stopwords = [x.strip() for x in f2.readlines()]

        data["cl"] = data["First_Information_Contents"].apply(
            lambda x: str(x).replace("।", ""))  # for replacing the | from the text
        data["cl"] = data["cl"].apply(
            lambda x: str(x).replace("#$%-/", ""))  # for replacing the special chrs from the dataframe
        data["cl"] = data["cl"].apply(lambda x: " ".join([word for word in x.split(" ") if word not in stopwords and len(
            word) > 1]))  # for removing the stopwords and characters of 0 length
        data["token"] = data["cl"].apply(lambda x: tokenize(x, language_code='pa'))
        data["token"] = data["token"].apply(lambda x: [word.replace("▁", "") for word in x])
        # tokenizer is used to put extra "_" between words So as to remove this extra thing

        return data



class EmbeddingsUsingPunjabiToEnglishConversion:

    def readingDictionaryPages(self):

        os.chdir("/home/nitpreet/Documents/Sabudh Projects/Dictionary")  # moving to specific directory
        rootdir = '/home/nitpreet/Documents/Sabudh Projects/Dictionary'
        Datatext = []
        # for reading images

        with PyTessBaseAPI(path='/usr/share/tesseract-ocr/4.00/tessdata/', lang='Gurmukhi') as api:

            for subdir, dirs, files in os.walk(rootdir):
                # walking to specific directory and searching for files that ends with jpeg

                for file in files:

                    if file.lower().endswith(".jpeg"):

                        api.SetImageFile(file)
                        text = api.GetUTF8Text()  # extracting the text from the image
                        Datatext.append(text)

        datatext = pd.DataFrame({'Dict': Datatext})  # converting to dataframe

        datatext.to_csv('EnglishtoPunjabiDictDf.csv')  # converting to csv file

        return datatext

    def separatingEnglishPunjabiWords(datatext):

        pstr = []  # punjabi array where all the meaning of the single english word would be saved
        pun = []  # array for storing punjabi words
        en1 = []  # english arry for storing english words
        data = []


        datatext['Dict'] = datatext['Dict'].apply(lambda x: re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", " ", x))
        # for removing special symbols

        datatext['Dict'] = datatext['Dict'].apply(lambda x: re.sub(r"[0123456789%»\u200c*¢॥_’]", " ", x))
        # for removing numbers and some symbols

        datatext['Dict'] = datatext['Dict'].apply(lambda x: re.sub("\n", ' ', x))
        # for removing \n


        grammar = ['adv', 'adj', 'nn', 'v', 'pref', 'suf', 'a', 'n', 'v.t ', 'prep', 'pred']
        data.append(datatext['Dict'].apply(lambda x: [word for word in x.split(" ") if len(word) >= 1 and word not in grammar]))



        # main logic is that whenever a single english word is obtained then all the punjabi words would be belonging to previous english word
        for pages_dict in range(0, len(data[0])):

            for word in data[0][pages_dict]:

                if wordnet.synsets(word) and len(word) > 1:

                    if wordnet.synsets(data[0][pages_dict][data[0][pages_dict].index(word) - 1]) and len(data[0][pages_dict][data[0][pages_dict].index(word) - 1]) > 1:

                        Engword = str(word) + ' ' + str(data[0][pages_dict][data[0][pages_dict].index(word) - 1])
                        en1.append(Engword)
                        pun.append(pstr)
                        pstr = []

                    else:

                        pun.append(pstr)
                        pstr = []
                        en1.append(word)

                else:

                    pstr.append(word)

        DictDF = pd.DataFrame()
        DictDF['English'] = en1
        DictDF['Punjabi'] = pun

        # converting to csv
        DictDF.to_csv("eng_pun_dict_words.csv")

        return en1, pun

#This function is used to create embeddings of words after perrforming Punjabi to English conversion with the use of dictionaries
    def WordEmbeddings(VocabWordsWithoutStopwrds):

        Embeddings=[]

        for each_doc in VocabWordsWithoutStopwrds:
            VectEmbeddings = get_embedding_vectors(str(each_doc), 'pa')
            Embeddings.append(VectEmbeddings)

        return Embeddings



# This function was created to form a solution for creating embeddings by replacing words using english to Punjabi dictionaries
    def ReplacingWordswithDict(DictDataframe,FIRDf_WithoutStopwords):

        FIRSummary=FIRDf_WithoutStopwords['First_Information_Contents']
        count=0

        for FIRContentIndex in range(0,len(FIRSummary)):

            eachSummary=FIRSummary[FIRContentIndex]
            Words=eachSummary.split(', ')

            for word in Words:

                word.replace("'","")

                for eachrowIndex in range(0,len(DictDataframe['Punjabi'])):

                    if word in DictDataframe['Punjabi'][eachrowIndex]:

                        count=count+1
                        eachSummary.replace(word,DictDataframe['English'][eachrowIndex])

            FIRSummary[FIRContentIndex]=eachSummary

        return FIRSummary



class UnderstandingSemanticsUsingEmbeddings:


# ComputeTF_IDF is a functtion built to create sparse matrix of occurences
    def ComputeTF_IDF(FIRSummary):

        tf = TfidfVectorizer()
        TFVector = tf.fit_transform(FIRSummary)
        VocabWords= tf.vocabulary_.keys()

        return TFVector,VocabWords


#This function is created to load the fasttext vector model for embeddings
    def load_vectors(fname):

        fin = io.open(fname, 'r', encoding='utf-8', newline='\n', errors='ignore')
        n, d = map(int, fin.readline().split())
        data = {}

        for line in fin:

            tokens = line.rstrip().split(' ')
            data[tokens[0]] = map(float, tokens[1:])

        return data


# This functions is made for creating embeddings of Punjabi words using Fasttext model
    def Embeddings(FTVocabWords,TF_IDF_VocabWords,model):

        Embedngs=[]

        for each_word in TF_IDF_VocabWords:

            if each_word in FTVocabWords:

                Emb=model.get_word_vector(each_word)
                Embedngs.append(Emb)

        return Embedngs



files = []
FTVocabWords=[]
os.chdir(r'D:\Workspace\PycharmProjects\Sabudh\MachineLearning\ProjectWork\data\Feb')
FIRdata = pd.read_csv("/home/nitpreet/Documents/Sabudh Projects/Fir/FIRDf.csv")
#rootdir = '/home/nitpreet/Documents/Fir/FIR/FEB-2019/'

FIRDf = pd.DataFrame(columns=['First_Information_Contents','Date_and_Location','FIR_Location','FIR_Date','PDF_Name'])

Preprocessing.pdftoimage()

files,ImgFiles,ImageFileSplitted=Preprocessing.FileNamesinList(files)

FIRDf=Preprocessing.Image2Text(ImgFiles,ImageFileSplitted,FIRDf)
FIRDf.to_csv(r'FIRDf.csv')
Df=pd.read_csv('FIRDf.csv')
Df['First_Information_Contents']=Preprocessing.removeStopWords(Df['First_Information_Contents'])

# check the data['cl'] for cleaned portion and data['token'] for tokenized text
Df = Preprocessing.stopwords_manual_list(Df)

Df.to_csv(r'FIRDf_WithoutStopwords.csv')
FIRDf_WithoutStopwords = pd.read_csv('FIRDf_WithoutStopwords.csv')

#Approach 1 of using English to Punjabi dictionary for getting embeddings of words after replacing punjabi words with english words

datatext=EmbeddingsUsingPunjabiToEnglishConversion.readingDictionaryPages()
en1,pun = EmbeddingsUsingPunjabiToEnglishConversion.separatingEnglishPunjabiWords(datatext)
DictDataframe=pd.read_csv('eng_pun_dict_words.csv')

FIRSummaries=EmbeddingsUsingPunjabiToEnglishConversion.WordEmbeddings()
TFVector,TF_IDF_VocabWords = UnderstandingSemanticsUsingEmbeddings.ComputeTF_IDF(FIRDf_WithoutStopwords['First_Information_Contents'])

FIRDf_WithoutStopwords=EmbeddingsUsingPunjabiToEnglishConversion.ReplacingWordswithDict(DictDataframe,FIRDf_WithoutStopwords)


#Approach 2 of using fasttext model for getting embeddings of Punjabi FIR reports

#Loading fasttext punjabi model vector
data = UnderstandingSemanticsUsingEmbeddings.load_vectors("cc.pa.300.vec")
FTVocabWords = data.keys()

#Loading fasttext punjabi model binary file
model = fasttext.load_model("cc.pa.300.bin")
FIRSummary=pd.DataFrame(FIRDf_WithoutStopwords['First_Information_Contents'])
TFVector,VocabWords=UnderstandingSemanticsUsingEmbeddings.ComputeTF_IDF(FIRSummary)
Embedngs = UnderstandingSemanticsUsingEmbeddings.Embeddings(FTVocabWords,TF_IDF_VocabWords,model)






