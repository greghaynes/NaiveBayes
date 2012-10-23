import math
import classifier

class CategoryInfo(object):

    def __init__(self):
        self.word_counts = {}
        self.total_word_count = 0
        self.document_count = 0

    def handle_document(self, document):
        '''A document is a list of words'''
        for word in document:
            self.handle_word(word)
        self.document_count += 1

    def handle_word(self, word):
        word_count = self.word_counts.get(word, 0)
        self.word_counts[word] = word_count + 1
        self.total_word_count += 1

class ImprovedNB(classifier.Classifier):
    '''
    An improved version of the naive bayes filter

    This version features +1 smoothing to avoid overfitting and evidence
    addition using the logarithm of bayes rule to avoid floating point
    underflow.
    '''

    def __init__(self,
                 multinominal=False,
                 language='english',
                 common_words_path='data/commonwords.txt'):
        '''
        Initialize the imrpoved naive bayes classifier

        If multinominal is true then documents are classified by the count of
        each unique word per document. Otherwise documents are classified using
        a bernoulli model describing the occurence of a unique work in the
        document.
        '''
        super(ImprovedNB, self).__init__(language, common_words_path)
        self.multinominal = multinominal
        self.categories = {}
        self.document_count = 0
        self.words_seen = {}

    def useful_words(self, text):
        if self.multinominal:
            all_words = text.replace('\n', ' ').split(' ')
            usefuls = []
            for word in all_words:
                if word  in self.common_words:
                    continue
                usefuls.append(self.word_stemmer.stemWord(word))
            return usefuls
        return super(ImprovedNB, self).useful_words(text)

    def text_category_probability(self, category, text):
        '''
        Probability of text being in specified category is calculated by:
        
        e^(ln P(c) + sum of (ln P(T_k|c)) for all k - ln P(d))
        where:
            P(c) is the probability of the class

            P(T_k|c) is the probability of k'th element of text being in class

            P(d) is the probability of the document

        By taking a logarithm of Bayes rule we are able to avoid floating point
        underflow.

        We also use a non-standard method to calculate P(T_k|c) in order to
        avoid overfitting (otherwise 0 values for a T_k will drive the whole
        solution to 0:
            P(T_k|c) = number of times T_k has appeared in class C docs + 1 /
                       number of words in class C docs + | Vocabulary |
        '''
        try:
            cat_info = self.categories[category]
        except KeyError:
            return -1
        p_c = math.log(float(cat_info.document_count) / self.document_count)

        useful_words = self.useful_words(text)
        seen_words = {}
        p_t_c = 0
        for word in useful_words:
            if word in seen_words:
                continue
            seen_words[word] = True
            word_cnt = float(cat_info.word_counts.get(word, 0))
            class_words_cnt = float(cat_info.total_word_count)

            # +1 is used to prevent overfitting
            p_tk_c = (word_cnt + 1)
            if self.multinominal:
                p_tk_c /= float(class_words_cnt + len(self.words_seen))
            else:
                p_tk_c /= float(class_words_cnt + 2)
            p_t_c += math.log(p_tk_c)

        p_d = math.log(1 / float(self.document_count))

        return math.exp(p_c + p_t_c - p_d)
 
    def train(self, category, text):
        cat_info = self.categories.get(category, CategoryInfo())
        useful_words = self.useful_words(text)
        for word in useful_words:
            self.words_seen[word] = True
        cat_info.handle_document(useful_words)
        self.categories[category] = cat_info
        self.document_count += 1

