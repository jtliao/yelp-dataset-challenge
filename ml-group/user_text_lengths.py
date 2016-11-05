import nltk
import json
import numpy as np
from matplotlib import pyplot as plt
# from sklearn import linear_model
from scipy import stats

def read_pittsburg_reviews(business_file, reviews_file, out_file):
    # businesses_in_pitt = set()
    # print("starting to read business file")
    # with open(business_file, "r") as f:
    #     for line in f:
    #         record = json.loads(line)
    #         if record["city"] == "Pittsburgh":
    #             businesses_in_pitt.add(record["business_id"])
    # print("done reading business file")
    ctr = 0
    user_id_to_reviews = {}
    with open(reviews_file, "r") as f:
        for line in f:
            record = json.loads(line)
            # if record["business_id"] in businesses_in_pitt:
            if True:
                ctr += 1
                print(ctr)
                user_id = record["user_id"]
                review = record["text"]
                tokens = nltk.word_tokenize(review)
                length = len(tokens)
                stars = record["stars"]
                if user_id in user_id_to_reviews:
                    user_id_to_reviews[user_id].append((stars, length))
                else:
                    user_id_to_reviews[user_id] = [(stars, length)]

    with open(out_file, "w") as f:
        for user_id, review_list in user_id_to_reviews.items():
            # print(user_id)
            json.dump(review_list, f)
            f.write("\n")


def analyze_review_lengths(reviews_file):
    with open(reviews_file, "r") as f:
        stars = []
        z_lengths = []

        # 1 list for each star rating
        stars_len_list = [[], [], [], [], []]

        for line in f:
            record = json.loads(line)
            if len(record) >= 10:
                lengths = []
                for [_, length] in record:
                    lengths.append(length)
                mean = np.mean(lengths)
                std = np.std(lengths)
                for [star_rating, length] in record:
                    stars.append(star_rating)
                    z_length = (length - mean) / (std)
                    z_lengths.append(z_length)

                    # add to corresponding list
                    stars_len_list[star_rating - 1].append(z_length)

    # plt.scatter(z_lengths, stars)
    # plt.xlabel("Text length normalized by user")
    # plt.ylabel("Stars")
    # plt.show()

    slope, intercept, r_value, p_value, std_err = stats.linregress(z_lengths, stars)
    print 'Coefficients: %f' % slope
    print 'Intercept: %f' % intercept
    print 'R^2: %f' % r_value ** 2
    print 'P-value: %f' % p_value
    print "Std err: %f" % std_err


    for i in xrange(5):
        plt.subplot(3, 2, i + 1)
        plt.hist(stars_len_list[i])
        plt.title(str(i + 1) + " stars")
    plt.show()

def main():
    # Just run once to write pitt_reviews file
    # read_pittsburg_reviews("yelp_academic_dataset_business.json", "yelp_academic_dataset_review.json", "pitt_reviews.json")

    analyze_review_lengths("pitt_reviews.json")

if __name__ == "__main__":
    main()