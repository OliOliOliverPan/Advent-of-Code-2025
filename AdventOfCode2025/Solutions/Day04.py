def canBeRemoved(g, i, j):
    m, n = len(g), len(g[0])
    DIR = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]
    cnt  = 0
    
    for dx, dy in DIR:
        cx, cy = i+dx, j+dy
        if 0 <= cx < m and 0 <= cy < n:
            if g[cx][cy] == '@':
                cnt += 1
    return cnt < 4


def day04Q1(grid):
    ans = 0
    m, n = len(grid), len(grid[0])
    for i in range(m):
        for j in range(n):
            if grid[i][j] == '@' and canBeRemoved(grid, i, j):  
                ans += 1
    return ans


def day04Q2(grid):
    ans = 0
    m, n = len(grid), len(grid[0])

    while True:
        toBeRemoved = [(x,y) for x in range(m) for y in range(n) if grid[x][y] == '@' and canBeRemoved(grid, x, y)]
        if not toBeRemoved:
            break
        
        for o, p in toBeRemoved:
            grid[o][p] = '.'
        ans += len(toBeRemoved)
    
    return ans



if __name__ == "__main__":
    lines  = []
    with open('Inputs/Day04Input.txt', 'r', encoding='utf-8') as f:
        for line in f:
            lines.append(list(line.strip()))
    result_part_one = day04Q1(lines)
    print("Result for part one: " + str(result_part_one))
    result_part_two = day04Q2(lines)
    print("Result for part two: " + str(result_part_two))