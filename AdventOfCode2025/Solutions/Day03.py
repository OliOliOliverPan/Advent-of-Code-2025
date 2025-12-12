def day03Q1(banks):
    ans = 0
    for bank in banks:
        n = len(bank)
        max_num = 0
        max_first_digit = int(bank[0])
        for i in range(n-1):
            if int(bank[i]) > max_first_digit:
                max_first_digit = int(bank[i])
            max_second_digit = max(int(char) for char in bank[i+1:])
            v = max_first_digit * 10 + max_second_digit
            if v > max_num:
                max_num = v
        ans += max_num
    
    return ans

def day03Q2(banks):
    ans = 0
    for bank in banks:
        v = 0
        n = len(bank)
        start = 0
        for i in range(12):
            end = n - (12 - (i+1)) - 1
            max_digit = -1
            max_pos = -1
            for j in range(start, end + 1):
                d = int(bank[j])
                if d > max_digit:
                    max_digit = d
                    max_pos = j
                    if max_digit == 9:
                        break
            v = v * 10 + max_digit
            start = max_pos + 1
        ans += v
    return ans
    




if __name__ == "__main__":
    lines  = []
    with open('Inputs/Day03Input.txt', 'r', encoding='utf-8') as f:
        for line in f:
            lines.append(line.strip())
    result_part_one = day03Q1(lines)
    print("Result for part one: " + str(result_part_one))
    result_part_two = day03Q2(lines)
    print("Result for part two: " + str(result_part_two))