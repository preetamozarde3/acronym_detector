
#!/usr/bin/env python
# coding: utf-8

"""
File to detect acronyms in text
"""

import spacy
import string
from nltk.corpus import words

from collections import Counter

from spacy.tokenizer import Tokenizer
from spacy.lang.en import English
nlp = English()
tokenizer = Tokenizer(nlp.vocab)

sentences = ["His bank acc. bal < 7000$.", 
             "This subject is impt", 
             "the age of this person is approx 35 yrs.", 
             "The current amt after the txn is 5000 rs"]

acronyms_dict1 = {'approx': 'Approximately',
'b/c': 'Because',
'bal': 'balance',
'def': 'Definition',
'diff': 'difference',
'e.g': 'example',
'impt': 'Important',
'w/': 'With',
'w/o': 'Without',
'viz': 'Namely',
'ppl': 'People',
'natl': 'National',
'eqn': 'Equation',
'ed': 'Education',
'dep': 'Department',
'esp': 'Especially',
'lrg': 'Large',
'Stats': 'Statistics',
'Amt': 'Amount',
'Amts': 'Amounts',
'subj': 'Subject',
'sub': 'Subject',
'Ltd': 'Limited',
'max': 'Maximum',
'min': 'Minimum',
'Eng': 'English',
'Ans': 'Answer',
'acc': 'account',
'app': 'Application',
'esp': 'Especially',
'est': 'estimate',
'ex': 'exchange',
'gen': 'general',
'govt': 'Government',
'info': 'Information',
'lang': 'Language',
'orig': 'Original',
'para': 'Paragraph',
'pt': 'point',
'pts': 'points',
'ref': 'Refer',
'sect': 'Section',
'sp': 'Special',
'txn': 'transaction',
'txns': 'transactions',
'yr': 'Year',
'Dpt': 'Department',
'Gov': 'Government',
'Mgmt': 'Management',
'Pol': 'Politics',
'Capt': 'Captain',
'Col': 'Colonel',
'Dr': 'Doctor',
'Gen': 'General',
'Lt': 'Lieutenant',
'Mr': 'Mister',
'Prof': 'Professor',
'St': 'Saint',
'Sgt': 'Sergeant',
'Sr': 'Senior',
'jr': 'Junior',
'Wt': 'Weight',
'fx': 'foreign exchange',
'rs': 'rupees',
'usd': 'united states dollars',
'yrs': 'years'}


acronyms_dict2 = {'asap': 'As soon as possible',
'Wrt': 'With respect to',
'aka': 'Also known as', 
'loc': 'letter of credit',
'fx': 'foreign exchange',
'MD': 'Medical Doctor',
'VP': 'Vice President',
'CMO': 'Chief Marketing Officer',
'CFO': 'Chief Financial Officer',
'CEO': 'Chief Executive Officer',
'PA': 'Personal Assistant',
'SMS': 'Short Message Service',
'ASCII': 'American Standard Code for Information Interchange'}

acronym_list = []
for key in acronyms_dict1:
    acronym_list.append(acronyms_dict1[key].lower())
acronym_list.sort()

acronym_list2 = []
for key in acronyms_dict2:
    acronym_list2.append(acronyms_dict2[key].lower())
acronym_list2.sort()

def acronym(current_word):
    multi_list = []
    words_removed = [] 
    for acronym in acronym_list2:
        words = tokenizer(acronym)
        if current_word[0] == acronym[0] and len(current_word) == len(words):
            multi_list.append(acronym)
    if multi_list:
        for current in range(0, len(current_word)):
            for item in multi_list:
                words = tokenizer(item)
                if str(words[current])[0] != current_word[current]:
                    words_removed.append(item)

    if words_removed:
        for item in words_removed:
            if item in multi_list:
                multi_list.remove(item)
    if len(multi_list) == 1:
        return multi_list
    else:
        return []

def slang(current_word):
    newlist = []
    newlist[:0] = current_word
    counter = 0
    temp_list = []
    removed_words = []
    for acronym in acronym_list:
        if acronym[0] == newlist[0]:
            temp_list.append([acronym, 0, 0, 1])
        elif acronym[0] > newlist[0]:
            break

    if temp_list:
        count_word = 0
        for letter_1 in newlist:
            for item in temp_list:
                if count_word == item[2] + 1:
                    flag = False
                    acronym = item[0]
                    counter = item[1]
                    count_letter = 0
                    for letter_2 in acronym:
                        if count_letter > counter:
                            if letter_1 == letter_2:
                                flag = True
                                item[3] += 1
                                item[1] = count_letter
                                counter = count_letter
                                item[2] = count_word
                                break
                        count_letter += 1
                    if flag == False:
                        removed_words.append(item)
            count_word += 1

    for item in removed_words:
        temp_list.remove(item)
    if temp_list:
        return min(temp_list, key=cmp_key)
    elif removed_words:
        removed_words = words_considered(removed_words, current_word)
        return min(removed_words, key=cmp_key)
    else:
        return []

def check_word(word_to_be_checked):
    if acronym(word_to_be_checked):
        return acronym(word_to_be_checked)[0]
    elif slang(word_to_be_checked):
        return slang(word_to_be_checked)[0]
    else:
        return word_to_be_checked

def common(str1,str2):
    dict1 = Counter(str1)  
    dict2 = Counter(str2)  
 
    commonDict = dict1 & dict2  
  
    if len(commonDict) == 0:  
        print (-1) 
        return

    commonChars = list(commonDict.elements())  

    commonChars = sorted(commonChars)  

    return len(commonChars)

def words_considered(remaining_words, acronym_considered):
    for item in remaining_words:
        item[3] = common(item[0], acronym_considered)
    return remaining_words

def cmp_key(e):
    return e[1]

def acronym_detector(sentences):
    """
    Input parameter: list of sentences
    
    Output parameter: list of modified sentences
    """
    new_sentences = []
    for sent in sentences:
        sentence_words = tokenizer(sent)
        new_sent = ''
        for word in sentence_words:
            word = str(word).lower()
            if word.find('.') != -1:
                word = word.translate(str.maketrans('', '', string.punctuation))
            if word not in words.words() and word.isalpha():
                acronym_checked = check_word(word)
                new_sent = new_sent + acronym_checked + ' '
            else:
                new_sent = new_sent + word + ' '
        new_sentences.append(new_sent)
    return new_sentences