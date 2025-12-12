def day01Q1(instructions):
    ans = 0
    start = 50
    for instruction in instructions:
        v = int(instruction[1:]) % 100
        if instruction[0] == 'L':
            if v > start:
                start = (start - v) % 100
            else:
                start -= v
        elif instruction[0] == 'R':
            start = (start + v) % 100
        if start == 0:
            ans += 1

    return ans

def day01Q2(instructions):
    ans = 0
    start = 50
    for instruction in instructions:
        v = int(instruction[1:])

        if instruction[0] == 'L':
            for i in range(1, v+1):
                if (start - i) % 100 == 0:
                    ans += 1
            start = (start - v) % 100

        elif instruction[0] == 'R':
            for i in range(1, v+1):
                if (start + i) % 100 == 0:
                    ans += 1
            start = (start + v) % 100

    return ans
        



if __name__ == "__main__":
    lines  = []
    with open('Inputs/Day01Input.txt', 'r', encoding='utf-8') as f:
        for line in f:
            lines.append(line.strip())
    result_part_one = day01Q1(lines)
    print("Result for part one: " + str(result_part_one))
    result_part_two = day01Q2(lines)
    print("Result for part two: " + str(result_part_two))