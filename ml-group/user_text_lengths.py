import nltk
import json
import numpy as np
from matplotlib import pyplot as plt
# from sklearn import linear_model
from scipy import stats
import seaborn as sns
import math

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
                # print(ctr)
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


def sort_by_num_reviews(review_lengths_file):
    with open(review_lengths_file, "r") as f:
        all_lines = f.readlines()

        # print(all_lines[0:3])

        all_lines_sorted = sorted(all_lines, key=lambda list_str: len(json.loads(list_str)), reverse=True)
        # print(len(all_lines[0]))
        # print(len(all_lines[1]))
        # print(len(all_lines[2]))

        all_lines_lists = map(lambda list_str: json.loads(list_str), all_lines_sorted)

        all_line_lens = map(lambda list_of_lists: len(list_of_lists), all_lines_lists)
        all_line_log_lens = map(lambda list_of_lists: math.log(len(list_of_lists)), all_lines_lists)
        # print(all_line_lens[-1])
        sns.set_style("whitegrid")
        sns.kdeplot(np.array(all_line_log_lens))
        sns.plt.show()

        # Examine where the spikes occur

        # all_lines = map(lambda list_str: len(json.loads(list_str)), all_lines)
        # print(all_lines[0:50])

        # stars = []
        # z_lengths = []

        # 1 list for each star rating
        # stars_len_list = [[], [], [], [], []]

        # Only do for top x users
        # x = 1
        # for i in range(0, x):
        #     record = all_lines_lists[i]
        #     lengths = []
        #     for [_,length] in record:
        #         lengths.append(length)
        #
        #     mean = np.mean(lengths)
        #     std = np.std(lengths)
        #
        #     for [star_rating, length] in record:
        #         stars.append(star_rating)
        #         z_length = (length - mean) / (std)
        #         z_lengths.append(z_length)
        #
        #         # add to corresponding list
        #         stars_len_list[star_rating - 1].append(z_length)
        #
        # f, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5)
        # axes = [ax1, ax2, ax3, ax4, ax5]
        # for i in xrange(5):
        #     sns.set_style("whitegrid")
        #     sns.kdeplot(np.array(stars_len_list[i]), ax=axes[i])
        # plt.show()

def analyze_review_lengths(reviews_file):
    with open(reviews_file, "r") as f:
        stars = []
        z_lengths = []

        # 1 list for each star rating
        stars_len_list = [[], [], [], [], []]

        for line in f:
            record = json.loads(line)
            if len(record) >= 30:
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

    # sns.set_style("whitegrid")
    # sns.kdeplot(np.array(stars_len_list[0]))
    # sns.plt.show()

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


    # for i in xrange(5):
    #     plt.subplot(3, 2, i + 1)
    #     plt.hist(stars_len_list[i])
    #     plt.title(str(i + 1) + " stars")
    # plt.show()

    f, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5)

    axes = [ax1, ax2, ax3, ax4, ax5]

    for i in xrange(5):
        sns.set_style("whitegrid")
        sns.kdeplot(np.array(stars_len_list[i]), ax=axes[i])
    plt.show()



def main():
    # Just run once to write pitt_reviews file
    # read_pittsburg_reviews("yelp_academic_dataset_business.json", "yelp_academic_dataset_review.json", "review_lengths.json")

    # analyze_review_lengths("review_lengths.json")

    sort_by_num_reviews("review_lengths.json")

if __name__ == "__main__":
    main()