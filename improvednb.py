import classifier

class CategoryInfo(object):

    def __init__(self):
        self.word_counts = word_counts
        self.total_word_count = total_word_count
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
        pass
 
    def train(self, category, text):
        cat_info = self.categories.get(categories, CategoryInfo())
        cat_info.handle_document(text)
        self.categories[category] = cat_info

