# -*- encoding:utf-8 -*-
import json
import Levenshtein
from flask import Flask, request
import jieba
import cfg

__author__ = 'TYM'
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def score():
    if request.method == 'POST':
        data = request.json if request.json else json.loads(request.data.decode('utf-8'))
        if 'query' not in data or 'document' not in data:
            return '{\"error message\": \"missing argument\"}'

        similarity = convert_distance_to_similarity(Levenshtein.distance)
        if 'method' in data:
            methods = {'hamming': convert_distance_to_similarity(Levenshtein.hamming),
                       'levenshtein': convert_distance_to_similarity(Levenshtein.distance),
                       'jaro': convert_distance_to_similarity(Levenshtein.jaro),
                       'jaro-winkler': convert_distance_to_similarity(Levenshtein.jaro_winkler),
                       'bm25': bm25}
            if data['method'] in methods:
                similarity = methods[data['method']]

        return '{\"similarity\": %f}' % similarity(data['query'], data['document'])

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

def convert_distance_to_similarity(func):
    def _decorator(query, document):
        similarity = 1 / (1 + func(query, document))
        return similarity
    return _decorator

def segmentation(s):
    return list(jieba.cut_for_search(s))

def bm25(query, document):
    bm25_score = 0
    seg_doc = segmentation(document)
    seg_q = segmentation(query)
    K = cfg.BM25_K1 * (1 - cfg.BM25_B
        + cfg.BM25_B * len(seg_doc) / cfg.BM25_AVERAGE_DOCUMENT_LENGTH)
    for seg in seg_q:
        frequency = len(list(filter(lambda e: e==seg, seg_doc)))
        # TODO: add weight according to IDF
        bm25_score += frequency * (cfg.BM25_K1 + 1) / (frequency + K)
    return bm25_score

if __name__ == '__main__':
    app.run(debug=True)

