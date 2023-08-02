# put every problem in the codeforces problemset in the database

import django
from django.conf import settings
import os
import sys

sys.path.insert(0, '../../')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'starlight.settings')
django.setup()

from problems.models import Problem
import requests
import json

URL = "https://codeforces.com/api/problemset.problems"
page = requests.get(URL)
data = json.loads(page.content)
if data['status'] == "OK":
    for problem in reversed(data['result']['problems']):
        problem_name = "Codeforces " + str(problem['contestId']) + problem['index'] + ": " + problem['name']
        problem_link = "https://codeforces.com/problemset/problem/" + str(problem['contestId']) + "/" + problem['index']
        if(Problem.objects.filter(name=problem_name, link=problem_link).count() == 0):
            new_problem = Problem(
                name=problem_name,
                link=problem_link,
                problem_type="codeforces"
            )
            new_problem.save()
else:
    print("Error occured when talking to codeforces!")
