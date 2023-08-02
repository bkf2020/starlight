# put every problem in the usaco problemset in the database

import django
from django.conf import settings
import os
import sys

sys.path.insert(0, '../../')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'starlight.settings')
django.setup()

from problems.models import Problem
import requests
import re
from bs4 import BeautifulSoup

for year in range(14, 24):
    for month in ["dec", "jan", "feb", "open"]:
        URL = f"http://usaco.org/index.php?page={month}{year}results"
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        h2_on_page = soup.find_all('h2')
        for h2 in h2_on_page:
            contest_name = h2.text.strip()
            contest_types = ["Platinum", "Gold", "Silver", "Bronze"]
            works = False
            for contest_type in contest_types:
                if contest_type in contest_name:
                    works = True
                    break
            if works:
                problem_information_wrapper = h2.find_next('div', {"class": "panel historypanel"})
                while problem_information_wrapper.name == "div":
                    problem_information = problem_information_wrapper.findChildren('div', recursive=False)[1]
                    problem_name = contest_name + ": " + problem_information.b.text.strip()
                    problem_link = "http://usaco.org/" + problem_information.findChildren("a", recursive=False)[0]['href']
                    problem_information_wrapper = problem_information_wrapper.find_next_sibling()
                    if(Problem.objects.filter(name=problem_name, link=problem_link, problem_type="usaco").count() == 0):
                        new_problem = Problem(
                            name=problem_name,
                            link=problem_link,
                            problem_type="usaco"
                        )
                        new_problem.save()

