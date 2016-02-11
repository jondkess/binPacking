# ----------------------------------------------
# CSCI 338, Spring 2016, Bin Packing Assignment
# Author: John Paxton
# Last Modified: January 25, 2016
# ----------------------------------------------
# Modified to include find_naive_solution so that
# driver does not need to be imported.  You may delete
# find_naive_solution from your submission.
# ----------------------------------------------

"""
FIND_NAIVE_SOLUTION:
    Line the the top left corners of the rectangles up along
the y = 0 axis starting with (0,0).
--------------------------------------------------
rectangles: a list of tuples, e.g. [(w1, l1), ... (wn, ln)] where
    w1 = width of rectangle 1,
    l1 = length of rectangle 1, etc.
--------------------------------------------------
RETURNS: a list of tuples that designate the top left corner placement,
         e.g. [(x1, y1), ... (xn, yn)] where
         x1 = top left x coordinate of rectangle 1 placement
         y1 = top left y coordinate of rectangle 1 placement, etc.
"""
import math

#global variables
hasPlaced = []
placement = []
sortedRectangles = []
currentRow = []

def find_naive_solution(rectangles):
    placement = []
    upper_left_x = 0
    upper_left_y = 0

    for rectangle in rectangles:
        width = rectangle[0]
        coordinate = (upper_left_x, upper_left_y)  # make a tuple
        placement.insert(0, coordinate)  # insert tuple at front of list
        upper_left_x = upper_left_x + width

    placement.reverse()  # original order
    return placement


# -----------------------------------------------

"""
FIND_SOLUTION:
    Define this function in bin_packing.py, along with any auxiliary
functions that you need.  Do not change the driver.py file at all.
--------------------------------------------------
rectangles: a list of tuples, e.g. [(w1, l1), ... (wn, ln)] where
    w1 = width of rectangle 1,
    l1 = length of rectangle 1, etc.
--------------------------------------------------
RETURNS: a list of tuples that designate the top left corner placement,
         e.g. [(x1, y1), ... (xn, yn)] where
         x1 = top left x coordinate of rectangle 1 placement
         y1 = top left y coordinate of rectangle 1 placement, etc.
"""


def find_solution(rectangles):
    sortedRectangles = sortRects(rectangles) #Sort rectangles by height greatest to least
    sideLength = findSideLength(rectangles)
    placement = placeBoxes(sortedRectangles, sideLength)
    finalPlacement = removeOrder(placement)
    return finalPlacement
    #return find_naive_solution(rectangles)

def findSideLength(rectangles):
    length = 0
    width = 0
    numRects = len(rectangles)
    rootNumRects = int(math.sqrt(numRects))

    for num in range(0,rootNumRects):
        width = width + rectangles[num][0]
        length = length + rectangles[num][1]

    sideLength = (width + length) / 2
    return sideLength


def sortRects(rectangles):
    i = 0

    for rectangle in rectangles:
        sortedRectangles.insert(0, (rectangle[0], rectangle[1], i))
        i += 1
        sortedRect = sorted(sortedRectangles, key=lambda tup: tup[1], reverse=True)

    return sortedRect

def placeBoxes(sortedRectangles, sideLength):
    yPosition = 0
    j = 0
    hasPlaced = [False for x in range(len(sortedRectangles))]

    while(1):
        xPosition = 0
        currentRow.clear()
        firstRectInRow = j
        while (xPosition <= sideLength):
            if hasPlaced[j] == False:
                coordinate = (xPosition, yPosition, sortedRectangles[j][2])
                xPosition += sortedRectangles[j][0]
                currentRow.append((sortedRectangles[j], xPosition, yPosition))
                placement.insert(0,coordinate)
                hasPlaced[j] = True

            j += 1
            fillRow(currentRow, j)


            if ((len(sortedRectangles) == j)):
                return placement
        yPosition += sortedRectangles[firstRectInRow][1]


def removeOrder(placement):
    finalPlacement = []

    sortedPlacement = sorted(placement, key=lambda tup: tup[2], reverse=True)
    for tuple in sortedPlacement:
        finalPlacement.insert(0, (tuple[0], tuple[1]))
    return finalPlacement

def fillRow(currentRow, numIntoArr):
    for num in range(0, len(currentRow) - 1):
        fillSection(currentRow[num], currentRow[num + 1], numIntoArr)

def fillSection(first, second, numIntoArr):
    sectionWidth = second[0]
    sectionHeight = first[1] - second[1]
    xSectionToFill = sectionWidth
    xFilled = 0

    #while [rectangle for rectangle in sortedRectangles if rectangle[1] < sectionHeight and rectangle[0] < xSectionToFill and hasPlaced[rectangle[2]] == False]:
    fit = [rectangle for rectangle in sortedRectangles in range(numIntoArr, len(sortedRectangles)) if rectangle[1] < sectionHeight and rectangle[0] < xSectionToFill and hasPlaced[rectangle[2]] == False]
    coordinate = (second[3] + xFilled, second[4] + second[1], fit[2])
    placement.insert(0, coordinate)
    hasPlaced[fit[2]] = True
    xSectionToFill -= fit[0]
    xFilled += fit[0]