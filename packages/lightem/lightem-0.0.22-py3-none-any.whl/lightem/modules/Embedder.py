from gensim.models import KeyedVectors
from sentence_transformers import SentenceTransformer
# import nltk
import numpy as np
# from nltk.corpus import stopwords
from typing import *
from modules.args import Args


EmbedderTypes = Literal['glove', 'sentence-transformers']

class Embedder():
  '''Classe responsável por calcular embeddings de uma sentença. Alguns embedders são aceitos, sendo eles:
  - sentence-transformers: Mais lento mas com embeddings de melhor qualidade
  - glove: Mais rápido mas com embeddings de qualidade inferior'''
  
  def __init__(self, embedderType: EmbedderTypes):
    # nltk.download('stopwords')
    # self.stopwords = set(stopwords.words(Args.language))
    self.embedderType = embedderType
    match embedderType:
      case 'glove':
        self.embedder = KeyedVectors.load_word2vec_format("models/bin/glove.6B.300d.bin", binary=True)
      case 'sentence-transformers':
        self.embedder = SentenceTransformer('sentence-transformers/all-MiniLM-L12-v2')
      
  
  def __preprocessSentence(self, sentence: str, removeStopwords) -> str:
    '''Remove stopwords, caracteres da sentença e deixa tudo em minúsculo.'''
    if removeStopwords:
      words = sentence.split()
      # words = [word for word in words if word not in self.stopwords]
      sentence = " ".join(words)
    specialChars = ['.', ',', '!', '?', ';', ':', '(', ')', '[', ']', '{', '}', '"', "'"]
    for char in specialChars:
      sentence = sentence.replace(char, ' ')
    
    return sentence.lower()

  def preprocess(self, sentence, removeStopwords=False):
    return self.__preprocessSentence(sentence, removeStopwords)
  
  def getEmbeddings(self, sentence: str, removeStopwords: bool = False) -> np.ndarray:
    '''Calcula o embedding de uma única sentença. Se removeStopwords for True, as stopwords são removidas da sentença.
    É calculado o embedding de cada palavra e, para retornar um embedding único, é feita a média dos embeddings.
    OBS.: Verificar se retornar a média é a melhor forma de retornar um embedding único. Pensar em como dar destaque para
    palavras mais importantes.'''
    # print(f"Calculating embeddings for sentence: {sentence}")
    sentence = self.__preprocessSentence(sentence, removeStopwords)
    # print(f"Preprocessed sentence: {sentence}")
    match self.embedderType:
      case 'glove':
        return self.__getEmbeddingsGlove(sentence)
      case 'sentence-transformers':
        return self.__getEmbeddingsSentenceTransformers(sentence)

  def __getEmbeddingsSentenceTransformers(self, sentence) -> np.ndarray:
    '''Retorna os embeddings de uma sentença utilizando o modelo de Sentence-Transformers all-MiniLM-L12-v2. Mais robusto e com melhores resultados, mas mais lento.'''
    return self.embedder.encode(sentence)

  def __getEmbeddingsGlove(self, sentence) -> List[np.ndarray]:
    '''Retorna os embeddings de uma sentença utilizando o modelo Glove. Se uma palavra não estiver no vocabulário, ela é ignorada.'''
    words = sentence.split()
    embeddings = [self.embedder[word] for word in words if word in self.embedder.key_to_index]
    if not embeddings:
      return np.zeros(self.embedder.vector_size)
    return np.mean(embeddings, axis=0)  # Otimizar a função de agrupamento de embeddings, média seria o suficiente/certo?
  