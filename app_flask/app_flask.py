#imports
from flask import Flask, render_template, request

app = Flask(__name__)


import nltk
import numpy as np
import re

#import du texte
texte = open('infos_corona.txt',  mode = 'r', encoding='utf-8')
texte = texte.read()


# tokenization -> Création d'une liste de phrases
# nltk.download('punkt') # first-time use only
# nltk.download('wordnet') # first-time use only (pour l'anglais)
phrases_token = nltk.sent_tokenize(texte)

for i in reversed(range(len(phrases_token))) :
    if phrases_token[i][-1] == '?':
        del phrases_token[i]
        
# on enlève les doublons
phrases_token = list(set(phrases_token)) 

# nettoyage
def nettoyage(phrases_token):
    phrases_token = phrases_token.lower()
    phrases_token = phrases_token.replace('n.c.a.', 'non-consommateur absolu')
    phrases_token = phrases_token.replace('covid-19', 'coronavirus')
    phrases_token = re.sub('[éèê]', 'e', phrases_token)
    phrases_token = re.sub('[àâ]', 'a', phrases_token)
    phrases_token = re.sub('[ô]', 'o', phrases_token)
    phrases_token = re.sub('\n', ' ', phrases_token)
    phrases_token = re.sub('A\/ ', '', phrases_token)
    phrases_token = re.sub('B\/ ', '', phrases_token)
    phrases_token = re.sub('C\/ ', '', phrases_token)
    phrases_token = re.sub('a\/ ', '', phrases_token)
    phrases_token = re.sub('b\/ ', '', phrases_token)
    phrases_token = re.sub('c\/ ', '', phrases_token)
    phrases_token = re.sub('d\/ ', '', phrases_token)
    return phrases_token
 
# on applique la fonciton de nettoyage
phrases_token_propres = []
for i in range(len(phrases_token)):
    phrases_token_propres.append(nettoyage(phrases_token[i]))
  
# Entraînement d'une matrice TF-IDF
from stop_words import get_stop_words
stop_words = get_stop_words('french')

from sklearn.feature_extraction.text import TfidfVectorizer
TfidfVec = TfidfVectorizer(stop_words = stop_words)
tfidf = TfidfVec.fit(phrases_token)

# on crée la matrice TF-IDF sur le texte de la page wiki
phrases_tf = tfidf.transform(phrases_token)
    
# la phrase la plus proche de celle posée par l'utilisateur
from sklearn.metrics.pairwise import cosine_similarity

def reponse_wiki(phrase_user):
    # on a besoin de passer la chaîne de caractère dans une liste :
    phrase_user = [phrase_user]
    
    
    # On calcule les valuers TF-IDF pour la phrase de l'utilisateur
    user_tf = tfidf.transform(phrase_user)
    # on calcule la similarité entre la question posée par l'utilisateur
    # et l'ensemble des phrases de la page wiki
    similarity = cosine_similarity(user_tf, phrases_tf).flatten()
    # on sort l'index de la phrase étant la plus similaire
    index_max_sim = np.argmax(similarity)
    # Si la similarité max ets égale à 0 == pas de correspondance trouvée
    if(similarity[index_max_sim] == 0):
        robo_response = "Je ne trouve pas la réponse à cette question, désolé"
    # Sinon, on sort la phrase correspondant le plus : 
    else:
        robo_response = phrases_token[index_max_sim]
    return robo_response

bonjour = ('.onjour|.jr|.alut|.lt')
aurevoir = ('.[aà].?plus|.[aà].?bientot|.[aà].?bientôt|.u revoir')

#define app routes
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/get")
#function for the bot response
def get_bot_response():

    phrase_user = request.args.get('msg')
    phrase_user = phrase_user.lower()
    if (re.fullmatch(aurevoir,phrase_user)):
        return "Pensez à appliquer les gestes barrières! Et restez-chez-vous"
    
    elif (re.fullmatch(bonjour,phrase_user)):
        return 'Bonjour en quoi puis-je vous aider ?'
        
    else:
        return reponse_wiki(phrase_user)
    
if __name__ == "__main__":
    app.run()


# source pour ma structure flask https://codinginfinite.com/chatbot-in-python-flask-tutorial/