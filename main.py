import Stemmer
from naivebayes import NaiveBayes

if __name__ == '__main__':
    c = NaiveBayes()
    c.train('cat', 'so very cuddly red blue green')
    c.train('baby', 'likes to be cuddly')
    c.train('cat', 'doesnt get cuddly with a bear')

    print 'trying cat'
    print c.text_category_probability('cat', 'cuddly bear blue')

    print 'trying baby'
    print c.text_category_probability('baby', 'cuddly bear blue')
