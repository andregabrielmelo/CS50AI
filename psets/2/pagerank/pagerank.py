import os
import random
import re
import sys
import copy


DAMPING = 0.85
SAMPLES = 10000


def main():

    # Verify if it was passed an parameter to the program
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")

    corpus = crawl(sys.argv[1]) # Call crawl function based in a directory that represents a collection of pages
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES) # Calculate the pagerank of each page in corpus by sampling

    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")

    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    # The random probability for choosing a page should be: 1 - Damping Factor / Number of Pages
    random_page = (1 - damping_factor)
    pages_in_corpus = len(corpus)
    damping_random_page = random_page / pages_in_corpus

    # Keep track of the possibility to visit each page next
    transition_model = dict()

    # Iterate over all pages 
    for current_page in corpus:

        # All pages have a initial equal probability to be accessed
        if current_page not in transition_model:
            transition_model[current_page] = damping_random_page

        # Verifiy if the current_page is the one you are current on
        if current_page == page:
            if len(corpus[current_page]) == 0:
                probability_links = DAMPING/len(corpus) + damping_random_page
                for p in corpus:
                    transition_model[p] = probability_links

                return transition_model


            probability_links = DAMPING/len(corpus[current_page])

            # Verify all pages linked to by the current_page
            for link in corpus[current_page]:

                # Confirm the key alredy exists
                if link not in transition_model:
                    transition_model[link] = damping_random_page

                transition_model[link] +=  probability_links # divide the rest of the probability equally between links

    return transition_model

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # Get all pages
    base_pages: list = [page for page in corpus]

    # Keep track of samples
    samples: list = list()

    # Keep track of probability
    sample_probability: dict = dict()

    # Get total number of pages in corpus
    number_of_pages: int = len(corpus)

    # Define a random first page
    random_index: int = random.randint(0, number_of_pages-1)
    page: str = base_pages[random_index]

    # Do sampling n times
    for num in range(n):

        # Insert current page into sample
        samples.append(page) 

        # Add to the sample probability that the page appeared one more time
        sample_probability[page] = sample_probability.get(page, 0) + 1

        # Get the transition model of the current page
        model = transition_model(corpus, page, damping_factor)
        
        # Get a list of pages and weights based in the model
        pages = list()
        weights = list()
        for page in model:
            weight = model[page]

            pages.append(page)
            weights.append(weight)

        # Choose a random page to go next
        [page] = random.choices(pages, weights)

    # Divede the number of times a page appeared by the number os samples
    sample_size = len(samples)
    probability: dict[float] = {}

    for page in sample_probability:
        probability[page] = sample_probability[page]/sample_size

    # Return samples
    return probability


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # Keep track of pagerank
    current_pagerank = dict()

    # Calculate the total number of pages in corpus
    pages_quantity = len(corpus)
    
    # Assig each page a rank of 1 / pages_quantity
    for page in corpus:
        current_pagerank[page] = 1 / pages_quantity

    # A page that has no links at all should be interpreted as having one link for every page in the corpus (including itself).
    for page in corpus:
        if len(corpus[page]) == 0:
            corpus[page] = [link for link in corpus]

    # First condition to calculate page rank 
    goto_random_page: float = (1 - damping_factor) / pages_quantity

    changes_pagerank = [float("inf"), float("inf"), float("inf")]
    while any(diff > 0.001 for diff in changes_pagerank):

        # New change rank list
        changes_pagerank = []

        # Keep track of the previous pagerank
        previous_pagerank = copy.deepcopy(current_pagerank)

        # Calculate new page rank
        for current_page in corpus:

            # Gather all pages that link to current page
            pages_linked = set()
            for other_page in corpus:
                other_page_links = corpus[other_page]
                if current_page in other_page_links:
                    pages_linked.add(other_page)
 
            # For each page that link to current page, sum their page rank divided by the number of links in their page
            sum_pages: float = 0.0
            for i in pages_linked:
                sum_pages += current_pagerank[i]/num_links(corpus, i)

            goto_linked_page: float = damping_factor * sum_pages

            # New pagerank
            current_pagerank[current_page] = goto_random_page + goto_linked_page

            # Difference between previous and current pagerank
            changes_pagerank.append(abs(previous_pagerank[current_page] - current_pagerank[current_page]))

    return current_pagerank


def num_links(corpus, page):
    links_quantity: int = len(corpus[page])
    return links_quantity


if __name__ == "__main__":
    main()
