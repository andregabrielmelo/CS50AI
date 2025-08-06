import csv
import itertools
import sys

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


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """

    # Keep track of joint probability (initialize to 1)
    probability: float = 1

    # Loop through everyone
    for person in people:

        # Check if the person does not have the genes
        if person not in one_gene and person not in two_genes:

            # Get their parents
            father = people[person]["father"]
            mother = people[person]["mother"]

            # If the person does not have parents
            if father == None or mother == None:
                person_probability: float = PROBS["gene"][0]

            # Now if the person has parents 
            else:
                person_probability: float = father_mother_passed_gene(person, father, mother, one_gene, two_genes, people)  

            # Check if the person also does not have the trait too
            if person not in have_trait:
                person_probability *= PROBS["trait"][0][False]

            # Check if the person also has the trait
            elif person in have_trait:
                person_probability *= PROBS["trait"][0][True]

            # Join probability
            probability *= person_probability

    # Everyone in one_gene has one copy of the gene
    for person in one_gene:

        # Get their parents
        father = people[person]["father"]
        mother = people[person]["mother"]

        # If the person does not have parents
        if father == None or mother == None:
            person_probability: float = PROBS["gene"][1]

        # Now if the person has parents 
        else:
            person_probability: float = father_mother_passed_gene(person, father, mother, one_gene, two_genes, people)    
        
        # If the person have the trait
        if person in have_trait:
            person_probability *= PROBS["trait"][1][True]

        # If the person does not have the trait
        elif person not in have_trait:
            person_probability *= PROBS["trait"][1][False]

        # Join probability
        probability *= person_probability
    
    # Everyone in two_genes has one copy of the gene
    for person in two_genes:
        
        # Get their parents
        father = people[person]["father"]
        mother = people[person]["mother"]

        # If the person does not have parents
        if father == None or mother == None:
            person_probability: float = PROBS["gene"][2]

        # Now if the person has parents
        else:
            person_probability: float = father_mother_passed_gene(person, father, mother, one_gene, two_genes, people)    
        
        # If the person have the trait
        if person in have_trait:
            person_probability *= PROBS["trait"][2][True]

        # If the person does not have the trait
        elif person not in have_trait:
            person_probability *= PROBS["trait"][2][False]

        # Join probability
        probability *= person_probability

    return probability


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """

    # Update all people in probababilities
    for person in probabilities:

        # Update people with zero genes
        if person not in one_gene and person not in two_genes:
            probabilities[person]["gene"][0] += p
        
        # Update people with one gene
        if person in one_gene:
            probabilities[person]["gene"][1] += p

        # Update people with two genes
        if person in two_genes:
            probabilities[person]["gene"][2] += p

        # Update people with the trait
        if person in have_trait:
            probabilities[person]["trait"][True] += p

        # Update people without the trait
        if person not in have_trait:
            probabilities[person]["trait"][False] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """

    # Normalize statistics of all people in probababilities
    for person in probabilities:

        # Get genes probabilities
        zero_gene_probability = probabilities[person]["gene"][0]
        one_gene_probability = probabilities[person]["gene"][1]
        two_gene_probability = probabilities[person]["gene"][2]
        total_gene_probability = zero_gene_probability + one_gene_probability + two_gene_probability

        # Get trait probabilities
        have_trait_possibility = probabilities[person]["trait"][True]
        not_have_trait_possibility = probabilities[person]["trait"][False]
        total_traits_probability = zero_gene_probability + one_gene_probability + two_gene_probability

        # Check if genes needs to be normalized
        if total_gene_probability != 1:     

            # Update zero genes probability
            probabilities[person]["gene"][0] = zero_gene_probability / total_gene_probability

            # Update one gene probability
            probabilities[person]["gene"][1] = one_gene_probability / total_gene_probability

            # Update two genes probability
            probabilities[person]["gene"][2] = two_gene_probability / total_gene_probability

        # Check if trats needs to be normalized
        if total_traits_probability != 1:  

            # Update have trait prossibility
            probabilities[person]["trait"][True] = have_trait_possibility / total_traits_probability 
            
            # Update not have trait prossibility
            probabilities[person]["trait"][False] = not_have_trait_possibility / total_traits_probability 


def father_mother_passed_gene(person: str, father: str, mother: str, one_gene, two_genes, people):
    """Return the probability of the mother and father passing theis genes.
    Basically, there are two ways this can happen, 
    either the person gets from it's father and not the mother, 
    or from it's mother and not the father"""

    # Get the father parents
    father_father = people[father]["father"]
    father_mother = people[father]["mother"]

    # If he has both parents
    if father_father and father_mother:
        gene_probability = father_mother_passed_gene(father, father_father, father_mother, one_gene, two_genes, people)
        father_passed: float = gene_probability
        father_not_passed: float = 1 - gene_probability

    # if the father has 0 copies of the gene
    elif father not in one_gene and father not in two_genes:

        # He can only pass if the gene suffer a mutation
        father_passed: float = PROBS["mutation"]
        father_not_passed: float = 1 - PROBS["mutation"]

    # If the father have one gene
    elif father in one_gene:
        
        # He can pass the one mutated gene, or the gene that is not alredy mutated can be passed and mutated
        father_passed: float = 0.5 + 0.5 * 0.001
        father_not_passed: float = 1 - (0.5 + 0.5 * 0.001)
    
    # If the father have two genes
    elif father in two_genes:

        # If the father has 2 genes, he can pass the mutated gene unless it suffers a mutation
        father_passed: float = 1 - PROBS["mutation"]
        father_not_passed: float = PROBS["mutation"]

    # Get the mother parents
    mother_father = people[mother]["father"]
    mother_mother = people[mother]["mother"]

    # If he has both parents
    if mother_father and mother_mother:
        gene_probability = father_mother_passed_gene(mother, mother_father, mother_mother, one_gene, two_genes, people)
        mother_passed: float = gene_probability
        mother_not_passed: float = 1 - gene_probability

    # if the mother has 0 copies of the gene
    if mother not in one_gene and mother not in two_genes:
        
        # She can only pass if the gene suffer a mutation
        mother_passed: float = PROBS["mutation"]
        mother_not_passed: float = 1 - PROBS["mutation"]
    
    # If the mother have one_gene
    elif mother in one_gene:

        # She can pass the one mutated gene, or the gene that is not alredy mutated can be passed and mutated
        mother_passed: float = 0.5 + 0.5 * 0.001
        mother_not_passed: float = 1 - (0.5 + 0.5 * 0.001)

    # If the mother have two genes
    elif mother in two_genes:

        # If the mother has 2 genes, he can pass the mutated gene unless it suffers a mutation
        mother_passed: float = 1 - PROBS["mutation"]
        mother_not_passed: float = PROBS["mutation"]    

    # If the person have one gene, either the mother or father passed it to him
    if person in one_gene:
        return (father_passed * mother_not_passed) + (father_not_passed * mother_passed)
    
    # If the person have two genes, both the mother and father passed it to him
    elif person in two_genes:
        return father_passed * mother_passed
    
    # Else, he has no gene, and neither mother or father passed it to him
    else:
        return mother_not_passed * father_not_passed


if __name__ == "__main__":
    main()
