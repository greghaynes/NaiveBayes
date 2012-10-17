import Stemmer

stemmy = Stemmer.Stemmer('english')

def getCommonwords(path='data/commonwords.txt'):
    '''So we dont classify common words'''
    words = {}
    with open(path) as f:
        for line in f:
            if not line.startswith('#'):
                stemmed_word = stemmy.stemWord(line[:-1])
                words[stemmed_word] = True
    return words

if __name__ == '__main__':
    print getCommonwords()

