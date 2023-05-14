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

from problems.models import Insight, InsightCluster, OverallInsightCluster

desired_distance_threshold = 1.5 # default

embedder = SentenceTransformer('all-MiniLM-L6-v2')
options, arguments = getopt.getopt(sys.argv[1:], 'd:')
for option, argument in options:
    if option in ('-d'):
        desired_distance_threshold = float(argument)

# Future: only add insights that were modified?
OverallInsightCluster.objects.all().delete()

corpus = []
sentence_id_insights = []
for insight in Insight.objects.all():
    corpus.append(insight.text)
    sentence_id_insights.append(insight)

if len(corpus) == 0:
    quit()
elif len(corpus) == 1:
    cluster_id_in_problem = InsightCluster.objects.filter(
        insight=sentence_id_insights[0]
    ).first().cluster_id

    new_overall_insight_cluster = OverallInsightCluster(
        problem_id=sentence_id_insights[0].problem_id,
        insight=sentence_id_insights[0],
        cluster_id_overall=0,
        cluster_id_in_problem=cluster_id_in_problem
    )
    new_overall_insight_cluster.save()
    quit()

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
for sentence_id, cluster_id in enumerate(cluster_assignment):
    cluster_id_in_problem = InsightCluster.objects.filter(
        insight=sentence_id_insights[sentence_id]
    ).first().cluster_id

    new_overall_insight_cluster = OverallInsightCluster(
        problem_id=sentence_id_insights[sentence_id].problem_id,
        insight=sentence_id_insights[sentence_id],
        cluster_id_overall=cluster_id,
        cluster_id_in_problem=cluster_id_in_problem
    )
    new_overall_insight_cluster.save()