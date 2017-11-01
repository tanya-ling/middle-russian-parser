# -*- coding: utf-8 -*-
import re

dictReplacements = {
                       'i': 'и',
                       'і': 'и',
                       'ї': 'и',
                       'ï': 'и',
                       'ꙇ': 'и',
                       'ѡ': 'о',
                       'є': 'e',
                       '́': '',
                       '҃': '',
                       'ѿ': 'от',
                       '꙽': '',
                       'ѵ': 'и',
                       '̂': '',
                       'ѻ': 'о',
                       'ѳ': 'ф',
                       'ѯ': 'кс',
                       'ѱ': 'пс',
                       'ѕ': 'з',
                       'ꙋ': 'у',
                       'ꙗ': 'я',
                       'ѧ': 'я',
                       'ѹ': 'у',
                    }
rxYer = re.compile('([цкнгшщзхфвпрлджчсмтб])(ь|ъ)([цкнгшщзхфвпрлджчсмтб])')
rxYu = re.compile('([уеыаоэяию])(у)')
rxYa = re.compile('([уеыаоэяию])(а)')
rxYe = re.compile('([уеыаоэяию])(э)')
rxEndCons = re.compile('[кнгзхфвпрлдсмтб]$')


def sochet(word):
    word = word.lower()
    word2 = word.replace('оу', 'у')
    word2 = word2.replace('жы', 'жи')
    word2 = word2.replace('шы', 'ши')
    word2 = word2.replace('щы', 'щи')
    word2 = word2.replace('чы', 'чи')
    word2 = word2.replace('жю', 'жу')
    word2 = word2.replace('шю', 'шу')
    word2 = word2.replace('щю', 'щу')
    word2 = word2.replace('чю', 'чу')
    word2 = word2.replace('сч', 'щ')
    word2 = word2.replace('жч', 'щ')
    word2 = word2.replace('дч', 'дш')
    word2 = word2.replace('дщ', 'дш')
    word2 = rxYu.sub('\\1ю', word2)
    word2 = rxYa.sub('\\1я', word2)
    word2 = rxYe.sub('\\1е', word2)
    word2 = word2.replace('тс', 'ц') 
    word2 = word2.replace('тц', 'ц')
    word2 = word2.replace('щъ', 'щь')
    return word2


def letterchange(word):
    newword = ''
    for c in word:
        try:
            newword += dictReplacements[c]
        except KeyError:
            newword += c
    return newword


def inter_new(word):
    newword = rxYer.sub('\\1\\3', word)
    return newword


def normalize_word(word):
    word = letterchange(word)
    word = inter_new(word)
    word = inter_new(word)
    word = sochet(word)
    word = begend_new(word)
    return word


def begend_new(word):
    if rxEndCons.search(word) is not None:
        word += 'ъ'
    return word

print(normalize_word('здравствуи'))