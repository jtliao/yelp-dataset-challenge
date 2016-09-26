import json

with open('yelp_academic_dataset_business.json') as data_file:
    data = json.load(data_file)
#filtered = [x for x in data if x['state'] == 'PA']