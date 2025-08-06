from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # Basic rule, one cannot be both knight and knave
    Or(AKnight, AKnave), 


    # A says "I am both a knight and a knave."
    Implication(AKnight, And(AKnight, AKnave)), # A tells the truth
    Implication(AKnave, Or(Not(AKnight), Not(AKnave))), # A tells a lie
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # Basic rule, one cannot be both knight and knave
    Or(AKnight, AKnave), 
    Or(BKnight, BKnave), 


    # A says "We are both knaves."
    Implication(AKnight, And(AKnave, BKnave)), # A tells the truth
    Implication(AKnave, Or(Not(AKnave), Not(BKnave))), # A tells a lie
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # Basic rule, one cannot be both knight and knave
    Or(AKnight, AKnave), 
    Or(BKnight, BKnave), 
    

    # A says "We are the same kind."
    # What A said is true and both A and B are from the same kind
    # Or what A said is false and both A and B are from differents kinds
    Implication(AKnight, BKnight), # A tells the truth
    Implication(AKnave, BKnight), # A tells a lie


    # B says "We are of different kinds."
    # What B said is true and both A and B are from differents kind
    # Or what B said is false and both A and B are from the same kind
    Implication(BKnight, AKnave), # A tells the truth
    Implication(BKnave, AKnave), # A tells a lie
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # Basic rule, one cannot be both knight and knave
    Or(AKnight, AKnave), 
    Or(BKnight, BKnave), 
    Or(CKnight, CKnave),


    # Evaluate A
    # A says either "I am a knight." or "I am a knave.", but you don't know which.
    Or(
        And(AKnight, AKnight), # "I am a knight."
        And(AKnight, AKnave), # "I am a knave."
        And(AKnave, AKnave), # "I am a knight."
        And(AKnave, AKnight) # "I am a knave."
    ),

    # Evaluate B
    # B says "A said 'I am a knave'."
    Implication(And(BKnight, AKnight), AKnave),
    Implication(And(BKnight, AKnave), AKnight),

    # B says "C is a knave."
    Biconditional(BKnight, CKnave),
    Biconditional(BKnave, CKnight),

    # Evaluate C
    # C says "A is a knight."
    Biconditional(CKnight, AKnight),
    Biconditional(CKnave, AKnave),
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
