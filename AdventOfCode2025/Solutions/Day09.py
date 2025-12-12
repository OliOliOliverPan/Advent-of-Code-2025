from itertools import combinations
from collections import deque
def day09Q1(tiles):
    combos = list(combinations(tiles, 2))
    return max((abs(a[0]-b[0])+1)*(abs(a[1]-b[1])+1) for a,b in combos)
       
    
def day09Q2(tiles):

    valid_x_vals = sorted(set(x for x,y in tiles))
    valid_y_vals = sorted(set(y for x,y in tiles))

    x_map, x_back_map = {}, {}
    last_x, next_x = None, 0
    for x in valid_x_vals:
        if last_x is not None:
            x_back_map[next_x] = x - last_x - 1
            next_x += 1
        x_map[x] = next_x
        x_back_map[next_x] = 1
        next_x += 1
        last_x = x

    y_map, y_back_map = {}, {}
    last_y, next_y = None, 0
    for y in valid_y_vals:
        if last_y is not None:
            y_back_map[next_y] = y - last_y - 1
            next_y += 1
        y_map[y] = next_y
        y_back_map[next_y] = 1
        next_y += 1
        last_y = y

    vertices = [(x_map[x], y_map[y]) for x,y in tiles]

    vert_edges = []
    valid_tiles = set()

    for (x, y), (x2, y2) in zip(vertices, vertices[1:] + vertices[:1]):
        if x == x2:
            edge_dir = (y < y2)
            vert_edges.append((x, min(y, y2), max(y, y2), edge_dir))
        else:
            assert y == y2
            for x3 in range(min(x, x2), max(x, x2)+1):
                valid_tiles.add((x3, y))

    minx = min(x for x,y in vertices)
    maxx = max(x for x,y in vertices)
    miny = min(y for x,y in vertices)
    maxy = max(y for x,y in vertices)

    for y in range(miny, maxy+1):
        included = False
        last_edge_dir = None
        for x in range(minx, maxx+1):
            hit_edge = False
            for ex, ey1, ey2, edge_dir in vert_edges:
                if x == ex and ey1 <= y <= ey2:
                    if edge_dir != last_edge_dir:
                        hit_edge = True
                        last_edge_dir = edge_dir
                        break
            if hit_edge:
                valid_tiles.add((x, y))
                included = not included
                continue
            if included:
                valid_tiles.add((x, y))

    def make_area_set(c1, c2):
        x1, y1 = c1
        x2, y2 = c2
        if x1 > x2: x1, x2 = x2, x1
        if y1 > y2: y1, y2 = y2, y1
        return set((x, y) for x in range(x1, x2+1) for y in range(y1, y2+1))

    def calc_area(area_set):
        area = 0
        for x, y in area_set:
            area += x_back_map[x] * y_back_map[y]
        return area

    answer = 0
    n = len(vertices)
    for i, c1 in enumerate(vertices):
        for c2 in vertices[i+1:]:
            x1, y1 = c1
            x2, y2 = c2
            if x1 > x2: x1, x2 = x2, x1
            if y1 > y2: y1, y2 = y2, y1

            valid = True
            for x3, y3 in vertices:
                if x1 < x3 < x2 and y1 < y3 < y2:
                    valid = False
                    break
            if not valid:
                continue

            area_set = make_area_set(c1, c2)
            if len(area_set) == len(area_set & valid_tiles):
                area2 = calc_area(area_set)
                answer = max(answer, area2)

    return answer

    



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