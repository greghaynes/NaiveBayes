import Stemmer

class Classifier(object):

    def __init__(self,
                 language='english',
                 common_words_path='data/commonwords.txt'):
        self.language = language
        self.stemmy = Stemmer.Stemmer(self.language)
        self.common_words = self.getCommonWords(common_words_path)
        self.category_data = {}
        self.total_category_trains = {}
        self.word_data = {}
        self.total_trains = 0

    def getCommonWords(self, path='data/commonwords.txt'):
        '''So we dont classify common words'''
        words = {}
        with open(path) as f:
            for line in f:
                if not line.startswith('#'):
                    stemmed_word = self.stemmy.stemWord(line[:-1])
                    words[stemmed_word] = True
        return words
    
    def getUsefulWords(self, text):
        '''Grab a list of unique words where each word is not a common word'''
        text.replace('\n', ' ')
        all_words = text.split(' ')
        useful_words_dict = {}
        for word in all_words:
            if len(word) > 0 and word not in self.common_words:
                useful_words_dict[self.stemmy.stemWord(word)] = True
        return useful_words_dict.keys()

    def train(self, category, text):
        '''Insert text as training data for category'''
        useful_words = self.getUsefulWords(text)
        for word in useful_words:
            # Get our category tally and total tally
            category_data = self.category_data.get(category, {})
            self.category_data[category] = category_data
            category_tally = category_data.get(word, 0)
            total_tally = self.word_data.get(word, 0)
            
            # Increment cat tally and total tally
            self.category_data[word] = category_tally + 1
            self.word_data[word] = total_tally + 1
        
        # increment number of tranings
        cat_trains = self.total_category_trains.get(category, 0)
        self.total_category_trains[category] = cat_trains + 1
        self.total_trains += 1

    def probCategory(self, category, text):
        '''Probability text is in given category'''
        if category not in self.category_data:
            return -1
        useful_words = self.getUsefulWords(text)
        num = 1.0
        den = 1.0
        for word in useful_words:
            word_cat_tally = self.category_data.get(word, 0)
            cat_tally = self.total_category_trains[category]
            t_num = (float(word_cat_tally) / cat_tally)
            if t_num == 0:
                t_num = 1
            num *= t_num
            t_den = (float(self.word_data.get(word, 0)) / self.total_trains)
            if t_den == 0:
                t_den = 1
            den *= t_den
        num *= (float(self.total_category_trains[category]) / self.total_trains)
        return num / den

if __name__ == '__main__':
    c = Classifier()
    c.train('cat', 'so very cuddly')
    c.train('baby', 'likes to be cuddly')
    print c.probCategory('cat', 'cuddly bear')
