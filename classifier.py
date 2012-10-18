import Stemmer

class Classifier(object):
    
    def __init__(self,
                 language='english',
                 common_words_path='data/commonwords.txt'):
        self.language = language
        self.common_words_path=common_words_path

    @property
    def word_stemmer(self):
        try:
            return self._word_stemmer
        except AttributeError:
            self._word_stemmer = Stemmer.Stemmer(self.language)
            return self._word_stemmer

    @property
    def common_words(self):
        try:
            return self._common_words
        except AttributeError:
            self._common_words = {}
            with open(self.common_words_path) as f:
                for line in f:
                    if not line.startswith('#'):
                        stemmed_word = self.word_stemmer.stemWord(line[:-1])
                        self._common_words[stemmed_word] = True
            return self._common_words

    def useful_words(self, text):
        '''Grab a list of unique words where each word is not a common word'''
        text.replace('\n', ' ')
        all_words = text.split(' ')
        useful_words_dict = {}
        for word in all_words:
            if len(word) > 0 and word not in self.common_words:
                useful_words_dict[self.word_stemmer.stemWord(word)] = True
        return useful_words_dict.keys()

    def classify(self, text):
        return None

