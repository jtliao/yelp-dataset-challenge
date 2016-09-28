import json
from nltk.tokenize import word_tokenize
from nltk.tag.perceptron import PerceptronTagger
import matplotlib.pyplot as plt
#from pywordcloud import pywordcloud
from wordcloud import WordCloud

tagger = PerceptronTagger()
data = []
counter = 0
with open('yelp_academic_dataset_review.json') as f:
    for line in f:
        if counter < 1000:
            counter += 1
            data.append(json.loads(line))
        else:
            break

stars_dict = {1: {}, 1.5: {}, 2: {}, 2.5: {}, 3: {}, 3.5: {}, 4: {}, 4.5: {}, 5: {}}
valid_pos = {'JJ', 'JJR', 'JJS', 'UH', 'RBR', 'RBS', 'PDT'}
words = {1: '', 1.5: '', 2: '', 2.5: '', 3: '', 3.5: '', 4: '', 4.5: '', 5: ''}
for rev in data:
    #tagged = nltk.pos_tag(word_tokenize(rev['text']))
    tagged = tagger.tag(word_tokenize(rev['text']))
    for word in tagged:
        if word[1] in valid_pos:
            st = rev['stars']
            words[st] += word[0] + ' '
            if word[0] in stars_dict[st]:
                stars_dict[st][word[0]] += 1
            else:
                stars_dict[st][word[0]] = 1
# for w in sorted(stars_dict[5], key=stars_dict[5].get, reverse=True):
#     print(w, stars_dict[5][w])
#pywordcloud.create(words)
n = 5
wc = WordCloud().generate(words[n])
wc.to_file('review_'+str(n)+'star.png')
plt.imshow(wc)
plt.axis('off')
plt.show()
for w in sorted(stars_dict[1], key=stars_dict[1].get, reverse=True):
    print(w, stars_dict[1][w])