import Stemmer
from naivebayes import NaiveBayes
from improvednb import ImprovedNB

def train_from_file(classifier, data_path):
    with open(data_path) as f:
        for line in f:
            category = line.split(':')[0]
            text = line[len(category)+1:]
            classifier.train(category, text)

if __name__ == '__main__':
    c1 = NaiveBayes()
    c2 = ImprovedNB()
    train_from_file(c1, 'data/training_1.txt')
    train_from_file(c2, 'data/training_1.txt')

    print 'trying meat'
    print 'c1:', c1.text_category_probability('meat', 'I want a taco')
    print 'c2:', c2.text_category_probability('meat', 'I want a taco')
    print 'c1:', c1.text_category_probability('not_meat', 'I want a taco')
    print 'c2:', c2.text_category_probability('not_meat', 'I want a taco')

