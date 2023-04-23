# example of possible tfidf clustering for future use? currently not going to use due to quality issues

from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.cluster.hierarchy import fcluster
from scipy.spatial.distance import pdist
import fastcluster

sentences = ["In the future, check the bounds of the answer, and play around with the sample input, don't ignore it",
"Maybe when the cost of something involves floor/ceiling and depends on the number of terms, consider using 1/2 terms at a time",
"If the numbers you have are a_1, a_2, a_3, .... a_n-1, a_n = (a_1^a_2^a_3^a_4^...^a_n) then that means you have a_1^a_2^a_3^...^a_n=0. In general be willing to consider if the operation over all numbers can help you get a simpler condition. Maybe also be willing to consider cases like this with larger n than the sample input to make sure you haven't missed anything. (again this idea was from the sample input)",
"Prefix sums of xor can detect if a subarray has xor of 0.",
"In a greedy, you probably want the ending to be as EARLY as possible and NOT the beginning.",
"You can take advantage that if 1 more than the previous ending had the same xor, then that value must be 0",
"be willing to check if something you try over and over again can be computed at the start",
"be careful you don't do cycling operations in the WRONG direction!!",
"Try seeing if a certain value of the answer is possible (maybe can be extended to binary search)",
"Let what is going to happen already happen (forced moves first)",
"Maybe construct the answer backwards given a test case (given 0 try constructing the test case..)",
"Take advantage of a cycle to avoid rechecking the same bitmask multiple times. Avoid doing repeated work... Ask if you really REALLY need to do something...",
"Set everything to 0 when trying to find an upperbound to the answer; when dealing with cycles turning something on and then off again can help",
"You can also try avoiding redoing work by using cycles directly on the bitmask do you don't need to do any rotation on the transitions (if that makes sense)",
"See what move must/can be made always; can help you out",
"Maybe try complementary counting, seeing the case that won't work... See how you can force there to only be certain moves making the case not work",
"Try working out some small cases out (active problem solving); try to continue pumping out new ideas, don't get too stuck on one idea",
"read the problem carefully; check if the length is 1 to n; read it out loud before starting",
"Try to do the least work possible? Keep it simple. If you want to compute (a_0 - a_1) + (a_1 - a_2) + ... + (a_n-1 - a_n); maybe just store a_0 and a_n, don't bother trying to find the remaining (can be faster too)",
"If you want gcd(a_1,a_2,a_3,a_4,...a_n, x) > 1, then x does NOT have to be the lcm... x just needs to contain the prime divisors of a_1,a_2,...,a_n",
"once again; given subset find answer for that is very powerful",
"also maybe do some thinking based on taking a possible optimal solution and making it better (or at least the same)???",
"think about just using one person/move for a certain component (e.g. value of b for this problem)",
"side note: when setting ans=0, check if the answer could be lower possibly..",
"just because i < n and j < i does NOT mean i < j. So be careful of using pref[j] in this case because it may NOT already cover i.",
"If you have two options of selecting one option and then determining the other option, consider 'reversing this'. E.g. start with fixing the second operation, try finding the first operation. This can be much easier to do while the other way maybe hard/impossible."
]
sentences = [sentence.lower() for sentence in sentences]
vectors = TfidfVectorizer().fit_transform(sentences)
print(vectors.todense())
cluster_id = fcluster(fastcluster.linkage(vectors.todense(), method='average', metric='cosine', preserve_input=True), t=0.85, criterion='distance')
clusters = {}
for i in range(len(cluster_id)):
    if(cluster_id[i] not in clusters):
        clusters[cluster_id[i]] = [sentences[i]]
    else:
        clusters[cluster_id[i]].append(sentences[i])
for key in clusters:
    print(f"Id: {key}")
    for sentence in clusters[key]:
        print(sentence)
    print("-------------------------------------\n")