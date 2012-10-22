import math
import classifier

class CategoryInfo(object):

    def __init__(self):
        self.word_counts = {}
        self.total_word_count = 0
        self.document_count = 0

    def handle_document(self, document):
        words = document.split(' ')
        for word in words:
            self.handle_word(word)
        self.document_count += 1

    def handle_word(self, word):
        word_count = self.word_counts.get(word, 0)
        self.word_counts[word] = word_count + 1
        self.total_word_count += 1

class ImprovedNB(classifier.Classifier):
    '''An improved version of the naive bayes filter'''

    def __init__(self,
                 language='english',
                 common_words_path='data/commonwords.txt'):
        super(ImprovedNB, self).__init__(language, common_words_path)
        self.categories = {}
        self.document_count = 0

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
                       number of words in class C docs + 1
        '''
        if category not in self.categories:
            return -1

        cat_info = self.categories[category]
        p_c = math.log(float(cat_info.document_count) / self.document_count)

        useful_words = self.useful_words(text)
        p_t_c = 0
        for word in useful_words:
            word_cnt = float(cat_info.word_counts.get(word, 0))
            class_words_cnt = float(cat_info.total_word_count)

            # +1 is used to prevent overfitting
            p_tk_c = (word_cnt + 1) / (class_words_cnt + 1)
            p_t_c += math.log(p_tk_c)

        p_d = math.log(1 / float(self.document_count))

        return p_c + p_t_c - p_d
 
    def train(self, category, text):
        cat_info = self.categories.get(categories, CategoryInfo())
        cat_info.handle_document(text)
        self.categories[category] = cat_info
        self.document_count += 1

