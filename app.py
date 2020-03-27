# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 09:03:27 2020

@author: Pierre

Corobot
"""
# import des librairies
import nltk
import numpy as np
import random
import string # to process standard python strings
import re

#import du texte
texte = open('infos_corona.txt',  mode = 'r', encoding='utf-8')
texte = texte.read()

# nettoyage
def nettoyage(texte):
    texte = texte.lower()
    texte = texte.replace('n.c.a.', 'non-consommateur absolu')
    texte = texte.replace('covid-19', 'coronavirus')
    texte = re.sub('\n', ' ', texte)
    texte = re.sub('A\/ ', '', texte)
    texte = re.sub('B\/ ', '', texte)
    texte = re.sub('C\/ ', '', texte)
    texte = re.sub('a\/ ', '', texte)
    texte = re.sub('b\/ ', '', texte)
    texte = re.sub('c\/ ', '', texte)
    texte = re.sub('d\/ ', '', texte)
    return texte
    
texte = nettoyage(texte)

# tokenization -> Création d'une liste de phrases
# nltk.download('punkt') # first-time use only
# nltk.download('wordnet') # first-time use only (pour l'anglais)
phrases_token = nltk.sent_tokenize(texte)


for i in reversed(range(len(phrases_token))) :
    if phrases_token[i][-1] == " ?":
        del phrases_token[i]

with open("test.txt", "w") as output:
    output.write(str(phrases_token))
    