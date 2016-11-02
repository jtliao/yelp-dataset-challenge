import json
import pickle
import nltk
import matplotlib.pyplot as plt
import time
from scipy.stats.stats import pearsonr


def json_to_dict():
    # Tagger tags each word with its part of speech
    data = []
    counter = 0
    with open('yelp_academic_dataset_review.json') as f:
        for line in f:
            counter += 1
            json_line = json.loads(line)
            json_dict = {"funny": json_line["votes"]["funny"], "useful": json_line["votes"]["useful"],
                         "cool": json_line["votes"]["cool"], "stars": json_line["stars"], "text": json_line["text"],
                         "business_id": json_line["business_id"], "user_id": json_line["user_id"]}
            data.append(json_dict)
    pickle.dump(data, open("reviews.pkl", "wb"))


def analyze_text(reviews):
    review_count = 0
    total_length = 0

    stars_list = []
    length_list = []

    for review in reviews:
        review_count += 1
        if review_count % 10000 == 0:
            print(review_count)
        #tokens = nltk.word_tokenize(review["text"])
        tokens = str.split(review["text"])
        total_length += len(tokens)
        stars_list.append(review["stars"])
        length_list.append(len(tokens))

    avg_length = total_length/review_count
    print("average review length: " + str(avg_length))

    corr = pearsonr(length_list, stars_list)
    print("correlation constant, text length vs stars: " + str(corr[0]))

    plt.scatter(length_list, stars_list)
    plt.xlabel("Text length")
    plt.ylabel("Stars")
    plt.show()

    plt.hist(length_list, bins=100)
    plt.xlabel("Text length")
    plt.ylabel("Frequency")
    plt.xlim(0, 1000)
    plt.show()


def main():
    start = time.time()
    # json_to_dict() # uncomment this to generate the pickled file, then comment it out on subsequent runs
    reviews_dict = pickle.load(open("reviews.pkl", "rb"))
    end = time.time()
    print(end-start)
    print("Reviews loaded")
    analyze_text(reviews_dict)


if __name__ == '__main__':
    main()
