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
    c3 = ImprovedNB(multinominal=True)
    classifiers = [c1, c2, c3]

    for classifier in classifiers:
        train_from_file(classifier, 'data/training_1.txt')

    print 'trying meat'
    for classifier in classifiers:
        print classifier.text_category_probability('meat', 'I want a taco')

    print 'trying not meat'
    for classifier in classifiers:
        print classifier.text_category_probability('not_meat',
            'Salads are nice')

