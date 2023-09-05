# put 2022 - 2023 season amc problems into collection (2022 AMC 10/12, 2023 AMC 8/AIME/USA(J)MO)

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
        "name": "AMC 8",
        "collection_id": 3,
        "problems": 25,
        "year": 2023
    },
    {
        "name": "AMC 10A",
        "collection_id": 4,
        "problems": 25,
        "year": 2022
    },
    {
        "name": "AMC 10B",
        "collection_id": 5,
        "problems": 25,
        "year": 2022
    },
    {
        "name": "AMC 12A",
        "collection_id": 6,
        "problems": 25,
        "year": 2022
    },
    {
        "name": "AMC 12B",
        "collection_id": 7,
        "problems": 25,
        "year": 2022
    },
    {
        "name": "AIME I",
        "collection_id": 8,
        "problems": 15,
        "year": 2023
    },
    {
        "name": "AIME II",
        "collection_id": 9,
        "problems": 15,
        "year": 2023
    },
    {
        "name": "USAJMO",
        "collection_id": 10,
        "problems": 6,
        "year": 2023
    },
    {
        "name": "USAMO",
        "collection_id": 11,
        "problems": 6,
        "year": 2023
    }
]

for test in tests:
    collection = Collection.objects.get(id=test["collection_id"])
    for prob_num in range(1, test["problems"] + 1):
        problem = Problem.objects.filter(name=f"{test['year']} {test['name']} Problem {prob_num}").first()
        new_problem_in_collection = ProblemInCollection(problem=problem, collection=collection)
        new_problem_in_collection.save()

