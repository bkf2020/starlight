# put AMC/AIME problems links in the database

import django
from django.conf import settings
import os
import sys

sys.path.insert(0, '../../')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'starlight.settings')
django.setup()

from problems.models import Problem

tests = ["AMC_8", "AMC_10", "AMC_12", "AIME"]
test_types = {}
test_types["AMC_8"] = [""]
test_types["AMC_10"] = ["A", "B"]
test_types["AMC_12"] = ["A", "B"]
test_types["AIME"] = ["I", "II"]

for test in tests:
    for year in range(2010, 2024):
        if(year == 2023 and (test == "AMC_10" or test == "AMC_12")):
            continue
        if(year == 2021 and (test == "AMC_8")):
            continue
        for test_type in test_types[test]:
            ending = 26
            if(test == "AIME"):
                ending = 16
            for num in range(1, ending):
                if(test == "AIME"):
                    URL = "https://artofproblemsolving.com/wiki/index.php/" + str(year) + "_" + test + "_" + test_type + "_Problems#Problem_" + str(num)
                    problem_name = str(year) + " " + test + " " + test_type + " Problem " + str(num)
                else:
                    URL = "https://artofproblemsolving.com/wiki/index.php/" + str(year) + "_" + test + test_type + "_Problems#Problem_" + str(num)
                    problem_name = str(year) + " " + test.replace("_", " ") + test_type + " Problem " + str(num)
                new_problem = Problem(
                    name=problem_name,
                    link=URL
                )
                new_problem.save()