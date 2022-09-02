import random
from tabulate import tabulate

WEIGHTS = {6: 10000,
            7: 36,
            8: 720,
            9: 360,
            10: 80,
            11: 252,
            12: 108,
            13: 72,
            14: 54,
            15: 180,
            16: 72,
            17: 180,
            18: 119,
            19: 36,
            20: 306,
            21: 1080,
            22: 144,
            23: 1800,
            24: 3600
        }

# Randomly populates the board
# Param arr: A 3x3 2D list of zeros
def populateBoardRand(arr:list):
    stopCond = 0
    possibleChoices = [i for i in range(1, 10)]
    while stopCond < 4:
        choice = random.choice(possibleChoices)
        possibleChoices.remove(choice)
        row = random.randint(0,2)
        col = random.randint(0,2)

        while(arr[row][col] != 0):
            row = random.randint(0,2)
            col = random.randint(0,2)

        arr[row][col] = choice
        stopCond += 1

# Helper function to find the number of zeros in a row, or column
# Param arr: A list of 3 integers
def getNumZeros(arr:list)->int:
    numZeroes = 0
    for el in arr:
        if el == 0:
            numZeroes += 1

    return numZeroes

# Gets the average of the potential earnings of each row or column
# Param arr: A list of 3 integers
# Param available: A list of the 5 integers not used on the board
def getAverage(arr:list, available:list)->int:
    zeros = getNumZeros(arr)
    retMax = 0
    potentialEarnings:int = []

    if zeros == 0:
        for el in arr:
            retMax += el
        return WEIGHTS[retMax]

    elif zeros == 1:
        for el in arr:
            retMax += el
        for pot in available:
            potentialEarnings.append(WEIGHTS[retMax + pot])
        
        return sum(potentialEarnings) // len(potentialEarnings)

    elif zeros == 2:
        retMax = max(arr)
        for i in range(0, len(available) - 1):
            for j in range(i + 1, len(available)):
                potentialEarnings.append(WEIGHTS[retMax + available[i] + available[j]])

        return sum(potentialEarnings) // len(potentialEarnings)
    
    elif zeros == 3:
        for i in range(0, len(available) - 2):
            for j in range(i + 1, len(available) - 1):
                for k in range(j + 1, len(available)):
                    potentialEarnings.append(WEIGHTS[available[i] + available[j] + available[k]])

        return sum(potentialEarnings) // len(potentialEarnings)

# Returns a list of integers not currently in the board
# Param arr: A list of integers already used in the board.
def getAvailable(arr:list)->list:
    available:int = [1,2,3,4,5,6,7,8,9]
    for el in arr:
        if el in arr:
            available.remove(el)

    return available 

# Driver function for finding the averages for each player choice.
# Param arr: The game board. 3x3 2D list
def getResults(arr:list)->list:

    used:int = []
    for row in arr:
        for i in range(3):
            if row[i] != 0:
                used.append(row[i])

    available = getAvailable(used)
    results:tuple[str, int] = []

    for i in range(0, 8):
        tempArr:int = []
        match i:
            case 0:
                results.append(("Row 1", getAverage(arr[0], available)))
            case 1:
                results.append(("Row 2", getAverage(arr[1], available)))
            case 2:
                results.append(("Row 3", getAverage(arr[2], available)))
            case 3:
                for i in range(3):
                    tempArr.append(arr[i][0])
                results.append(("Column One", getAverage(tempArr, available)))
            case 4:
                for i in range(3):
                    tempArr.append(arr[i][1])
                results.append(("Column Two", getAverage(tempArr, available)))
            case 5:
                for i in range(3):
                    tempArr.append(arr[i][2])
                results.append(("Column Three", getAverage(tempArr, available)))
            case 6:
                for i in range(3):
                    tempArr.append(arr[i][i])
                results.append(("Negative Diagonal", getAverage(tempArr, available)))
            case 7:
                for i in range(3):
                    tempArr.append(arr[i][2-i])
                results.append(("Positive Diagonal", getAverage(tempArr, available)))
                
    
    return results

# MAIN FUNCTION.
def main():
    rows, cols = (3,3)
    board = [[0 for _ in range(cols)] for _ in range(rows)]
    populateBoardRand(board)

    for row in board:
        print(row)

    results = getResults(board)
    print(tabulate(results))

    print("The best choice is ", max(results, key=lambda val:val[1]))


if __name__ == "__main__":
    main()