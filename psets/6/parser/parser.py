import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP
NP -> N | N AP | Adj NP | Det NP | N PP | P NP | N CP | N VP
VP -> V | V NP | V AP | V CP | Det VP
PP -> P | P NP
AP -> Adv | Adv NP | Adv CP
CP -> Conj NP | Conj VP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():
    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence: str):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """

    words = []
    tokenized_words = nltk.word_tokenize(sentence)

    for i in range(len(tokenized_words)):
        # Remove words with no alphabetic character
        if not any(char.isalpha() for char in tokenized_words[i]):
            continue

        # Words to lowercase
        word = tokenized_words[i].lower()

        words.append(word)

    return words


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """

    # If there is nothing left to chunck
    if tree.height() == 2:
        return []

    chunks = []

    # Get chuncks from all children
    for child in tree:
        chunks += np_chunk(child)

    # If no child produced an NP, and this tree is NP, add this as a chunk
    if len(chunks) == 0 and tree.label() == "NP":
        return [tree]

    return chunks


def debug(words, labels, number=None):
    if number:
        labels = labels[:number]
        words = words[:number]

    print(labels)
    print(words)

    teste = parser.chart_parse(words)
    for t in teste:
        print(t)


if __name__ == "__main__":
    main()
