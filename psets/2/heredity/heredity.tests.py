from heredity import *

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}

FAMILIES = [

    # 0: simple
    {
        "Harry": {"name": "Harry", "mother": "Lily", "father": "James", "trait": None},
        "James": {"name": "James", "mother": None, "father": None, "trait": None},
        "Lily": {"name": "Lily", "mother": None, "father": None, "trait": None}
    },

    # 1: multiple children
    {
        "Arthur": {"name": "Arthur", "mother": None, "father": None, "trait": None},
        "Charlie": {"name": "Charlie", "mother": "Molly", "father": "Arthur", "trait": None},
        "Fred": {"name": "Fred", "mother": "Molly", "father": "Arthur", "trait": None},
        "Ginny": {"name": "Ginny", "mother": "Molly", "father": "Arthur", "trait": None},
        "Molly": {"name": "Molly", "mother": None, "father": None, "trait": None},
        "Ron": {"name": "Ron", "mother": "Molly", "father": "Arthur", "trait": None}
    },

    # 2: multiple generations
    {
        "Arthur": {"name": "Arthur", "mother": None, "father": None, "trait": None},
        "Hermione": {"name": "Hermione", "mother": None, "father": None, "trait": None},
        "Molly": {"name": "Molly", "mother": None, "father": None, "trait": None},
        "Ron": {"name": "Ron", "mother": "Molly", "father": "Arthur", "trait": None},
        "Rose": {"name": "Rose", "mother": "Ron", "father": "Hermione", "trait": None}
    }
]


# Update probabilities with new joint probability
# print(people)
p = joint_probability(FAMILIES[2], {"Rose"}, {"Ron"}, {"Ron"})
print(p)