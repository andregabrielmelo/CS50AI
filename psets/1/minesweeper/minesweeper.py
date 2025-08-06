import itertools
import random, copy


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if self.count == len(self.cells): return self.cells
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0: return self.cells
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge: list[Sentence] = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)
        self.mark_safe(cell)

        unknow_neighbours = set()
        new_count = copy.deepcopy(count)
        for neighbour in self.cell_neighbours(cell):
            
            # Verify if the neighbour is a mine
            if neighbour in self.mines:
                new_count -= 1
                continue

            # Verify if the neighbour is a safe place
            if neighbour in self.safes:
                continue
            
            # Just add unknown cells
            unknow_neighbours.add(neighbour)
            
        self.knowledge.append(Sentence(unknow_neighbours, new_count))

        # Reorganize knowledge
        change = True
        while change:
            change = False

            all_sentences = copy.deepcopy(self.knowledge)
            for sentence in all_sentences:
                
                # Verify if there is a sentence without bombs (count zero)
                if sentence.count == 0:
                    change = True

                    # Mark all cell as safe
                    for cell in sentence.cells: 
                        self.mark_safe(cell)

                # Verify if there is a sentece where the number of bombs and cells are the same
                if sentence.count == len(sentence.cells):
                    change = True

                    # Mark all cells as mines
                    for cell in sentence.cells:
                        self.mark_mine(cell)

            # Remove empty sets (set())
            self.knowledge = [sentence for sentence in self.knowledge if sentence.cells]   
            
            # Remove duplicates
            new_knowledge = []
            for sentence in self.knowledge:

                if sentence not in new_knowledge:
                    new_knowledge.append(sentence)

            self.knowledge = new_knowledge
                    
            # Subset reasoning
            all_sentences = copy.deepcopy(self.knowledge)
            new_sentences = []

            for i, sentence1 in enumerate(all_sentences):
                for j, sentence2 in enumerate(all_sentences):
                    if i == j: continue  # Avoid comparing the sentence with itself
                    
                    # Ensure subset inference works both ways
                    if sentence1.cells.issubset(sentence2.cells):
                        new_cells = sentence2.cells - sentence1.cells
                        new_count = sentence2.count - sentence1.count
                    elif sentence2.cells.issubset(sentence1.cells):
                        new_cells = sentence1.cells - sentence2.cells
                        new_count = sentence1.count - sentence2.count
                    else:
                        continue

                    # Ensure the new sentence is valid
                    if new_cells and new_count >= 0:
                        new_sentence = Sentence(new_cells, new_count)

                        # Avoid duplicates before adding
                        if new_sentence not in self.knowledge:
                            change = True
                            new_sentences.append(new_sentence)

            # Add inferred sentences to knowledge base
            self.knowledge.extend(new_sentences)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        safe_moves = []
        for i in range(self.height):
            for j in range(self.width):

                if ((i, j) not in self.mines and
                    (i, j) not in self.moves_made and
                    (i, j) in self.safes):
                    safe_moves.append((i, j))

        if len(safe_moves) == 0: return None
        return safe_moves.pop()

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        random_moves = []
        for i in range(self.height):
            for j in range(self.width):

                if ((i, j) not in self.mines and
                    (i, j) not in self.moves_made):
                    random_moves.append((i, j))

        if len(random_moves) == 0: return None
        return random_moves.pop()
    
    def cell_neighbours(self, cell: tuple) -> set[tuple]:
        """Return cell neighbours"""
        neighbours = set()
        for i in range(-1, 2):
            for j in range(-1, 2):
                neighbour_i = cell[0] + i
                neighbour_j = cell[1] + j

                # Make sure the neghbours does not contain the cell iteself
                if (neighbour_i, neighbour_j) == cell:
                    continue
                
                # Make sure the i and j are within bounds
                if 0 <= neighbour_i < self.height and 0 <= neighbour_j < self.width:
                    neighbours.add((neighbour_i, neighbour_j))
        
        return neighbours
