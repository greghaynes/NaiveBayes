import classifier

class ImprovedNB(classifier.Classifier):
    '''An improved version of the naive bayes filter'''

    def __init__(self,
                 language='english',
                 common_words_path='data/commonwords.txt'):
        super(ImprovedNB, self).__init__(language, common_words_path)

    def text_category_probability(self, category, text):
        '''
        Probability of text being in specified category is calculated by:
        
        e^( ln P(c) + sum of (ln P(T_k|c)) for all k - ln P(d))
        where:
            P(c) is the probability of the class

            P(T_k|c) is the probability of k'th element of text being in class

            P(d) is the probability of the document

        By taking a logarithm of Bayes rule we are able to avoid floating point
        underflow.

        We also use a non-standard method to calculate P(T_k|c) in order to
        avoid overfitting (otherwise 0 values for a T_k will drive the whole
        solution to 0:
            P(T_k|c) = 
        '''
        pass

