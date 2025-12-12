def day05Q1(ranges, numbers):
    ans = 0
    for num in numbers:   
        if any(r[0] <= num <= r[1] for r in ranges):
            ans += 1
    return ans

def day05Q2(ranges):
    ranges.sort(key=lambda x: x[0])
    distinct = [ranges[0]]
    for i in range(1, len(ranges)):
        s, e = ranges[i][0], ranges[i][1]
        _, last_e = distinct[-1]

        if s <= last_e:
            distinct[-1][1] = max(last_e, e)
        else:
            distinct.append([s,e])
    return sum(e-s+1 for s, e in distinct)



if __name__ == "__main__":
    ranges = []
    numbers = []
    with open('Inputs/Day05Input.txt', 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines()]

    split_index = lines.index("")
    range_lines = lines[:split_index]
    number_lines = lines[split_index + 1:]

    for r in range_lines:
        start, end = map(int, r.split('-'))
        ranges.append([start, end])

    for n in number_lines:
        numbers.append(int(n))
    
    result_part_one = day05Q1(ranges, numbers)
    print("Result for part one: " + str(result_part_one))
    result_part_two = day05Q2(ranges)
    print("Result for part two: " + str(result_part_two))