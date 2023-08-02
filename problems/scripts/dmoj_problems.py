# put every problem in the dmoj problemset in the database

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

URL = "https://dmoj.ca/api/v2/problems"
page = requests.get(URL)
data = json.loads(page.content)
total_pages = data["data"]["total_pages"]

for page in range(1, total_pages + 1):
    URL = "https://dmoj.ca/api/v2/problems?page=" + str(page)
    page = requests.get(URL)
    data = json.loads(page.content)
    for problem in data["data"]["objects"]:
        problem_name = "DMOJ " + problem['name']
        problem_link = "https://dmoj.ca/problem/" + problem['code']
        if(Problem.objects.filter(name=problem_name, link=problem_link, problem_type="dmoj").count() == 0):
            new_problem = Problem(
                name=problem_name,
                link=problem_link,
                problem_type="dmoj"
            )
            new_problem.save()