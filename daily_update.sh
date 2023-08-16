#!/bin/sh
# run on fly server
cd /code/problems/scripts && echo "CF" && python cf_problems.py && echo "AC" && python atcoder_problems.py && echo "DMOJ" && python dmoj_problems.py && echo "cluster hints" && python cluster_hints.py && echo "cluster insights" && python cluster_insights.py && echo "cluster insights overall" && python cluster_insights_overall.py