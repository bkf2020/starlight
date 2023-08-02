# put every problem in the atcoder problemset in the database

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

URL = "https://kenkoooo.com/atcoder/resources/problems.json"
page = requests.get(URL)
data = json.loads(page.content)
for problem in data:
    problem_name = "AtCoder " + problem['contest_id'].upper() + ": " + problem['title']
    problem_link = "https://atcoder.jp/contests/" + problem['contest_id'] + "/tasks/" + problem['id']
    if(Problem.objects.filter(name=problem_name, link=problem_link, problem_type="atcoder").count() == 0):
        new_problem = Problem(
            name=problem_name,
            link=problem_link,
            problem_type="atcoder"
        )
        new_problem.save()