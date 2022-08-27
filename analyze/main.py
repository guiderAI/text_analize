from nltk import word_tokenize
# st = ISRIStemmer()
# from nltk.stem.isri import ISRIStemmer
import json
from playsound import playsound
from os import getcwd,chdir
from pydub import AudioSegment
from pydub.playback import play

def function_sound():
    path_1 = getcwd()
    chdir("sounds")
    # playsound('output.mp3')
    song = AudioSegment.from_mp3('output.mp3')
    play(song)
    chdir(path_1)
with open('analyze/dictionary.json', encoding='utf-8') as fh:
    data = json.load(fh)
ignore_letters = ['!', '?', ',', '.']
Prepositions = ['الى', 'في', 'على', 'من', 'إلى']
#  length one prefixes
pre_1 = ['ل', 'ب', 'ف', 'س', 'و', 'ي', 'ت', 'ن', 'ا']
# length two prefixes
pre_2 = ['ال', 'لل']
#  length three prefixes
pre_3 = ['كال', 'بال', 'ولل', 'وال']
# ###################################################################################################################################################
# length one suffixes
suf_1 = ['ة', 'ه', 'ي', 'ك', 'ت', 'ا', 'ن']
#  length two suffixes
suf_2 = ['ون', 'ات', 'ان', 'ين', 'تن', 'كم', 'هن', 'نا', 'يا', 'ها', 'تم', 'كن', 'ني', 'وا', 'ما', 'هم']
#  length three suffixes
suf_3 = ['تمل', 'همل', 'تان', 'تين', 'كمل']
# ###################################################################################################################################################
pr_4_3 = {
    0: ['م'],
    1: ['ا'],
    2: ['ا', 'و', 'ي'],
    3: ['ة']
}
pr_5_3 = {
    0: ['ا', 'ت'],
    1: ['ا', 'ي', 'و'],
    2: ['ا', 'ت', 'م'],
}
# ###################################################################################################################################################
def pro_w(word):
    print(word)
    if (word[0]) in pr_4_3[0]:# مفعل
        word = word[1:]
    if word[1] in pr_4_3[1]: # فاعل
        word = word[0:1] + word[2:]
    if word[2] in pr_4_3[2]: # فعال - فعول - فعيل
        word = word[0:2] + word[3:]
    if len(word) > 3:
        if word[3] in pr_4_3[3]: # فعلة
            word = word[:-1]
        elif (word[3] in pr_5_3[1]) and word[0] == "م":
            # مفعول - مفعال - مفعيل
            word = word[1, 3] + word[4];
        elif (word[0] in pr_5_3[2]) and word[4] == "ة":
            # مفعلة - تفعلة - افعلة
            word = word[1, 4]
    return word
def pre32_and_suf32(word):
    if (len(word) >= 6):
        for pre3 in pre_3:
            if word.startswith(pre3):
                return word[3]
        for suf3 in suf_3:
            if word.endswith(suf3):
                return word[-3]
    if (len(word) >= 5):
        for pre2 in pre_2:
            if word.startswith(pre2):
                return word[2];
        for suf2 in suf_2:
            if word.endswith(suf2):
                return word[-2]
    return word
def find_stem(token):
    if token[0:2] == 'ال':
        token = token[2:]
    token_1 = pre32_and_suf32(token)
    token_2 = pro_w(token_1);
    return token_2

def print_stem(input):
    out = []
    words_separate = word_tokenize(input)
    words = [find_stem(word) for word in words_separate if word not in ignore_letters]
    for i, w in enumerate(words):
        if w in Prepositions:
            out.append(w + " حرف جر")
            out.append('line')
        else:
            out.append(words_separate[i] + ' => جذر الكلمة : ' + w)
            out.append('line')
            out.append(find_derivatives(w))
            out.append('line')
    return out

def find_derivatives(word):
    out = ''
    for intent in data["intents"]:
        if intent["الفعل"] == word:
            for key in intent:
                out += '، ' + key + " : " + intent[key] + ' '
    return out
def call(inp = 'default'):
    if inp == 'default':
        with open("analyze/input.txt", mode='r', encoding = 'utf-8') as f:
            inp = f.read()
    return print_stem(inp)
