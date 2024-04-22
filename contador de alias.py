import nltk
nltk.download("words")
from nltk.corpus import words
listaAlias = words.words()
num=0
for item in listaAlias:
    num=num+1
    print(item)
print(num)
