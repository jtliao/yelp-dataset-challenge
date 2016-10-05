import json
from nltk.tokenize import word_tokenize
from nltk.tag.perceptron import PerceptronTagger
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm


def tag_reviews(n):
    # Tagger tags each word with its part of speech
    tagger = PerceptronTagger()
    data = []
    counter = 0
    with open('yelp_academic_dataset_review.json') as f:
        for line in f:
            # Read in n lines
            if counter < n:
                counter += 1
                data.append(json.loads(line))
            else:
                break
    print "Read %d lines from the review json file" % n

    # Turns out that reviews are only whole stars
    # This dictionary maps star value to dictionaries that map from word to number of times
    # that word appears in a review that has the certain star value.
    stars_dict = {1: {}, 2: {}, 3: {}, 4: {}, 5: {}}
    # These are the parts of speech -- adjectives, interjections, adverbs, and pre-determiners
    valid_pos = {'JJ', 'JJR', 'JJS', 'UH', 'RB', 'RBR', 'RBS', 'PDT'}
    # This dictionary maps star value to string of words that appear in reviews with that star value
    filtered_words = {1: '', 2: '', 3: '', 4: '', 5: ''}

    # Stores list of stars and corresponding reviews
    stars_list = []
    review_list = []

    review_bigram_list = []

    for rev in data:

        # Separates review text into each word and then tagger tages each word with part of speech
        review = rev['text']

        review_bigram_list += [review]

        tagged = tagger.tag(word_tokenize(rev['text']))
        filt = ''

        for word in tagged:
            # Check if part of speech is one of the ones that we are looking for
            if word[1] in valid_pos:
                filt += word[0] + ' '
                st = rev['stars']
                filtered_words[st] += word[0] + ' '
                if word[0] in stars_dict[st]:
                    stars_dict[st][word[0]] += 1
                else:
                    stars_dict[st][word[0]] = 1
        stars_list.append(st)
        review_list.append(filt)
    return filtered_words, review_list, review_bigram_list, stars_list
# for w in sorted(stars_dict[1], key=stars_dict[1].get, reverse=True):
#     print(w, stars_dict[1][w])


def predict_star(review_list, stars_list, reviews_bigram, start, total):
    #print review_list
    # print reviews_bigram

    bigram_vectorizer = CountVectorizer(ngram_range=(2,2))
    x_2 = bigram_vectorizer.fit_transform(reviews_bigram)
    print x_2
    clf_bigram = svm.SVC(kernel='linear')
    clf_bigram.fit(x_2, stars_list)

    # This transforms each review to bag-of-words vector
    vocab = {}
    index = 0
    for r in review_list:
        words = r.split()
        for item in words:
            if item not in vocab:
                vocab[item] = index
                index += 1
    vectorizer = CountVectorizer(vocabulary=vocab)
    x = vectorizer.fit_transform(review_list)
    # print x

    # Classifier is SVM classification
    clf = svm.SVC(kernel='linear')
    clf.fit(x, stars_list)

    print "Finished converting reviews to Bag-Of-Words"

    predict_bigram = 0.
    act_bigram = 0.
    error_bigram = 0.

    counter = 0
    predict = 0.
    act = 0.
    error = 0.
    with open('yelp_academic_dataset_review.json') as f:
        # Skip the first 'start' entries that we used for training
        for _ in xrange(start):
            next(f)
        print "Starting to predict the next %d reviews" % total
        for line in f:
            if counter < total:
                counter += 1
                js = json.loads(line)

                review = [js['text']]
                pred = clf.predict(vectorizer.transform(review))
                pred_bigram = clf_bigram.predict(bigram_vectorizer.transform(review))
                print "pred is %d" % pred_bigram

                stars = js['stars']
                act += stars
                act_bigram += stars

                print "stars is %d" % stars

                predict += pred
                predict_bigram += pred_bigram
                # print 'actual:' + str(js['stars']) + ' prediction:' + str(pred)

                error += (abs(act-predict)/act)
                error_bigram += (abs(act_bigram-pred_bigram)/act_bigram)
            else:
                break
    print "accuracy = " + str(1 - (error/counter))
    print "accuracy bigram = " + str(1 - (error_bigram/counter))


def word_cloud(words, n):
    wc = WordCloud().generate(words[n])
    wc.to_file('review_'+str(n)+'star.png')
    plt.imshow(wc)
    plt.axis('off')
    plt.show()


def main():
    words, reviews, review_bigrams, stars = tag_reviews(1000)
    predict_star(reviews, stars, review_bigrams, 1000, 500)
    #word_cloud(words, 5)


if __name__ == '__main__':
    main()
