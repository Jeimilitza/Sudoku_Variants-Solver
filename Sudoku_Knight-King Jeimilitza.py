"""
Author: Jeimilitza Sainz Lopez
Chess Knight and King move Sudoku
"""
import pygame
# Imported to generate random numbers
import random
# Imported to seed the random number generator with the current time
import time
# Imported to get functions to iterate/count over values in efficient way
import itertools


def init_grid():
    # Fill the background
    screen.fill(WHITE)

    # Draw the grid
    for row in range(9):
        for column in range(9):
            color = WHITE
            pygame.draw.rect(screen, color, [(margin + grid_size) * column + margin, (margin + grid_size) * row + margin, grid_size, grid_size])
            
            if grid[row][column] != 0:
                text = font.render(str(grid[row][column]), True, BLACK)
                text_rect = text.get_rect(center=((margin + grid_size) * column + margin + grid_size / 2, (margin + grid_size) * row + margin + grid_size / 2))
                screen.blit(text, text_rect)

    # Draw the lines
    for i in range(10):
        if i % 3 == 0:
            color = BLACK
        else:
            color = GRAY
        pygame.draw.line(screen, color, (margin, (margin + grid_size) * i + margin), (margin + 9 * (grid_size + margin), (margin + grid_size) * i + margin), 2)
        pygame.draw.line(screen, color, ((margin + grid_size) * i + margin, margin), ((margin + grid_size) * i + margin, margin + 9 * (grid_size + margin)), 2)
        
# Checks classical sudoku, Knight move and Kings move restrictions
def check_restrictions(num, row, col):
    print("Checking restrictions...")
    if grid[row][col] == 0:
        # Check row
        for i in range(9):
            if grid[row][i] == num:
                return False
    
        # Check column
        for i in range(9):
            if grid[i][col] == num:
                return False
    
        # Check 3x3
        box_x = col // 3
        box_y = row // 3
        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if grid[i][j] == num:
                    return False
        
        # Check King's move
        if row > 0:
            if grid[row-1][col] == num:
                return False
        if row < 8:
            if grid[row+1][col] == num:
                return False
        if col > 0:
            if grid[row][col-1] == num:
                return False
        if col < 8:
            if grid[row][col+1] == num:
                return False
        if row > 0 and col > 0:
            if grid[row-1][col-1] == num:
                return False
        if row < 8 and col < 8:
            if grid[row+1][col+1] == num:
                return False
        if row > 0 and col < 8:
            if grid[row-1][col+1] == num:
                return False
        if row < 8 and col > 0:
            if grid[row+1][col-1] == num:
                return False
          
    
        # Check Knight's move
        if row < 8 and col > 1:
            if grid[row+1][col-2] == num:
                return False
        if row < 8  and col < 7:
            if grid[row+1][col+2] == num:
                return False
        if row > 0 and col > 1:
            if grid[row-1][col-2] == num:
                return False
        if row > 0 and col < 7:
            if grid[row-1][col+2] == num:
                return False
        if row > 1 and col < 8:
            if grid[row-2][col+1] == num:
                return False
        if row < 7 and col < 8:
            if grid[row+2][col+1] == num:
                return False
        if row > 1 and col > 0:
            if grid[row-2][col-1] == num:
                return False
        if row < 7 and col > 0:
            if grid[row+2][col-1] == num:
                return False
        
        print("Valid")
        return True
    else:
        return False
        

# Inserts initial values into the sudoku grid
def initial_values(values):
    print("Setting up initial values...")
    global grid

    grid[3][1] = values[0]
    grid[6][0] = values[0]
    grid[5][4] = values[0]
    grid[0][2] = values[0]
    grid[8][3] = values[0]

    grid[6][2] = values[1]
    grid[4][0] = values[1]
    grid[3][3] = values[1]
    grid[0][4] = values[1]
    grid[8][5] = values[1]

    grid[2][6] = values[2]
    grid[4][8] = values[2]
    grid[5][5] = values[2]
    grid[0][3] = values[2]
    grid[8][4] = values[2]

    grid[5][7] = values[3]
    grid[2][8] = values[3]
    grid[3][4] = values[3]
    grid[0][5] = values[3]
    grid[8][6] = values[3]

    grid[5][8] = values[4]
    grid[2][0] = values[4]
    grid[3][5] = values[4]
    grid[4][2] = values[4]

    grid[4][4] = values[5]
    grid[0][8] = values[5]
    grid[8][0] = values[5]
    grid[2][2] = values[5]

    grid[0][1] = values[6]
    grid[6][8] = values[6]
    grid[8][2] = values[6]
    grid[1][7] = values[6]

    grid[0][0] = values[7]
    grid[6][7] = values[7]
    grid[3][8] = values[7]

    grid[8][8] = values[8]
    grid[5][0] = values[8]
    grid[0][7] = values[8]

# Notes all possible solutions of each cell   
def make_notations():
    print("Making notations...")
    global notations
    notations = [[[] for i in range(9)] for j in range(9)]
    for i in range(9):
        for j in range(9):
            for num in range(1, 10):
                valid = check_restrictions(num, i, j)
                if valid:
                    notations[i][j].append(num)
    
    
    find_Swordfish()
    find_YWing()
    find_XWing()           
    find_HiddenTriple()
    find_PointingTriple()
    find_NakedTriple()
    find_HiddenPair()
    find_PointingPair()
    find_NakedPair()
    return notations
             
# Find a value that only appears once in notations of same row, column or 3x3
def find_HiddenSingle():
    print("Looking for Hidden Singles...")
    global notations
    # Check rows
    for row in range(9):
        nums = []
        for col in range(9):
            for x in notations[row][col]:
                nums.append(x)
            
        for x in nums:
            if nums.count(x) == 1:
                for j in range(9):
                    if x in notations[row][j]:
                        grid[row][j] = x
                        make_notations()
                        print("Found Hidden Single in (%d, %d)" % (row, j))
    
    
    # Check columns
    for col in range(9):
        nums = []
        for row in range(9):
            for x in notations[row][col]:
                nums.append(x)
            
        for x in nums:
            if nums.count(x) == 1:
                for i in range(9):
                    if x in notations[i][col]:
                        grid[i][col] = x
                        make_notations()
                        print("Found Hidden Single in (%d, %d)" % (i, col))
                    
    # Check 3x3
    for r in range(0, 9, 3):
        for c in range(0, 9, 3):
            box_x = r // 3
            box_y = c // 3
            nums = []
            for i in range(box_y * 3, box_y * 3 + 3):
                for j in range(box_x * 3, box_x * 3 + 3):
                    for x in notations[i][j]:
                        nums.append(x)
                        
            for x in nums:
                if nums.count(x) == 1:
                    for row in range(box_y * 3, box_y * 3 + 3):
                        for col in range(box_x * 3, box_x * 3 + 3):
                            if x in notations[row][col]:
                                grid[row][col] = x
                                make_notations()
                                print("Found Hidden Single in 3x3 (%d, %d)" % (row, col))

    
    print("No Hidden singles")
                            
def find_NakedSingle():
    print("Looking for Naked Singles...")
    global notations
    # Check rows/cols
    for row in range(9):
        for col in range(9):
            if len(notations[row][col]) == 1:
                num = notations[row][col][0]
                grid[row][col] = num
                make_notations()
                print("Found Naked Single in (%d, %d)" % (row, col))
            
    # Check 3x3
    for r in range(0, 9, 3):
        for c in range(0, 9, 3):
            box_x = r // 3
            box_y = c // 3
            for i in range(box_y * 3, box_y * 3 + 3):
                for j in range(box_x * 3, box_x * 3 + 3):
                    if len(notations[i][j]) == 1:
                        num = notations[i][j][0]
                        grid[i][j] = num
                        make_notations()
                        print("Found Naked Single in (%d, %d)" % (i, j))
    
    print("No Naked singles")
    
    
def find_NakedPair():
    print("Looking for Naked Pairs...")
    global notations
    # Check rows
    for row in range(9):
        for i in range(9):
            for j in range(i+1, 9):
                if notations[row][i] == notations[row][j]:
                    nums = notations[row][i]
                    for col in range(9):
                        for num in nums:
                            if num in notations[row][col] and col != i and col != j:
                                notations[row][col].remove(num)
                    print("Found Naked Pairs in (%d, %d) (%d, %d)" % (row, i, row, j))
                    
    print("No Naked pairs")

def find_PointingPair():
    print("Looking for Pointing Pairs...")
    global notations
    
    # Check rows
    for row in range(9):
        for digit in range(1, 10):
            boxes = []
            for col in range(9):
                if digit in notations[row][col]:
                    boxes.append((row, col))
            if len(set(box[0] // 3 for box in boxes)) == 1:
                box_row = boxes[0][0] // 3
                for col in range(box_row * 3, box_row * 3 + 3):
                    if col not in range(boxes[0][1], boxes[-1][1]+1):
                        if digit in notations[row][col]:
                            notations[row][col].remove(digit)
                            print("Removed value %d from (%d, %d)" % (digit, row, col))

    # Check columns
    for col in range(9):
        for digit in range(1, 10):
            boxes = []
            for row in range(9):
                if digit in notations[row][col]:
                    boxes.append((row, col))
            if len(set(box[1] % 3 for box in boxes)) == 1:
                box_col = boxes[0][1] % 3
                for row in range(box_col, 9, 3):
                    if row not in range(boxes[0][0], boxes[-1][0]+1):
                        if digit in notations[row][col]:
                            notations[row][col].remove(digit)
                            print("Removed value %d from (%d, %d)" % (digit, row, col))
    
    print("No Pointing pairs")
   
def find_HiddenPair():
    print("Looking for Hidden Pairs...")
    global notations
    
    # Check rows
    for row in range(9):
        counts = {}
        for col in range(9):
            for val in notations[row][col]:
                if val not in counts:
                    counts[val] = []
                counts[val].append((row, col))
        for val in counts:
            if len(counts[val]) == 2:
                cells = counts[val]
                if cells[0][0] == cells[1][0]:
                    for i in range(9):
                        if i != cells[0][1] and i != cells[1][1]:
                            if val in notations[cells[0][0]][i]:
                                notations[cells[0][0]][i].remove(val)
                else:
                    for i in range(9):
                        if i != cells[0][0] and i != cells[1][0]:
                            if val in notations[i][cells[0][1]]:
                                notations[i][cells[0][1]].remove(val)
    
    # Check columns
    for col in range(9):
        counts = {}
        for row in range(9):
            for val in notations[row][col]:
                if val not in counts:
                    counts[val] = []
                counts[val].append((row, col))
        for val in counts:
            if len(counts[val]) == 2:
                cells = counts[val]
                if cells[0][1] == cells[1][1]:
                    for i in range(9):
                        if i != cells[0][0] and i != cells[1][0]:
                            if val in notations[i][cells[0][1]]:
                                notations[i][cells[0][1]].remove(val)
                else:
                    for i in range(9):
                        if i != cells[0][1] and i != cells[1][1]:
                            if val in notations[cells[0][0]][i]:
                                notations[cells[0][0]][i].remove(val)
    
    print("No Hidden pairs")   

def find_HiddenTriple():
    print("Looking for Hidden Triples...")
    global notations
    
    # Check rows
    for row in range(9):
        counts = {}
        for col in range(9):
            for val in notations[row][col]:
                if val not in counts:
                    counts[val] = []
                counts[val].append((row, col))
        for val in counts:
            if len(counts[val]) >= 2 and len(counts[val]) <= 3:
                for i in range(len(counts[val])):
                    for j in range(i+1, len(counts[val])):
                        for k in range(j+1, len(counts[val])):
                            cells = [counts[val][i], counts[val][j], counts[val][k]]
                            rows = set([cell[0] for cell in cells])
                            if len(rows) == 3:
                                for col in range(9):
                                    if (row, col) not in cells and val in notations[row][col]:
                                        notations[row][col].remove(val)
                            
    # Check columns
    for col in range(9):
        counts = {}
        for row in range(9):
            for val in notations[row][col]:
                if val not in counts:
                    counts[val] = []
                counts[val].append((row, col))
        for val in counts:
            if len(counts[val]) >= 2 and len(counts[val]) <= 3:
                for i in range(len(counts[val])):
                    for j in range(i+1, len(counts[val])):
                        for k in range(j+1, len(counts[val])):
                            cells = [counts[val][i], counts[val][j], counts[val][k]]
                            cols = set([cell[1] for cell in cells])
                            if len(cols) == 3:
                                for row in range(9):
                                    if (row, col) not in cells and val in notations[row][col]:
                                        notations[row][col].remove(val)
    
    # Check 3x3 boxes
    for box_row in range(0, 9, 3):
        for box_col in range(0, 9, 3):
            counts = {}
            for row in range(box_row, box_row+3):
                for col in range(box_col, box_col+3):
                    for val in notations[row][col]:
                        if val not in counts:
                            counts[val] = []
                        counts[val].append((row, col))
            for val in counts:
                if len(counts[val]) >= 2 and len(counts[val]) <= 3:
                    for i in range(len(counts[val])):
                        for j in range(i+1, len(counts[val])):
                            for k in range(j+1, len(counts[val])):
                                cells = [counts[val][i], counts[val][j], counts[val][k]]
                                box = set([(cell[0]//3, cell[1]//3) for cell in cells])
                                if len(box) == 3:
                                    for row in range(box_row, box_row+3):
                                        for col in range(box_col, box_col+3):
                                            if (row, col) not in cells and val in notations[row][col]:
                                                notations[row][col].remove(val)
    
    print("No Hidden Triples")

def find_NakedTriple():
    print("Looking for Naked Triples...")
    global notations
    
    # Check rows
    for row in range(9):
        for col1 in range(9):
            if len(notations[row][col1]) == 3:
                for col2 in range(col1+1, 9):
                    if len(notations[row][col2]) == 3:
                        for col3 in range(col2+1, 9):
                            if len(notations[row][col3]) == 3:
                                triple = set(notations[row][col1] + notations[row][col2] + notations[row][col3])
                                if len(triple) == 3:
                                    for col in range(9):
                                        if col != col1 and col != col2 and col != col3:
                                            for val in triple:
                                                if val in notations[row][col]:
                                                    notations[row][col].remove(val)
                                                    print("Removed value %d from (%d, %d)" % (val, row, col))
                                                    
    # Check columns
    for col in range(9):
        for row1 in range(9):
            if len(notations[row1][col]) == 3:
                for row2 in range(row1+1, 9):
                    if len(notations[row2][col]) == 3:
                        for row3 in range(row2+1, 9):
                            if len(notations[row3][col]) == 3:
                                triple = set(notations[row1][col] + notations[row2][col] + notations[row3][col])
                                if len(triple) == 3:
                                    for row in range(9):
                                        if row != row1 and row != row2 and row != row3:
                                            for val in triple:
                                                if val in notations[row][col]:
                                                    notations[row][col].remove(val)
                                                    print("Removed value %d from (%d, %d)" % (val, row, col))
    
    # Check 3x3 boxes
    for box_row in range(0, 9, 3):
        for box_col in range(0, 9, 3):
            cells = []
            for row in range(box_row, box_row+3):
                for col in range(box_col, box_col+3):
                    cells.append((row, col))
            for i in range(len(cells)):
                row1, col1 = cells[i]
                if len(notations[row1][col1]) == 3:
                    for j in range(i+1, len(cells)):
                        row2, col2 = cells[j]
                        if len(notations[row2][col2]) == 3:
                            for k in range(j+1, len(cells)):
                                row3, col3 = cells[k]
                                if len(notations[row3][col3]) == 3:
                                    triple = set(notations[row1][col1] + notations[row2][col2] + notations[row3][col3])
                                    if len(triple) == 3:
                                        for row, col in cells:
                                            if (row, col) != (row1, col1) and (row, col) != (row2, col2) and (row, col) != (row3, col3):
                                                for val in triple:
                                                    if val in notations[row][col]:
                                                        notations[row][col].remove(val)
                                                        print("Removed value %d from (%d, %d)" % (val, row, col))
print("Naked Triple check complete.")
                                              
                                                
def find_PointingTriple():
    print("Looking for Pointing Triples...")
    global notations
    
    # Check rows
    for row in range(9):
        for digit in range(1, 10):
            boxes = []
            for col in range(3):
                if digit in notations[row][col]:
                    boxes.append((row, col))
            if len(set(box[0] // 3 for box in boxes)) == 1:
                box_row = boxes[0][0] // 3
                for col in range(3, 9):
                    if digit in notations[row][col]:
                        if row // 3 == box_row:
                            for r in range(box_row * 3, box_row * 3 + 3):
                                if r != row:
                                    if digit in notations[r][col]:
                                        notations[r][col].remove(digit)
                                        print("Removed value %d from (%d, %d)" % (digit, r, col))
            elif len(set(box[0] // 3 for box in boxes)) == 2:
                continue

    # Check columns
    for col in range(9):
        for digit in range(1, 10):
            boxes = []
            for row in range(3):
                if digit in notations[row][col]:
                    boxes.append((row, col))
            if len(set(box[1] // 3 for box in boxes)) == 1:
                box_col = boxes[0][1] // 3
                for row in range(3, 9):
                    if digit in notations[row][col]:
                        if col // 3 == box_col:
                            for c in range(box_col * 3, box_col * 3 + 3):
                                if c != col:
                                    if digit in notations[row][c]:
                                        notations[row][c].remove(digit)
                                        print("Removed value %d from (%d, %d)" % (digit, row, c))
            elif len(set(box[1] // 3 for box in boxes)) == 2:
                continue

def find_XWing():
    print("Looking for X-Wing...")
    global notations
    
    for digit in range(1, 10):
        rows = []
        cols = []
        for row in range(9):
            if len([c for c in range(9) if digit in notations[row][c]]) == 2:
                rows.append(row)
        for col in range(9):
            if len([r for r in range(9) if digit in notations[r][col]]) == 2:
                cols.append(col)
        for r1 in rows:
            for r2 in rows:
                if r1 >= r2:
                    continue
                c1, c2 = None, None
                for c in range(9):
                    if digit in notations[r1][c] and digit in notations[r2][c]:
                        if c1 is None:
                            c1 = c
                        else:
                            c2 = c
                            break
                if c2 is not None:
                    for r in range(9):
                        if r != r1 and r != r2:
                            if digit in notations[r][c1]:
                                notations[r][c1].remove(digit)
                                print("Removed value %d from (%d, %d)" % (digit, r, c1))
                            if digit in notations[r][c2]:
                                notations[r][c2].remove(digit)
                                print("Removed value %d from (%d, %d)" % (digit, r, c2))
        for c1 in cols:
            for c2 in cols:
                if c1 >= c2:
                    continue
                r1, r2 = None, None
                for r in range(9):
                    if digit in notations[r][c1] and digit in notations[r][c2]:
                        if r1 is None:
                            r1 = r
                        else:
                            r2 = r
                            break
                if r2 is not None:
                    for c in range(9):
                        if c != c1 and c != c2:
                            if digit in notations[r1][c]:
                                notations[r1][c].remove(digit)
                                print("Removed value %d from (%d, %d)" % (digit, r1, c))
                            if digit in notations[r2][c]:
                                notations[r2][c].remove(digit)
                                print("Removed value %d from (%d, %d)" % (digit, r2, c))
    
    print("No X-wing found")

def find_YWing():
    print("Looking for Y-Wing...")
    global notations
    
    for row in range(9):
        for col in range(9):
            for digit in notations[row][col]:
                cells = {(r, c) for r, c in zip(range(row + 1, 9), itertools.repeat(col))}
                cells &= {(r, c) for r, c in zip(range(row + 1, 9), range(col + 1, 9))}
                for cell1 in cells:
                    if notations[cell1[0]][cell1[1]] == [digit]:
                        hinge_cells = {(r, c) for r, c in zip(range(row + 1, cell1[0]), itertools.repeat(col))}
                        hinge_cells &= {(r, c) for r, c in zip(itertools.repeat(row), range(col + 1, cell1[1]))}
                        for cell2 in hinge_cells:
                            if notations[cell2[0]][cell2[1]] == [digit]:
                                if notations[cell1[0]][cell1[1]] != notations[cell2[0]][cell2[1]]:
                                    new_digits = set(notations[row][col]) - set([digit])
                                    if new_digits.issubset(notations[cell1[0]][cell1[1]]) and new_digits.issubset(notations[cell2[0]][cell2[1]]):
                                        for r in range(row + 1, 9):
                                            if r != cell1[0]:
                                                if digit in notations[r][cell1[1]]:
                                                    notations[r][cell1[1]].remove(digit)
                                                    print("Removed value %d from (%d, %d)" % (digit, r, cell1[1]))
                                        for c in range(col + 1, 9):
                                            if c != cell2[1]:
                                                if digit in notations[cell2[0]][c]:
                                                    notations[cell2[0]][c].remove(digit)
                                                    print("Removed value %d from (%d, %d)" % (digit, cell2[0], c))
    print("No Y-Wing found")

def find_Swordfish():
    print("Looking for Swordfish...")
    global notations
    
    # Check rows
    for row in range(9):
        for digit in range(1, 10):
            cols = []
            for col in range(9):
                if digit in notations[row][col]:
                    cols.append(col)
            if len(cols) == 3:
                rows = []
                for row2 in range(9):
                    if row2 != row and digit in notations[row2][cols[0]] and digit in notations[row2][cols[1]] and digit in notations[row2][cols[2]]:
                        rows.append(row2)
                if len(rows) == 3:
                    for col1 in range(9):
                        if col1 not in cols and digit in notations[rows[0]][col1] and digit in notations[rows[1]][col1] and digit in notations[rows[2]][col1]:
                            for r in rows:
                                if digit in notations[r][col1]:
                                    notations[r][col1].remove(digit)
                                    print("Removed value %d from (%d, %d)" % (digit, r, col1))
    
    # Check columns
    for col in range(9):
        for digit in range(1, 10):
            rows = []
            for row in range(9):
                if digit in notations[row][col]:
                    rows.append(row)
            if len(rows) == 3:
                cols = []
                for col2 in range(9):
                    if col2 != col and digit in notations[rows[0]][col2] and digit in notations[rows[1]][col2] and digit in notations[rows[2]][col2]:
                        cols.append(col2)
                if len(cols) == 3:
                    for row1 in range(9):
                        if row1 not in rows and digit in notations[row1][cols[0]] and digit in notations[row1][cols[1]] and digit in notations[row1][cols[2]]:
                            for c in cols:
                                if digit in notations[row1][c]:
                                    notations[row1][c].remove(digit)
                                    print("Removed value %d from (%d, %d)" % (digit, row1, c))
    
    # Check columns
    for digit in range(1, 10):
        candidates = []
        for col in range(9):
            rows = [row for row in range(9) if digit in notations[row][col]]
            if len(rows) >= 2 and len(rows) <= 3:
                candidates.append((col, rows))
        for i in range(len(candidates)):
            for j in range(i+1, len(candidates)):
                for k in range(j+1, len(candidates)):
                    cols = [candidates[i][0], candidates[j][0], candidates[k][0]]
                    rows = sorted(set(candidates[i][1] + candidates[j][1] + candidates[k][1]))
                    if len(rows) == 3:
                        #cells = [(row, col) for row in rows for col in cols]
                        if len(set(notations[row][col]) & set([digit])) == 3:
                            for r in range(9):
                                if r not in rows:
                                    if digit in notations[r][cols[0]]:
                                        notations[r][cols[0]].remove(digit)
                                        print("Removed value %d from (%d, %d)" % (digit, r, cols[0]))
                                    if digit in notations[r][cols[1]]:
                                        notations[r][cols[1]].remove(digit)
                                        print("Removed value %d from (%d, %d)" % (digit, r, cols[1]))
                                    if digit in notations[r][cols[2]]:
                                        notations[r][cols[2]].remove(digit)
                                        print("Removed value %d from (%d, %d)" % (digit, r, cols[2]))
    
    print("No Swordfish")
    
# Function for displaying a message
def display_message(message, duration):
    global label_text, label_color, displayed_message
    
    if not displayed_message:
        displayed_message = True
        label_text = message
        label_color = (255, 0, 0)  # Set the color of the message to red
        label = label_font.render(label_text, True, label_color)
        label_rect = label.get_rect()
        label_rect.center = (label_x, label_y)
        screen.blit(label, label_rect)
        pygame.display.flip()
        pygame.time.wait(duration)
        clear_message()

# Function for clearing a message
def clear_message():
    label_text = " "
    label = label_font.render(label_text, True, label_color)
    label_rect = label.get_rect()
    label_rect.center = (label_x, label_y)
    screen.blit(label, label_rect)
    pygame.display.flip()

# Function for checking Phistomephel's Ring
def PhistomephelsRing():
    global grid
    
    ringIndex = [(2, 2), (2, 3), (2, 4), (2, 5), (2, 6),
                 (3, 6), (4, 6), (5, 6), (6, 6),
                 (6, 5), (6, 4), (6, 3), (6, 2),
                 (5, 2), (4, 2), (3, 2)]
    ring = []
    for i in range(len(ringIndex)):
        ring.append(grid[ringIndex[i][0]][ringIndex[i][1]])
    
    cornerIndex = [(0, 0), (0, 1), (1, 0), (1, 1),
                   (0, 7), (0, 8), (1, 7), (1, 8),
                   (7, 0), (7, 1), (8, 0), (8, 1),
                   (7, 7), (7, 8), (8, 7), (8, 8)]
    
    corners = []
    for i in range(len(cornerIndex)):
        corners.append(grid[cornerIndex[i][0]][cornerIndex[i][1]])
        
    sortedRing = sorted(ring)
    sortedCorners = sorted(corners)
    
    Phistomephels = True
    for i in range(len(ring)):
        if sortedRing[i] != sortedCorners[i]:
            Phistomephels = False
    
    if not Phistomephels:
        return False
    else:
        return ring, corners
    
    
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Set up the window and grid
pygame.init()
size = (560, 560)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Sudoku")
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()
grid_size = 50
margin = 10
label_font = pygame.font.Font(None, 24)
label_x = 280
label_y = 530

# Create the 9x9 grid
grid = [[0 for i in range(9)] for j in range(9)]
notations = [[[] for i in range(9)] for j in range(9)]

displayed_message = False
# Setting seed with current time
random.seed(time.time())

# Set of numbers that each row, column and box should have
nums = [x for x in range(1,10)]

# Amount of unique initial digits
kVal = 9
# Getting random values that will be inserted initially
values = random.sample(nums, k = kVal)
# With the random values as argument, calling the initial values function
initial_values(values)

# Initializing grid so the user can see initial values before it gets solved
init_grid()

# Displays message of Initial values
message = "Initial Values"
display_message(message, 5)

# Matrix that will hold the sudoku notations
notations = [[[] for i in range(9)] for j in range(9)]

# Loop until the user clicks the close button.
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            
    init_grid()

    # Update notations matrix
    make_notations()
    
    # Calling sudoku technique functions
    find_HiddenSingle()
    find_NakedSingle()
    
    # Updating grid so inserted values are visible to user
    init_grid()

    # Update the screen
    pygame.display.flip()

    # Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
pygame.quit()