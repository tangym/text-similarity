# -*- encoding:utf-8 -*-
import json
import Levenshtein
from flask import Flask, request

__author__ = 'TYM'
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def score():
    if request.method == 'POST':
        data = request.json if request.json else json.loads(request.data.decode('utf-8'))
        if 'query' not in data or 'document' not in data:
            return '{\"error message\": \"missing argument\"}'

        distance = Levenshtein.distance
        if 'method' in data:
            methods = {'hamming': Levenshtein.hamming,
                       'levenshtein': Levenshtein.distance,
                       'jaro': Levenshtein.jaro,
                       'jaro-winkler': Levenshtein.jaro_winkler}
            if data['method'] in methods:
                distance = methods[data['method']]

        similarity = 1 / (1 + distance(data['query'], data['document']))
        return '{\"similarity\": %f}' % similarity

        # return json.dumps(json.loads(request.data.decode('utf8'))) # request.json if request.json else None
    elif request.method == 'GET':
        return '''please POST json data: <br>
                {
                    "query" : "decf",
                    "document": "abcdefg"
                } <br>
                this service will return the similarity score (0, 1] based on Levenshtein distance in json format: <br>
                {
                    'similarity' : 0.25
                }
                Tips:
                - <s>remember to set the content type as 'application/json'</s>
                - please use utf-8 encoding and double quotes for keys and values if you concatenates strings manually'''


if __name__ == '__main__':
    app.run(debug=True)

