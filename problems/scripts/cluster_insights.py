"""
cluster insights using sentence transformers

From: https://github.com/UKPLab/sentence-transformers/blob/master/examples/applications/clustering/agglomerative.py
Copyright Notice: Copyright 2019 Nils Reimers
For the Apache License: see APACHE_LICENSE
For the NOTICE file with attributions see: NOTICE.txt in the root directory of this repo

This is a simple application for sentence embeddings: clustering
Sentences are mapped to sentence embeddings and then agglomerative clustering with a threshold is applied.
Modifications:
* cluster insights from this app and put those insights into the InsightCluster model
* custom value of distance_threshold
* clear InsightCluster model every time this script is run

THIS FILE IS LICENSED UNDER AGPLv3

Copyright (C) 2023 bkf2020

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, version 3 of the License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from sentence_transformers import SentenceTransformer
from sklearn.cluster import AgglomerativeClustering
import numpy as np
import os, sys, getopt
import django
from django.conf import settings

sys.path.insert(0, '../../')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'starlight.settings')
django.setup()

from problems.models import Insight, InsightCluster

desired_distance_threshold = 1.5 # default

embedder = SentenceTransformer('all-MiniLM-L6-v2')
options, arguments = getopt.getopt(sys.argv[1:], 'd:')
for option, argument in options:
    if option in ('-d'):
        desired_distance_threshold = float(argument)

# Future: only add insights that were modified?
InsightCluster.objects.all().delete()

insights_problem_ids = {}
for insight in Insight.objects.all():
    if insight.problem_id not in insights_problem_ids:
        insights_problem_ids[insight.problem_id] = [insight]
    else:
        insights_problem_ids[insight.problem_id].append(insight)
for problem_id in insights_problem_ids:
    print(problem_id)
    corpus = []
    sentence_id_insight = {}
    for insight in insights_problem_ids[problem_id]:
        corpus.append(insight.text)
    for i in range(len(insights_problem_ids[problem_id])):
        sentence_id_insight[i] = insights_problem_ids[problem_id][i]

    if len(corpus) == 0:
        continue
    elif len(corpus) == 1:
        new_insight_cluster = InsightCluster(
            problem_id=problem_id,
            insight=sentence_id_insight[0],
            cluster_id=cluster_id,
            first=True
        )
        new_insight_cluster.save()
        continue
        
    print("embedding corpus")
    corpus_embeddings = embedder.encode(corpus)
    
    # Normalize the embeddings to unit length
    print("normalizing the embeddings")
    corpus_embeddings = corpus_embeddings /  np.linalg.norm(corpus_embeddings, axis=1, keepdims=True)

    # Perform kmean clustering
    print("performing kmean clustering")
    clustering_model = AgglomerativeClustering(n_clusters=None, distance_threshold=desired_distance_threshold) #, affinity='cosine', linkage='average', distance_threshold=0.4)
    clustering_model.fit(corpus_embeddings)
    cluster_assignment = clustering_model.labels_

    clustered_problems = {}
    seen_cluster_id = {}
    for sentence_id, cluster_id in enumerate(cluster_assignment):
        new_insight_cluster = InsightCluster(
            problem_id=problem_id,
            insight=sentence_id_insight[sentence_id],
            cluster_id=cluster_id
        )
        if cluster_id not in seen_cluster_id:
            new_insight_cluster.first = True
            seen_cluster_id[cluster_id] = True
        new_insight_cluster.save()