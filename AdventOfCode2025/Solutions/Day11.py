from functools import cache
def day11Q1(lines):
    memo = dict()
    def dfs(node):
        nonlocal memo
        if node == 'out': return 1
        if node in memo.keys():
            return memo[node]
        total = 0
        for nxt in lines.get(node, []):
            total += dfs(nxt)
        memo[node] = total

        return total

    return dfs('you')

def day11Q2(lines):

    @cache
    def dfs(node, seen_fft, seen_dac):
        if node == 'fft':
            seen_fft = True
        if node == 'dac':
            seen_dac = True

        if node == 'out': 
            return 1 if (seen_fft and seen_dac) else 0

        total = 0
        for nxt in lines.get(node, []):
            total += dfs(nxt, seen_fft, seen_dac)

        return total

    return dfs('svr', False, False)


if __name__ == "__main__":
    lines = dict()

    with open("Inputs/Day11Input.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            name, targets = line.split(":")
            name = name.strip()
            targets = targets.strip().split()
            lines[name] = targets
    result_part_one = day11Q1(lines)
    print("Result for part one: " + str(result_part_one))
    result_part_two = day11Q2(lines)
    print("Result for part two: " + str(result_part_two))