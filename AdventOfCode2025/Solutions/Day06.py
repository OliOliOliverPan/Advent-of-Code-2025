import math

def day06Q1(rows):
    ans = 0

    operators = rows[-1]
    numbers = rows[:-1]

    # Record the index of the last separator column
    # A separator column is a column where all row entries on that column are spaces
    last_separator = -1

    for i in range(len(operators) + 1):
        is_separator = i == len(operators) or all(numbers[r][i] == ' ' for r in range(len(numbers)))
        if is_separator:
            # Find the operator for the current problem
            operator = ''
            for l in range(last_separator+1, i):
                if operators[l] in "+*":
                    operator = operators[l]
                    break

            # Parse all numbers for the current problem
            problem_numbers = []
            for j in range(len(numbers)):
                num_str = ""
                # Read each row horizontally across numbers' columns to form each number
                for k in range(last_separator + 1, i):
                    if k < len(numbers[j]) and numbers[j][k] != ' ':
                        num_str += numbers[j][k]
                problem_numbers.append(int(num_str))
            if operator == '+':
                ans += sum(problem_numbers)
            elif operator == '*':
                ans += math.prod(problem_numbers)

            # Update the last separator position
            last_separator = i
    return ans


def day06Q2(rows):

    ans = 0

    # The operators line and all lines of numbers are of the same length
    operators = rows[-1]
    numbers = rows[:-1]
    
    # Track the current column we're at
    cur_col = 0

    # Continue until all problems are processed
    while cur_col < len(operators):
        # Skip spaces in operator line to find next operator
        while operators[cur_col] == ' ':
            cur_col += 1

        if cur_col >= len(operators):
            break
        
        # Record the index of the current problem's operator on the operators line
        operator_idx = cur_col

        # Parse numbers for the current problem
        problem_numbers = []

        # Continue moving cur_col until it hits a column of all spaces
        while cur_col < len(operators):
            is_separator = cur_col >= len(operators) or (all(numbers[row][cur_col] == ' ' 
                             for row in range(len(numbers))) and operators[cur_col] == ' ')
            
            if is_separator:
                break
            
            # Concatenate all numbers from the current row to form a number
            num_str = ""
            for row in range(len(numbers)):
                if numbers[row][cur_col] != ' ':
                    num_str += numbers[row][cur_col]
            
            # Add the concatenated number to the current list of numbers for this problem
            problem_numbers.append(int(num_str))
            
            cur_col += 1

        operator = operators[operator_idx]

        if operator == '+':
            ans += sum(problem_numbers)
        elif operator == '*':
            ans += math.prod(problem_numbers)

    return ans



if __name__ == "__main__":
    with open("Inputs/Day06Input.txt") as f:
        rows = [line.rstrip("\n") for line in f]
    result_part_one = day06Q1(rows)
    print("Result for part one: " + str(result_part_one))
    result_part_two = day06Q2(rows)
    print("Result for part two: " + str(result_part_two))