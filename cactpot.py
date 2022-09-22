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
def populate_board_rand(arr: list[list[int]]) -> list[list[int]]:
    stop_cond: int = 0
    possible_choices: list = [i for i in range(1, 10)]
    while stop_cond < 4:
        choice = random.choice(possible_choices)
        possible_choices.remove(choice)
        row = random.randint(0, 2)
        col = random.randint(0, 2)

        while arr[row][col] != 0:
            row = random.randint(0, 2)
            col = random.randint(0, 2)

        arr[row][col] = choice
        stop_cond += 1

    return arr

# Runs through the board asking the user for the value of each location
# Param arr: The 3x3 gameboard populated with zeroes. 
def populate_custom_board(arr: list[list[int]]) -> list[list[int]]:
    count: int = 0
    print("As the program goes, please enter in a zero for a non entry.")
    print("Otherwise, enter the number you have in that location.")

    used_nums: list = []
    for indexR, row in enumerate(arr):
        for indexC, entry in enumerate(row):
            print(f"Please enter a number for row {indexR + 1} col {indexC + 1}")
            user_input = int(input())
            while user_input in used_nums:
                print("You have already used that num")
                user_input = int(input())

            if user_input != 0:
                count += 1
                used_nums.append(user_input)

            arr[indexR][indexC] = user_input
            if count == 4:
                return arr

    return arr


# Helper function to find the number of zeros in a row, or column
# Param arr: A list of 3 integers
def get_num_zeroes(arr: list) -> int:
    num_zeroes = 0
    for el in arr:
        if el == 0:
            num_zeroes += 1

    return num_zeroes


# Gets the average of the potential earnings of each row or column
# Param arr: A list of 3 integers
# Param available: A list of the 5 integers not used on the board
def get_average(arr: list, available: list) -> int:
    zeros = get_num_zeroes(arr)
    ret_max = 0
    potential_earnings: list[int] = []

    if zeros == 0:
        for el in arr:
            ret_max += el
        return WEIGHTS[ret_max]

    elif zeros == 1:
        for el in arr:
            ret_max += el
        for pot in available:
            potential_earnings.append(WEIGHTS[ret_max + pot])

        return sum(potential_earnings) // len(potential_earnings)

    elif zeros == 2:
        ret_max = max(arr)
        for i in range(0, len(available) - 1):
            for j in range(i + 1, len(available)):
                potential_earnings.append(WEIGHTS[ret_max + available[i] + available[j]])

        return sum(potential_earnings) // len(potential_earnings)

    elif zeros == 3:
        for i in range(0, len(available) - 2):
            for j in range(i + 1, len(available) - 1):
                for k in range(j + 1, len(available)):
                    potential_earnings.append(WEIGHTS[available[i] + available[j] + available[k]])

        return sum(potential_earnings) // len(potential_earnings)

    return 0


# Returns a list of integers not currently in the board
# Param arr: A list of integers already used in the board.
def get_available(arr: list) -> list:
    available: list[int] = [i for i in range(1, 10)]
    for el in arr:
        if el in arr:
            available.remove(el)

    return available


# Driver function for finding the averages for each player choice.
# Param arr: The game board. 3x3 2D list
def get_results(arr: list) -> list:
    used: list[int] = []
    for row in arr:
        for i in range(3):
            if row[i] != 0:
                used.append(row[i])

    available = get_available(used)
    results: list[tuple[str, int]] = []

    for i in range(0, 8):
        temp_arr: list[int] = []
        match i:
            case 0:
                results.append(("Row 1", get_average(arr[0], available)))
            case 1:
                results.append(("Row 2", get_average(arr[1], available)))
            case 2:
                results.append(("Row 3", get_average(arr[2], available)))
            case 3:
                for j in range(3):
                    temp_arr.append(arr[j][0])
                results.append(("Column One", get_average(temp_arr, available)))
            case 4:
                for j in range(3):
                    temp_arr.append(arr[j][1])
                results.append(("Column Two", get_average(temp_arr, available)))
            case 5:
                for j in range(3):
                    temp_arr.append(arr[j][2])
                results.append(("Column Three", get_average(temp_arr, available)))
            case 6:
                for j in range(3):
                    temp_arr.append(arr[j][j])
                results.append(("Negative Diagonal", get_average(temp_arr, available)))
            case 7:
                for j in range(3):
                    temp_arr.append(arr[j][2 - j])
                results.append(("Positive Diagonal", get_average(temp_arr, available)))

    return results


# MAIN FUNCTION.
def main():
    rows, cols = (3, 3)
    board = [[0 for _ in range(cols)] for _ in range(rows)]
    # populateBoardRand(board)

    running: bool = True

    while running:
        board = [[0 for _ in range(cols)] for _ in range(rows)]
        print("Would you like to generate a random board or do you want to enter a custom board?")
        print("1.) Custom Board\n2.) Random Board\n")

        user_choice = input()
        if user_choice == "1":
            board = populate_custom_board(board)
        elif user_choice == "2":
            board = populate_board_rand(board)
        else:
            print("That's not a valid option. Try again")
            continue

        running = False

    for row in board:
        print(row)

    results = get_results(board)
    print(tabulate(results))

    print("The best choice is ", max(results, key=lambda val: val[1]))


if __name__ == "__main__":
    main()
