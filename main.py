import Stemmer
from naivebayes import NaiveBayes

def train_from_file(classifier, data_path):
    with open(data_path) as f:
        for line in f:
            category = line.split(':')[0]
            text = line[len(category)+1:]
            classifier.train(category, text)

if __name__ == '__main__':
    c = NaiveBayes()
    train_from_file(c, 'data/training_1.txt')

    print 'trying meat'
    print c.text_category_probability('meat', 'I want a taco')
    print c.text_category_probability('not_meat', 'I want a taco')

