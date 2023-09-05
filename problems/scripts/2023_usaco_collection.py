# put the 2022 - 2023 season usaco problems (bronze, silver, etc) into a colection

import django
from django.conf import settings
import os
import sys

sys.path.insert(0, '../../')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'starlight.settings')
django.setup()

from problems.models import Problem, Collection, ProblemInCollection

tests = [
    {
        "name": "Bronze",
        "collection_id": 12
    },
    {
        "name": "Silver",
        "collection_id": 13
    },
    {
        "name": "Gold",
        "collection_id": 14
    },
    {
        "name": "Platinum",
        "collection_id": 15
    }
]
for test in tests:
    collection = Collection.objects.get(id=test["collection_id"])
    problems_dec_2022 = Problem.objects.filter(name__search=f"2022 December {test['name']}")
    problems_rem = Problem.objects.filter(name__search=f"2023 {test['name']}")
    for problem in problems_dec_2022:
        new_problem_in_collection=ProblemInCollection(collection=collection,problem=problem)
        new_problem_in_collection.save()
    for problem in problems_rem:
        new_problem_in_collection=ProblemInCollection(collection=collection,problem=problem)
        new_problem_in_collection.save()
