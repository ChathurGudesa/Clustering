import re
import sys
import numpy as np
from sklearn import cluster
from scipy.spatial.distance import cosine
from sklearn.metrics.pairwise import pairwise_distances

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)
fh = logging.FileHandler("logs/agreement_all.log")
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

def loadScores(
    result_file
):
    scores = {}
    with open(f"rankings/{result_file}") as f:
        lines = f.read().splitlines()
        for line in lines:
            words = re.split(" |\t", line)
            # print(words)
            # print(line, result_file)
            query_id = words[0]
            doc_id = words[2]
            if not query_id in scores:
                scores[query_id] = []
            scores[query_id].append(doc_id)
    return scores


def computeMAP(
    result_file, qrels_file
):
    qrel_scores = loadScores(qrels_file)
    computed_scores = loadScores(result_file)

    # print(qrel_scores)
    # print(computed_scores['51'])

    APs = []

    for query_id, doc_ids in computed_scores.items():
        # print(computed_scores[query_id])
        # print(qrel_scores[str(int(query_id))])

        a = computed_scores[query_id]
        b = qrel_scores[str(int(query_id))]
        # print(len(set(a) & set(b)))

        relevant = 0
        total = 0
        precisions = []
        for doc_id in doc_ids:
            total += 1
            if doc_id in qrel_scores[str(int(query_id))]:
                relevant += 1
                precisions.append(relevant/total)
        if len(precisions) > 0:
            AP = np.mean(precisions)
        else:
            AP = 0
        APs.append(AP)

    if len(APs) == 0:
        return 0
    # APs = sorted(APs, reverse=True)[0:10]
    return np.mean(APs)

if __name__ == "__main__":
    CollectionName = sys.argv[1]

    result_file = f"bm25-ranking-{CollectionName}"
    qrels_file = "trec12-news.tsv"

    MAP = computeMAP(
        result_file, qrels_file
    )

    with open(f"results/bm25_{CollectionName}", "a") as f:
        f.write(f"MAP = {MAP}")


 