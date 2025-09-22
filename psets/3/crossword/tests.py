import sys
from generate import CrosswordCreator, Variable
from crossword import Crossword

# Parse command-line arguments
structure = sys.argv[1]
words = sys.argv[2]
output = sys.argv[3] if len(sys.argv) == 4 else None

# Generate crossword
crossword: Crossword = Crossword(structure, words)
creator: CrosswordCreator = CrosswordCreator(crossword)

var: Variable = Variable(0, 0, "UP", 5)
assignment: dict[Variable, str] = {var: "hello"}

creator.enforce_node_consistency()
print(creator.select_unassigned_variable(assignment))
