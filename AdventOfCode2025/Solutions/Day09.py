from itertools import combinations
from collections import deque
def day09Q1(tiles):
    combos = list(combinations(tiles, 2))
    return max((abs(a[0]-b[0])+1)*(abs(a[1]-b[1])+1) for a,b in combos)
       
    

def day09Q2(tiles):
    # Extract and sort unique x and y coordinates of red tiles
    xs = sorted({x for x, _ in tiles})
    ys = sorted({y for _, y in tiles})

    grid = [[0] * (len(ys) * 2 - 1) for _ in range(len(xs) * 2 - 1)]

    # Draw the red-green loop by filling all cells along each segment
    # Consecutive red tiles are connected by straight green paths
    for (x1, y1), (x2, y2) in zip(tiles, tiles[1:] + tiles[:1]):
        cx1, cx2 = sorted([xs.index(x1) * 2, xs.index(x2) * 2])
        cy1, cy2 = sorted([ys.index(y1) * 2, ys.index(y2) * 2])
        for cx in range(cx1, cx2 + 1):
            for cy in range(cy1, cy2 + 1):
                grid[cx][cy] = 1
    
    # Flood fill from outside the grid
    # Cells reachable from outside the grid are neither red nor green
    outside = {(-1, -1)}
    queue = deque(outside)

    while len(queue) > 0:
        tx, ty = queue.popleft()
        for nx, ny in [(tx - 1, ty), (tx + 1, ty ), (tx, ty - 1), (tx, ty + 1)]:
            if nx < -1 or ny < -1 or nx > len(grid) or ny > len(grid[0]):
                continue
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] == 1:
                continue
            if (nx, ny) in outside: 
                continue
            outside.add((nx, ny))
            queue.append((nx, ny))

    # Any tile that is not reachable from outside the grid is either green or red
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if (x, y) not in outside:
                grid[x][y] = 1
    
    # Build prefix sum array for fast rectangle queries
    psa = [[0] * len(row) for row in grid]
    for x in range(len(psa)):
        for y in range(len(psa[0])):
            left = psa[x - 1][y] if x > 0 else 0
            top = psa[x][y - 1] if y > 0 else 0
            topleft = psa[x - 1][y - 1] if x > 0 and y > 0 else 0
            psa[x][y] = left + top - topleft + grid[x][y]
    
    # Check if rectangle defined by two red tiles is valid
    def valid(x1, y1, x2, y2):
        cx1, cx2 = sorted([xs.index(x1) * 2, xs.index(x2) * 2])
        cy1, cy2 = sorted([ys.index(y1) * 2, ys.index(y2) * 2])
        left = psa[cx1 - 1][cy2] if cx1 > 0 else 0
        top = psa[cx2][cy1 - 1] if cy1 > 0 else 0
        topleft = psa[cx1 - 1][cy1 - 1] if cx1 > 0 and cy1 > 0 else 0

        count = psa[cx2][cy2] - left - top + topleft
        return count == (cx2 - cx1 + 1) * (cy2 - cy1 + 1)

    # Enumerate all red-tile pairs as opposite corners and find the largest possible rectangle area
    ans = max([(abs(x1 - x2) + 1) * (abs(y1 - y2) + 1) for i, (x1, y1) in enumerate(tiles) for x2, y2 in tiles[:i] if valid(x1, y1, x2, y2)])
    return ans




if __name__ == "__main__":
    points = []

    with open("Inputs/Day09Input.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            x, y = line.split(",")
            points.append((int(x), int(y)))
    result_part_one = day09Q1(points)
    print("Result for part one: " + str(result_part_one))
    result_part_two = day09Q2(points)
    print("Result for part two: " + str(result_part_two))