from django.shortcuts import render
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from scipy import spatial
import requests
import math
from googletrans import Translator


def wup_simi(text1, text2):
    if (text1 == text2):
        return 1.0;
    w1 = wn.synsets(text1)
    w2 = wn.synsets(text2)
    maxScore = 0
    for synset1 in w1:
        for synset2 in w2:
            currScore = wn.wup_similarity(synset1, synset2)
            if currScore > maxScore:
                maxScore = currScore
    #print(text1 + ' ' + text2+ ' ', maxScore)
    return maxScore

def simiS(text1, text2):
    listtext = text1 + text2
    print("list text: ", listtext)
    vector1 = []
    for w in listtext:
        max = 0
        for w1 in text1:
            tmp = wup_simi(w,w1)
            if tmp>max:
                max = tmp 
        vector1.append(max);
    print('vector1 =', vector1)
    
    vector2 = []
    for w in listtext:
        max = 0
        for w2 in text2:
            tmp = wup_simi(w,w2)
            if tmp>max:
                max = tmp 
        vector2.append(max);
    print('vector2 =', vector2)
    result = 1 - spatial.distance.cosine(vector1, vector2)
    print (result)
    return result

def simiR(text1, text2):
    pi = 0.8
    listtext = text1 + text2
    vector1 = []
    for i in range(len(listtext)):
        max = 0
        index = 0
        for w1 in text1:
            tmp = wup_simi(listtext[i],w1)
            if (tmp>max and tmp>pi):
                max = tmp
                index = i 
        vector1.append(index);
    print('vector1 =', vector1)
    
    vector2 = []
    for i in range(len(listtext)):
        max = 0
        index = 0
        for w2 in text2:
            tmp = wup_simi(listtext[i],w2)
            if (tmp>max and tmp>pi):
                max = tmp 
                index = i
        vector2.append(index);
    print('vector2 =', vector2)
    a=0
    b=0
    for i in range (0,len(listtext)):
        a=a+(vector1[i]-vector2[i])*(vector1[i]-vector2[i])
        b=b+(vector1[i]+vector2[i])*(vector1[i]+vector2[i])
    result= 1 - math.sqrt(a)/math.sqrt(b)
    print (result)
    return result


def test(request):
    #next = request.GET('next','')
    eng =  request.POST.get('engsenten')
    viet =  request.POST.get('vietsenten')
    submit = request.POST.get('submit')

    viet=trans(viet)

    englist = preprocessing(eng)
    vietlist= preprocessing(viet)
    
    result = 0.5 * simiS(englist,vietlist) + 0.5 * simiR(englist,vietlist) 
    result = round(result *100,2)
    context= {'engsenten': preprocessing(eng), 'vietsenten': preprocessing(viet), 'submit': submit, 'result': result}
    print ("result: ",result)
    return render(request, 'home.html', context )

def get_home(request):
    return render(request,'home.html')

def trans(text):
    translate = Translator()
    result = translate.translate(text)
    return result.text


def preprocessing(text):
    #bỏ in hoa
    text = text.lower()
    #bỏ dấu câu
    text = text.translate(str.maketrans('', '', string.punctuation))
    #bỏ stopword
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)
    filtered_sentence = []
    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)
    
    #bỏ đuôi V
    #wordnet_map = {"N":wordnet.NOUN, "V":wordnet.VERB, "J":wordnet.ADJ, "R":wordnet.ADV}
    lemmatizer = WordNetLemmatizer()
    lem_sentence=[]
    for word in filtered_sentence: # or filtered_sentence:
        lem_sentence.append(lemmatizer.lemmatize(word))
        #lem_sentence.append(" ")
    
    #gắn thẻ 
    """lotr_pos_tags = nltk.pos_tag(lem_sentence)
    #vẽ cây
    grammar = "NP: {<DT>?<JJ>*<NN>}"
    chunk_parser = nltk.RegexpParser(grammar)
    tree = chunk_parser.parse(lotr_pos_tags)    
    tree.draw()
    """
    #trả về từ gốc (eng)
    stem_sentence=[]
    for word in lem_sentence:
        stem_sentence.append(PorterStemmer().stem(word))
        #stem_sentence.append(" ")
    
    #pos_tagged_sentence = nltk.pos_tag(lem_sentence.split())
    #lem_sentence.append(" ".join([lemmatizer.lemmatize(word, wordnet_map.get(pos[0], wordnet.NOUN)) for word, pos in pos_tagged_sentence]))
    
    return stem_sentence;
    #return "".join(stem_sentence)
    #return "".join(lem_sentence)

"""


#1. cd mysite
#2. python manage.py migrate
#3. python manage.py runserver 8888
"""
