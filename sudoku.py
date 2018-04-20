#!/usr/bin/python3

# testing

import sys
# defaultdict creates empty values in dict to avoid "missing" errors
from collections import defaultdict


# TODO
def usage():
    print('Usage: '+ sys.argv[0]+ ' manual or filename')
    print('Where:  manual      means manually enter a puzzle')
    print('        filename    is the name of a stored puzzle')
    return

#-------------------------------------------------------------
# Set default static values for mapping boxes and cells
def init_defaults():

    # box[row][col] = box-number
    box = defaultdict(dict) # define dict of dict (i.e. 2 levels)
    for x in [ 1, 2, 3 ]:
        box[x][1] = box[x][2] = box[x][3] = 1
        box[x][4] = box[x][5] = box[x][6] = 2
        box[x][7] = box[x][8] = box[x][9] = 3
    for x in [ 4, 5, 6 ]:
        box[x][1] = box[x][2] = box[x][3] = 4
        box[x][4] = box[x][5] = box[x][6] = 5
        box[x][7] = box[x][8] = box[x][9] = 6
    for x in [ 7, 8, 9 ]:
        box[x][1] = box[x][2] = box[x][3] = 7
        box[x][4] = box[x][5] = box[x][6] = 8
        box[x][7] = box[x][8] = box[x][9] = 9

    # cells[box-number] = list of list of row,col in that box
    cells = {}  # define empty list
    cells[1] = [ [1,1], [1,2], [1,3], [2,1], [2,2], [2,3], [3,1], [3,2], [3,3] ]
    cells[2] = [ [1,4], [1,5], [1,6], [2,4], [2,5], [2,6], [3,4], [3,5], [3,6] ]
    cells[3] = [ [1,7], [1,8], [1,9], [2,7], [2,8], [2,9], [3,7], [3,8], [3,9] ]
    cells[4] = [ [4,1], [4,2], [4,3], [5,1], [5,2], [5,3], [6,1], [6,2], [6,3] ]
    cells[5] = [ [4,4], [4,5], [4,6], [5,4], [5,5], [5,6], [6,4], [6,5], [6,6] ]
    cells[6] = [ [4,7], [4,8], [4,9], [5,7], [5,8], [5,9], [6,7], [6,8], [6,9] ]
    cells[7] = [ [7,1], [7,2], [7,3], [8,1], [8,2], [8,3], [9,1], [9,2], [9,3] ]
    cells[8] = [ [7,4], [7,5], [7,6], [8,4], [8,5], [8,6], [9,4], [9,5], [9,6] ]
    cells[9] = [ [7,7], [7,8], [7,9], [8,7], [8,8], [8,9], [9,7], [9,8], [9,9] ]

    return(box, cells)

#-------------------------------------------------------------
# Create hash of all possible values for each cell
def init_possible():

    # define 3-level dictionary of integer values
    poss = defaultdict( lambda: defaultdict(lambda: defaultdict( int )))
    for row in range(1, 10):
        for col in range(1, 10):
            for num in range(1, 10):
                poss[row][col][num] = 1

    return(poss)


#-------------------------------------------------------------
# Print the grid with either "possible" values, or answers
def print_grid(answers, possible, title):

    if possible == '':
        horizontal = '+'.join(('-'*6, '-'*6, '-'*6))
        kind = 'ans'
    else:
        horizontal = '+'.join(('-'*30, '-'*30, '-'*30))
        kind = 'pos'

    print()
    print(title)
    print()
    for row in range(1, 10):
        for col in range(1, 10):
            if kind == 'pos':
                # Print possible values
                poss = ''
                for num in range(1, 10):
                    if possible[row][col][num] == 1:
                        poss += str(num)
                if poss == '':
                    # no possibles, so print answer
                    poss = '-'+str(answers[row][col])+'-'
                print('{:10}'.format(poss), end='')
            else:
                # Print just answers
                num = answers[row][col]
                print('{:2}'.format(num), end='')
            if col == 3 or col == 6:
                print('|', end='')
        print()
        if row == 3 or row == 6:
            print(horizontal)
    print()
    return

#-------------------------------------------------------------
# Get input values from wherever
def get_puzzle(source):

    # Puzzle input is stored as a list of 9 rows, each with 9 characters
    # Assumes zero and space both mean an empty value
    puzzle = []

    if source == 'manual':
        print()
        print('Enter nine ines each with nine digits or spaces')
        print('Use zero or space to indicate an epmpty cell')
        savefile = input('Save data in file (optional): ')
        if savefile != '':
            file_obj = open(savefile, 'w')
        for row in range(1, 10):
            aline = input('Row '+str(row)+': ')
            aline = aline[0:10]     # only first 9 chars
            puzzle.append(aline)
            if savefile != '':
                file_obj.write(aline+"\n")
        if savefile != '':
            file_obj.close()
    elif source == 'test':
        puzzle.append('060090400')
        puzzle.append('000007080')
        puzzle.append('000260100')
        puzzle.append('020000005')
        puzzle.append('907504208')
        puzzle.append('400000030')
        puzzle.append('005081000')
        puzzle.append('040300000')
        puzzle.append('001020070')
    else:
        # Add default extension
        if '.' not in source:
            source = source+'.txt'
        try:
            file_obj = open(source, 'r')
        except IOError as err:
            print('Error opening '+source, err)
            sys.exit()
        puzzle = file_obj.readlines()

    return (puzzle)

#-------------------------------------------------------------
# Create initial answers grid based on the input list
def add_input(possible, input_list):

    answers = defaultdict(lambda: defaultdict( int ))
    for row in range(1, 10):
        for col in range(1, 10):
            num = int(input_list[row-1][col-1])
            if num == 0:
                answers[row][col] = ' '
            else:
                set_value(answers, possible, row, col, num, '')

    return (answers)

#-------------------------------------------------------------
# Assign an answer to the grid, and remove the related possibilties
def set_value(answers, possible, row, col, num, method):

    # Store answer
    answers[row][col] = num
    if show_detail == 1:
        print('SET VALUE: {} at row {}, col {}'.format(num, row, col))

    # Clear answer from possibilities in this row, column, and cell
    for xx in range(1, 10):
        #print('Clear A {},{} = {}'.format(row, xx, num))
        #print('Clear B {},{} = {}'.format(xx, col, num))
        #print('BEFORE: {} for id {}'.format(possible[row][xx][num], id(possible)))
        possible[xx][col][num] = 0  # all rows for this col
        possible[row][xx][num] = 0  # all cols for this row
        possible[row][col][xx] = 0  # all possible for this cell
        #print(' AFTER: {} for id {}'.format(possible[row][xx][num], id(possible)))

    #print_grid('pos', answers, possible, 'Possible A B')

    # Clear answer from possibilities in this box
    boxnum = which_box[row][col]
    for xx in box_cells[boxnum]:
        possible[xx[0]][xx[1]][num] = 0
        #print('Clear C box={} {},{} = {}'.format(boxnum, xx[0], xx[1], num))

    #print_grid('pos', answers, possible, 'Possible C')

    return

#-------------------------------------------------------------
# Methods which look for answers
#-------------------------------------------------------------

#-------------------------------------------------------------
# For each cell in the grid, if only one possible number, then set it
def check_cells(answers, possible):

    found = 0
    for row in range(1, 10):
        for col in range(1, 10):
            cnt_possible = 0
            for num in range(1, 10):
                if possible[row][col][num] == 1:
                    only_num = num
                    cnt_possible += 1
            # If num is only possible value, then found an answer
            if cnt_possible == 1:
                set_value(answers, possible, row, col, only_num, 'check_cells')
                found += 1

    if show_detail == 1:
        print('check cells found '+str(found))
    return found


#-------------------------------------------------------------
# Check if each number is only possible once in each column
def check_cols(answers, possible):

    found = 0
    for col in range(1, 10):
        for num in range(1, 10):
            cnt_possible = 0
            for row in range(1, 10):
                if possible[row][col][num] == 1:
                    only_row = row
                    cnt_possible += 1
            # If num is only possible value, then found an answer
            if cnt_possible == 1:
                set_value(answers, possible, only_row, col, num, 'check_cols')
                found += 1

    if show_detail == 1:
        print('check cols found '+str(found))
    return found


#-------------------------------------------------------------
# Check if each number is only possible once in each row
def check_rows(answers, possible):

    found = 0
    for row in range(1, 10):
        for num in range(1, 10):
            cnt_possible = 0
            for col in range(1, 10):
                if possible[row][col][num] == 1:
                    only_col = col
                    cnt_possible += 1
            # If num is only possible value, then found an answer
            if cnt_possible == 1:
                set_value(answers, possible, row, only_col, num, 'check_rows')
                found += 1
    if show_detail == 1:
        print('check rows found '+str(found))
    return found

#-------------------------------------------------------------
# Check if each number is only possible once in each box
def check_boxes(answers, possible):

    found = 0
    for boxnum in range(1, 10):
        for num in range(1, 10):
            cnt_possible = 0
            for xx in box_cells[boxnum]:
                if possible[xx[0]][xx[1]][num] == 1:
                    only_row = xx[0]
                    only_col = xx[1]
                    cnt_possible += 1
            # If num is only possible value, then found an answer
            if cnt_possible == 1:
                set_value(answers, possible, only_row, only_col, num, 'check_boxes')
                found += 1
    if show_detail == 1:
        print('check boxes found '+str(found))
    return found


#-------------------------------------------------------------
# Check for two twins of possible values
# Look in rows, columns, boxes
# Remove the twins from other possibilities
def check_twins(possible):

    found = 0

    # Check the rows
    for row in range(1, 10):
        have_twin_at = {}  # dict
        for col in range(1, 10):
            found += check_twins_specific(possible, have_twin_at, row, col, 'C')

    # Check the columns
    for col in range(1, 10):
        have_twin_at = {}  # dict
        for row in range(1, 10):
            found += check_twins_specific(possible, have_twin_at, row, col, 'R')

    if show_detail == 1:
        print('check twins found '+str(found))
    return found


#-------------------------------------------------------------
# Shared logic when checking for twins by rows or by columns
# 'have_twin_at' is row or column of previously found twin we're trying to match
# possible[R][C]['twin'] is flag indicating this is a twin
def check_twins_specific(possible, have_twin_at, row, col, check_by):

    found_here = 0
    if possible[row][col]['twin'] == 0:
        # Determine string of possible values for this cell
        twin = ''
        for num in range(1, 10):
            if possible[row][col][num] == 1:
                twin += str(num)

        # Only care if found one twin of possibilities
        if len(twin) == 2:
            if twin in have_twin_at:
                # Found the second twin!
                possible[row][col]['twin'] = 1
                if check_by == 'C':
                    possible[row][have_twin_at[twin]]['twin'] = 1
                    if show_detail == 1:
                        print('TWIN: {} in {} {} at {} {} and {}'.format(twin,'row',row,'cols',have_twin_at[twin],col))
                else:
                    possible[have_twin_at[twin]][col]['twin'] = 1
                    if show_detail == 1:
                        print('TWIN: {} in {} {} at {} {} and {}'.format(twin,'col',col,'rows',have_twin_at[twin],row))
                found_here += 1
                # For each col in this row (or row in this col),
                # clear the twins from other possibilities
                for xx in range(1, 10):
                    if xx != have_twin_at[twin]:
                        if check_by == 'C':
                            if xx != col:
                                possible[row][xx][twin[0]] = 0
                                possible[row][xx][twin[1]] = 0
                        else:
                            if xx != row:
                                possible[xx][col][twin[0]] = 0
                                possible[xx][col][twin[1]] = 0
            else:
                # Found first instance of this twin
                if check_by == 'C':
                    have_twin_at[twin] = col
                else:
                    have_twin_at[twin] = row

    return found_here


#-------------------------------------------------------------
def main():

    if len(sys.argv) == 1:
        usage()
        sys.exit()

    # Initialize static global values
    global show_detail
    global which_box
    global box_cells
    (which_box, box_cells) = init_defaults()
    show_detail = 1

    # Initialize all possible values per cell
    (possible) = init_possible()

    # Input puzzle and place into answer grid
    (input_list) = get_puzzle(sys.argv[1])
    answers = add_input(possible, input_list)

    print_grid(answers, '', 'Initial Answers')
    print_grid(answers, possible, 'Initial Possible')

    # Loop thru rules to look for answers
    found = 1
    while found > 0:
        found = 0
        found += check_cells(answers, possible)
        if show_detail == 1 and found > 0:
            print_grid(answers, possible, 'AFTER check-cells')
            exit
        found += check_rows(answers, possible)
        if show_detail == 1 and found > 0:
            print_grid(answers, possible, 'AFTER check-rows')
        found += check_cols(answers, possible)
        if show_detail == 1 and found > 0:
            print_grid(answers, possible, 'AFTER check-cols')
        found += check_boxes(answers, possible)
        if show_detail == 1 and found > 0:
            print_grid(answers, possible, 'AFTER check-boxes')
        found += check_twins(possible)
        if show_detail == 1 and found > 0:
            print_grid(answers, possible, 'AFTER check-twins')

    print_grid(answers, possible, 'Possible')
    print_grid(answers, '', 'Final Answers')


if __name__ == '__main__':
    main()
