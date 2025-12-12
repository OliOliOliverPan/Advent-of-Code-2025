from collections import deque

def day07Q1(diagram):
    m, n = len(diagram), len(diagram[0])

    sx = sy = None
    for i in range(m):
        for j in range(n):
            if diagram[i][j] == 'S':
                sx, sy = i, j
                break
    
    q = deque()
    q.append((sx, sy))

    visited_starts = {(sx, sy)}

    processed_splitters = set()

    while q:
        x, y = q.popleft()

        nx = x
        while True:
            nx += 1
            if nx >= m:
                break

            cell = diagram[nx][y]

            if cell == '^':
                if (nx, y) not in processed_splitters:
                    processed_splitters.add((nx, y))

                    if y - 1 >= 0 and (nx, y - 1) not in visited_starts:
                        visited_starts.add((nx, y - 1))
                        q.append((nx, y - 1))
                    
                    if y + 1 < n and (nx, y + 1) not in visited_starts:
                        visited_starts.add((nx, y + 1))
                        q.append((nx, y + 1))
                
                break
            
            continue

    return len(processed_splitters)

def day07Q2(diagram):
    m, n = len(diagram), len(diagram[0])

    for i in range(m):
        for j in range(n):
            if diagram[i][j] == 'S':
                sx, sy = i, j
                break
    
    dp = [[0]*n for _ in range(m)]
    dp[sx][sy] = 1

    for row in range(sx, m-1):
        for col in range(n):
            if dp[row][col] == 0:
                continue
            cell = diagram[row+1][col]
        
            if cell == '^':
                if col - 1 >= 0:
                    dp[row+1][col-1] += dp[row][col]
                if col + 1 < n:
                    dp[row+1][col+1] += dp[row][col]
            
            else:
                dp[row+1][col] += dp[row][col]
    
    return sum(dp[m-1])
                


if __name__ == "__main__":
    lines  = []
    with open('Inputs/Day07Input.txt', 'r', encoding='utf-8') as f:
        for line in f:
            lines.append(list(line.strip()))
    result_part_one = day07Q1(lines)
    print("Result for part one: " + str(result_part_one))
    result_part_two = day07Q2(lines)
    print("Result for part two: " + str(result_part_two))