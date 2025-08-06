from minesweeper import *

ai = MinesweeperAI(height=4, width=5)
ai.add_knowledge((0, 1), 1)
ai.add_knowledge((1, 0), 1)
ai.add_knowledge((1, 2), 1)
ai.add_knowledge((3, 1), 0)
ai.add_knowledge((0, 4), 0)
ai.add_knowledge((3, 4), 0)
safes = [(0, 0), (0, 2)]
for safe in safes:
    if safe not in ai.safes:
        print(f"did not find {safe} in safe cells when possible to conclude safe")

print(ai.safes)
print(ai.mines)