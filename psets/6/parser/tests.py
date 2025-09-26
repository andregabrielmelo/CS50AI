from tkinter.tix import Tree
import nltk
import sys


def main():
    t = nltk.Tree.fromstring(
        "(S (NP (D the) (N dog)) (VP (V chased) (NP (D the) (N cat))))"
    )

    for subtree in t.subtrees():
        print(subtree)

    print("\n\n\n")

    for subtree in t:
        print(subtree)

    print(len(t))
    print(t[0])
    print(t[1])


if __name__ == "__main__":
    main()
