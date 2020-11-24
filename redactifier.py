import nltk
from nltk.tag.stanford import StanfordNERTagger
from nltk.tag import SennaNERTagger
    
#from nltk.parse import CoreNLPParser
#nltk.download('punkt')

import progressbar

def redactAllNames(inputString, exceptFor = ""):
    #classifier = 'stanfordNER/english.all.3class.distsim.crf.ser.gz'
    #nerJavaJar = 'stanfordNER/stanford-ner.jar'
    #st = StanfordNERTagger(classifier, nerJavaJar)
    #tagger = CoreNLPParser(url='http://localhost:9000', tagtype='ner')
    tagger = SennaNERTagger('senna')
    
    result = ""
    redactedNames = []
    
    print("Splitting into sentences...")
    sentences = nltk.sent_tokenize(inputString)
    
    bar = progressbar.ProgressBar(maxval=len(sentences), \
        widgets=['Processing sentences (', progressbar.SimpleProgress(), ')... ', progressbar.Bar('=', '[', ']'), ' ', progressbar.AdaptiveETA()])
    count = 0
    
    bar.start()
    for sentence in sentences:
        bar.update(count)
        count = count + 1
        
        tokens = nltk.tokenize.word_tokenize(sentence)
        
        if len(tokens) >= 1024:
            print("Sentence contains {} tokens - Senna can only handle 1024. Panic!")
        
        PERSON_TAG = 'B-PER'
        
        NE = ""
        prev_tag = "O"
        for token, tag in tagger.tag(tokens):
            if tag == "O":
                if prev_tag == PERSON_TAG:
                    redactedNames.append(NE)
                    sentence = sentence.replace(NE, "[REDACTED]")
                prev_tag = tag
                NE = ""
                continue
    
            if tag != "O" and prev_tag == "O": # Begin named entity
                NE = token
            elif prev_tag != "O" and prev_tag == tag: # Inside named entity
                NE = NE + " " + token
            elif prev_tag != "O" and prev_tag != tag: # Adjacent named entity
                if prev_tag == PERSON_TAG:
                    redactedNames.append(NE)
                    sentence = sentence.replace(NE, "[REDACTED]")
                NE = token
            prev_tag = tag
        
        if prev_tag == PERSON_TAG: # catch if last tag was a person tag
            redactedNames.append(NE)
            sentence = sentence.replace(NE, "[REDACTED]")
            
        result = result + sentence + " "
    bar.finish()
    
    for name in redactedNames:
        result = result.replace(name, "[REDACTED]")
    
    return result, redactedNames
