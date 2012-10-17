import Stemmer

stemmy = Stemmer.Stemmer('english')

def getCommonWords(path='data/commonwords.txt'):
    '''So we dont classify common words'''
    words = {}
    with open(path) as f:
        for line in f:
            if not line.startswith('#'):
                stemmed_word = stemmy.stemWord(line[:-1])
                words[stemmed_word] = True
    return words

common_words = getCommonWords()

def getUsefulWords(text):
    '''Grab a list of unique words where each word is not a common word'''
    text.replace('\n', ' ')
    all_words = text.split(' ')
    useful_words_dict = {}
    for word in all_words:
        if len(word) > 0 and word not in common_words:
            useful_words_dict[stemmy.stemWord(word)] = True
    return useful_words_dict.keys()

if __name__ == '__main__':
    print getUsefulWords('This is a very neat piece of text')
