import json
import pickle
import matplotlib.pyplot as plt
import time
from scipy.stats.stats import pearsonr
from nltk.sentiment import SentimentIntensityAnalyzer


def json_to_dict():
    # Tagger tags each word with its part of speech
    data = []
    counter = 0
    with open('yelp_academic_dataset_tip.json') as f:
        for line in f:
            counter += 1
            json_line = json.loads(line)
            json_dict = {"text": json_line["text"], "likes": json_line["likes"], "date": json_line["date"],
                         "business_id": json_line["business_id"], "user_id": json_line["user_id"]}
            data.append(json_dict)
    pickle.dump(data, open("tips.pkl", "wb"))


def analyze_text(tips, reviews):
    tip_count = 0

    tips_dict = {}
    review_stars_list = []
    star_count_dict = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    star_length_dict = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}

    for tip in tips:
        tip_count += 1
        tokens = str.split(tip["text"])
        tips_dict[(tip["date"], tip["user_id"], tip["business_id"])] = tokens

    for review in reviews:
        if (review["date"], review["user_id"], review["business_id"]) in tips_dict:
            review_stars_list.append(review["stars"])
            star_count_dict[review["stars"]] += 1
            star_length_dict[review["stars"]] += len(tips_dict[(review["date"], review["user_id"],
                                                                review["business_id"])])

    plt.hist(review_stars_list)
    plt.xlabel("Stars")
    plt.ylabel("Frequency of Tips")
    plt.xlim(1, 5)
    plt.show()

    plt.scatter([1, 2, 3, 4, 5], [star_length_dict[1]/star_count_dict[1], star_length_dict[1]/star_count_dict[2],
                                  star_length_dict[1]/star_count_dict[3], star_length_dict[1]/star_count_dict[4],
                                  star_length_dict[1]/star_count_dict[5]])
    plt.xlabel("Stars")
    plt.ylabel("Average Text length")
    plt.show()


def main():
    start = time.time()
    # json_to_dict() # uncomment this to generate the pickled file, then comment it out on subsequent runs
    tips_dict = pickle.load(open("tips.pkl", "rb"))
    reviews_dict = pickle.load(open("reviews.pkl", "rb"))
    end = time.time()
    print("time taken to load: " + str(end-start))
    print("loaded")
    analyze_text(tips_dict, reviews_dict)


if __name__ == '__main__':
    main()
