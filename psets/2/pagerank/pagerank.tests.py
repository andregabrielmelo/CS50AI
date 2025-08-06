from pagerank import *

DAMPING = 0.85
SAMPLES = 10000

corpus = crawl("corpus0")

# Test transiton model
# result = transition_model({"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}, "1.html", DAMPING)

# Test sample rank
# result = sample_pagerank(corpus, DAMPING, SAMPLES)

# Test iterate pagerank
result = iterate_pagerank({'1': {'2'}, '2': {'3', '1'}, '3': {'2', '5', '4'}, '4': {'1', '2'}, '5': set()}, DAMPING)
print(result)