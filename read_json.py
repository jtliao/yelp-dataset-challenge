import json
data = []
with open('yelp_academic_dataset_business.json') as f:
    for line in f:
        data.append(json.loads(line))
print(data[0])