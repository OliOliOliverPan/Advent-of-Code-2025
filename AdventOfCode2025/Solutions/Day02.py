def day02Q1(ranges):
    ans = 0
    for start, end in ranges:
        for i in range(start, end + 1):
            i_str = str(i)
            n = len(i_str)
            if i_str[:n//2] == i_str[n//2:]:
                ans += i
    return ans

def day02Q2(ranges):
    ans = 0
    for start, end in ranges:
        for i in range(start, end + 1):
            s = str(i)
            for j in range(2, len(s) + 1):
                if len(s) % j == 0 and s[:len(s) // j] * j == s:
                    ans += i
                    break
                            
    return ans


if __name__ == "__main__":
    ranges = []
    with open('Inputs/Day02Input.txt', 'r', encoding='utf-8') as f:
        line = f.read().strip()
        parts = line.split(',')

        for part in parts:
            start, end = map(int, part.split('-'))
            ranges.append((start, end))
    result_part_one = day02Q1(ranges)
    print("Result for part one: " + str(result_part_one))
    result_part_two = day02Q2(ranges)
    print("Result for part two: " + str(result_part_two))