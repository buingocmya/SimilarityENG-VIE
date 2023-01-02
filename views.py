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
from googletrans import Translator

def test(request):
    #next = request.GET('next','')
    eng =  request.POST.get('engsenten')
    viet =  request.POST.get('vietsenten')
    submit = request.POST.get('submit')

    viet=trans(viet)

    englist = preprocessing(eng)
    vietlist= preprocessing(viet)
    
    result = simiS(englist,vietlist)

    context= {'engsenten': preprocessing(eng), 'vietsenten': preprocessing(viet), 'submit': submit, 'result': result}
    return render(request, 'home.html', context )

def get_home(request):
    return render(request,'home.html')

def trans(text):
    translate = Translator()
    result = translate.translate(text)
    return result.text

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

def wup_simi(text1, text2):
    #print(text1 + ' ' + text2)
    if (text1 == text2):
        return 1.0;
    w1 = wn.synsets(text1)
    #w1.lowest_common_hypernyms(w1, use_min_depth=True)
    w2 = wn.synsets(text2)
    maxScore = 0
    for synset1 in w1:
        for synset2 in w2:
            currScore = wn.wup_similarity(synset1, synset2)
            if currScore > maxScore:
                maxScore = currScore
    #print(text1 + ' ' + text2+ ' ', maxScore)
    return maxScore

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
def simS(t1,t2):
    return 0

def simR(t1,t2):
    return 0

def show_result(reponse):
    return 1


#1. cd mysite
#2. python manage.py migrate
#3. python manage.py runserver 8888
"""
