import classifier

class NaiveBayes(classifier.Classifier):
    '''
    A modified naive bayes classifier which doesnt assume zero probability
    for samples which have never been seen in a class
    '''

    def __init__(self,
                 language='english',
                 common_words_path='data/commonwords.txt'):
        super(NaiveBayes, self).__init__(language, common_words_path)
        self._category_word_occurences = {}
        self._category_num_samples = {}
        self.num_samples = 0

    @property
    def num_categories(self):
        return len(self._categories)

    def train(self, category, text):
        cat_word_cnts = self._category_word_occurences.get(category, {})
        cat_num_samples = self._category_num_samples.get(category, 0)
        useful_words = self.useful_words(text)
        for word in useful_words:
            # update word count in category
            word_cnt = cat_word_cnts.get(word, 0)
            cat_word_cnts[word] = word_cnt + 1
        self._category_word_occurences[category] = cat_word_cnts
        self._category_num_samples[category] = cat_num_samples + 1
        self.num_samples += 1

    def classify(self, text):
        pass

    def text_category_probability(self, category, text):
        '''
        Probability of text being in category is calculated by:
            P(category|text) = P(text|category)P(category) / P(text)
        
        Sub equations are:
        P(text|category) = P(text_elem_1|category)*P(text_elem_2|category)...

        P(text_elem_n|category) =
            elem_n_occurences in category / category_occurences

        P(category) = category_occurences / samples

        P(text) = 1 / num_samples
        '''
        if category not in self._category_word_occurences:
            raise ValueError('No elements have been trained for category')

        useful_words = self.useful_words(text)
        cat_word_occurences = self._category_word_occurences[category]

        p_text_given_category = float(1)
        for word in useful_words:
            try:
                word_cat_cnt = cat_word_occurences[word]
            except KeyError:
                # negative weight for words that we havent seen
                # If we set this to zero then words we havent seen drive the
                # probability to 0. We set it to 1 / num_samples to increase
                # the negative weight as we gain more training data
                word_cat_cnt = 1 / float(self.num_samples)

            p_word_given_category = (float(word_cat_cnt) / 
                                    self._category_num_samples[category])
            #print 'word prob for %s: %f' % (word, p_word_given_category)
            p_text_given_category *= p_word_given_category

        #print 'prob text given category is %f' % p_text_given_category
        p_category = (self._category_num_samples[category] /
                     float(self.num_samples))
        num = p_text_given_category * p_category
        p_text = float(1) / self.num_samples
        #print 'prob for text is %f' % (p_text)
        return num / p_text
