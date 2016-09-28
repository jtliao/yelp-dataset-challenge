import json
from nltk.tokenize import word_tokenize
from nltk.tag.perceptron import PerceptronTagger
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm


def tag_reviews(n):
    tagger = PerceptronTagger()
    data = []
    counter = 0
    with open('yelp_academic_dataset_review.json') as f:
        for line in f:
            if counter < n:
                counter += 1
                data.append(json.loads(line))
            else:
                break
    stars_dict = {1: {}, 1.5: {}, 2: {}, 2.5: {}, 3: {}, 3.5: {}, 4: {}, 4.5: {}, 5: {}}
    valid_pos = {'JJ', 'JJR', 'JJS', 'UH', 'RBR', 'RBS', 'PDT'}
    filtered_words = {1: '', 1.5: '', 2: '', 2.5: '', 3: '', 3.5: '', 4: '', 4.5: '', 5: ''}
    stars_list = []
    review_list = []
    for rev in data:
        tagged = tagger.tag(word_tokenize(rev['text']))
        for word in tagged:
            filt = ''
            if word[1] in valid_pos:
                filt += word[0] + ' '
                st = rev['stars']
                filtered_words[st] += word[0] + ' '
                if word[0] in stars_dict[st]:
                    stars_dict[st][word[0]] += 1
                else:
                    stars_dict[st][word[0]] = 1
                stars_list.append(st)
                review_list.append(rev['text'])
    return filtered_words, review_list, stars_list
# for w in sorted(stars_dict[1], key=stars_dict[1].get, reverse=True):
#     print(w, stars_dict[1][w])


def predict_star(review_list, stars_list, start, total):
    vectorizer = CountVectorizer(min_df=1)
    x = vectorizer.fit_transform(review_list)

    clf = svm.SVC()
    clf.fit(x, stars_list)

    counter = 0
    predict = 0.
    act = 0.
    with open('yelp_academic_dataset_review.json') as f:
        for _ in xrange(start):
            next(f)
        for line in f:
            if counter < total:
                counter += 1
                js = json.loads(line)
                pred = clf.predict(vectorizer.transform([js['text']]))
                act += js['stars']
                predict += pred
                # print 'actual:' + str(js['stars']) + ' prediction:' + str(pred)
            else:
                break
    print "accuracy = " + str(1 - (abs(act-predict)/act))


def word_cloud(words, n):
    wc = WordCloud().generate(words[n])
    wc.to_file('review_'+str(n)+'star.png')
    plt.imshow(wc)
    plt.axis('off')
    plt.show()


def main():
    words, reviews, stars = tag_reviews(2000)
    predict_star(reviews, stars, 2000, 500)
    # word_cloud(words, 5)


if __name__ == '__main__':
    main()
