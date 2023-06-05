# library data preprocessing
import string as s
import os
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
nltk.download('wordnet')
# !pip install Sastrawi
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
# library membaca model
import pickle
import pandas as pd

def preprocessing(text):
  # lowercase
  text = text.lower()
  # remove punctuation and numbers
  TANDA_BACA = s.punctuation
  ANGKA = s.digits
  text = text.translate(str.maketrans('', '', TANDA_BACA)).translate(str.maketrans('', '', ANGKA))
  # remove stopwords
  from nltk.corpus import stopwords
  STOPWORDS = set(stopwords.words('indonesian'))
  text = " ".join([word for word in str(text).split() if word not in STOPWORDS])
  # stemming
  Fact = StemmerFactory()
  Stemmer = Fact.create_stemmer()
  text = Stemmer.stem(text)
  return text

# Kemiskinan
kemiskinan_model = pickle.load(open(os.getcwd() + '\\dashboard\\scraper\\model\\kemiskinan.pkl', 'rb'))
def classify_kemiskinan(text):
  t = preprocessing(text)
  s = pd.Series(t)
  hasil = kemiskinan_model.predict(s)
  return hasil[0]

# Pengangguran
pengangguran_model = pickle.load(open(os.getcwd() + '\\dashboard\\scraper\\model\\pengangguran.pkl', 'rb'))
def classify_pengangguran(text):
  t = preprocessing(text)
  s = pd.Series(t)
  hasil = pengangguran_model.predict(s)
  return hasil[0]

# Demokrasi
demokrasi_model = pickle.load(open(os.getcwd() + '\\dashboard\\scraper\\model\\demokrasi.pkl', 'rb'))
def classify_demokrasi(text):
  t = preprocessing(text)
  s = pd.Series(t)
  hasil = demokrasi_model.predict(s)
  return hasil[0]

# Inflasi
inflasi_model = pickle.load(open(os.getcwd() + '\\dashboard\\scraper\\model\\inflasi.pkl', 'rb'))
def classify_inflasi(text):
  t = preprocessing(text)
  s = pd.Series(t)
  hasil = inflasi_model.predict(s)
  return hasil[0]

# Pertumbuhan Ekonomi
ekonomi_model = pickle.load(open(os.getcwd() + '\\dashboard\\scraper\\model\\ekonomi.pkl', 'rb'))
def classify_ekonomi(text):
  t = preprocessing(text)
  s = pd.Series(t)
  hasil = ekonomi_model.predict(s)
  return hasil[0]