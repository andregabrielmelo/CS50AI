from copy import deepcopy
import sys
from unittest import result

from crossword import Variable, Crossword


class CrosswordCreator:
    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy() for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont

        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size, self.crossword.height * cell_size),
            "black",
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                rect = [
                    (j * cell_size + cell_border, i * cell_size + cell_border),
                    (
                        (j + 1) * cell_size - cell_border,
                        (i + 1) * cell_size - cell_border,
                    ),
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (
                                rect[0][0] + ((interior_size - w) / 2),
                                rect[0][1] + ((interior_size - h) / 2) - 10,
                            ),
                            letters[i][j],
                            fill="black",
                            font=font,
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for variable in self.crossword.variables:
            variable_domain = deepcopy(self.domains[variable])
            for value in variable_domain:
                # Remove value who do not respect the variable length
                if len(value) != variable.length:
                    self.domains[variable].remove(value)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """

        revised = False

        # The pair (i, j) should be interpreted to mean that the ith character of
        # v1’s value must be the same as the jth character of v2’s value.
        position_tuple = self.crossword.overlaps[(x, y)]
        if position_tuple is None:
            return revised

        i, j = position_tuple

        # If a value in self.domains[x] does not correspond to any variable in self.domains[y], remove it
        # It correnspond to a value only if they have the same letter for the position they overlap
        domain_x = self.domains[x].copy()
        for word_x in domain_x:
            if all(word_x[i] != word_y[j] for word_y in self.domains[y]):
                self.domains[x].remove(word_x)

                revised = True

        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """

        queue = arcs

        # If arcs is None, start with an initial queue of all of the arcs in the problem
        if queue is None:
            queue = []

            # Fill queue with arcs from all variables
            for x in self.crossword.variables:
                for y in self.crossword.variables:
                    if x != y and (x, y) not in queue:
                        queue.append((x, y))

        # Revise arcs until solution is found or the domain is empty
        while len(queue) != 0:
            (x, y) = queue.pop()

            if self.revise(x, y):
                # If the domain is empty after revision, there is no solution
                if len(self.domains[x]) == 0:
                    return False

                # Get all x eighbours minus y
                neighbours = self.crossword.neighbors(x)
                neighbours.remove(y)

                # Enforce arc consistency bewtween them
                for z in neighbours:
                    queue.append((z, x))

        return True

    def assignment_complete(self, assignment: dict[Variable, str]):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """

        # If the assignement does not contain all variables, return false
        if any(variable not in assignment for variable in self.crossword.variables):
            return False

        # If some variable does not contain an assigned value, return false
        if any(value is None for key, value in assignment.items()):
            return False

        # If all variables (keys) have a value, it is complete (true)
        return True

    def consistent(self, assignment: dict[Variable, str]):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        for variable, word in assignment.items():
            # Verify if they are correct length
            if len(word) != variable.length:
                return False

            for key, value in assignment.items():
                # Do not compare the the variable to itself
                if variable != key:
                    # Verify if all values are distict
                    if word == value:
                        print("Hello")

                    # Verify if the is a conflict, if two overlapping variables have different values for the same position
                    position_tuple = self.crossword.overlaps[(variable, key)]
                    if position_tuple is None:
                        continue

                    i, j = position_tuple
                    if word[i] != value[j]:
                        return False

        return True

    def order_domain_values(self, var: Variable, assignment: dict[Variable, str]):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        # Order the domain values, by less constraining values (values that leave open more possibilities)

        # Dictionary for value and number of values they rule out for neighbouring values
        all_values = {}
        for value in self.domains[var]:
            count_ruled_out_values = 0

            # Get neighbours
            neighbours = self.crossword.neighbors(var)

            # Remove variables with assigned values
            for assigned_variable, v in assignment.items():
                if assigned_variable in neighbours:
                    neighbours.remove(assigned_variable)

            # Count the number of ruled out values from neighbours if this value is selected
            for neighbour_variable in neighbours:
                # Verify if variables overlap
                overlap_tuple = self.crossword.overlaps[(var, neighbour_variable)]

                for neighbour_value in self.domains[neighbour_variable]:
                    # Duplicates
                    if neighbour_value == value:
                        count_ruled_out_values += 1

                    # Overlaping with different letter values
                    if overlap_tuple is not None:
                        i, j = overlap_tuple
                        if value[i] != neighbour_value[j]:
                            count_ruled_out_values += 1

            all_values[value] = count_ruled_out_values

        # sort by all values by count_ruled_out_values
        all_values = dict(sorted(all_values.items(), key=lambda item: item[1]))

        # return only the values as a list
        return list(all_values.keys())

    def select_unassigned_variable(
        self, assignment: dict[Variable, str]
    ) -> Variable | None:
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        # Get possible variables, excluding those alredy assigned
        possible_variables = deepcopy(list(self.crossword.variables))
        for variable in self.crossword.variables:
            if variable in assignment:
                possible_variables.remove(variable)

        # Initialize with the first possible variable
        selected_var = possible_variables[0]

        for variable in possible_variables:
            variable_remaning_domain_values = len(self.domains[variable])
            selected_variable_remaning_domain_values = len(self.domains[selected_var])

            # If the variable has less values in its domains than the curret selected variable, select it
            if (
                variable_remaning_domain_values
                < selected_variable_remaning_domain_values
            ):
                selected_var = variable

            # If there is a tie, select the variable with the most neighbours
            elif (
                variable_remaning_domain_values
                == selected_variable_remaning_domain_values
            ):
                variable_neighbours_count = len(self.crossword.neighbors(variable))
                selected_variable_neighbours_count = len(
                    self.crossword.neighbors(selected_var)
                )
                if variable_neighbours_count > selected_variable_neighbours_count:
                    selected_var = variable

        return selected_var

    def backtrack(self, assignment: dict[Variable, str]):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        # If all variables have an assigned value, the solution is found, then return it
        if self.assignment_complete(assignment):
            return assignment

        # Select a variable that is not yet assigned
        var: Variable = self.select_unassigned_variable(assignment)

        # Try to pick a value in the selected variable, ordered by preferred value
        for value in self.order_domain_values(var, assignment):
            assignment[var] = value

            # If value is consistent with the assignment
            if self.consistent(assignment):
                # Consider all options based in this assignment
                result = self.backtrack(assignment)
                if result is not False:
                    return result

            # If result is false, it is a failure, so remove it
            assignment.pop(var)


def main():
    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword: Crossword = Crossword(structure, words)
    creator: CrosswordCreator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
