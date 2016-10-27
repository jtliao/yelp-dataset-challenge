import json
import urllib2
from nltk.sentiment import SentimentIntensityAnalyzer

def analyze():
    sentences = ["i love food", "i dont like that dish"]
    sid = SentimentIntensityAnalyzer()
    for s in sentences:
        print(s)
        ss = sid.polarity_scores(s)
        for k in sorted(ss):
            print('{0}:{1}, '.format(k, ss[k], end=''))


def sentiment():
    base_url = 'https://westus.api.cognitive.microsoft.com/'
    key = 'd9994fe3adf540e9bb1bc748b6a7779f'
    headers = {'Content-Type': 'application/json', 'Ocp-Apim-Subscription-Key': key, 'Accept': 'application/json'}

    input_texts = '{"documents":[{"id":"1","text":"hello world"},' \
                  '{"id":"2","text":"hello foo world"},' \
                  '{"id":"3","text":"hello my world"},]}'
    batch_sentiment_url = base_url + 'text/analytics/v2.0/sentiment'
    req = urllib2.Request(batch_sentiment_url, input_texts, headers)
    response = urllib2.urlopen(req)
    result = response.read()
    obj = json.loads(result)
    for sentiment_analysis in obj['documents']:
        print('Sentiment ' + str(sentiment_analysis['id']) + ' score: ' + str(sentiment_analysis['score']))


def main():
    analyze()

if __name__ == "__main__":
    main()