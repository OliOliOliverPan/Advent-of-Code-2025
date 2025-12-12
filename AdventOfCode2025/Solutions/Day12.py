import sys
def day12Q1(shapes, regions):
    sys.setrecursionlimit(10000)

    # All present shapes fits inside a fixed 3×3 grid
    def serialize_shape(grid):
        """Serialize a 3×3 shape into a 9-bit integer mask"""
        v = 0
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                v += (1 << (3*i+j)) * (grid[i][j] == '#')
        return v

    def rotate_grid(grid):
        """Rotate a shape clockwise by 90 degrees"""
        return [list(row) for row in zip(*grid[::-1])]

    def flip_grid(grid):
        """Horizontally flip a shape"""
        return [row[::-1] for row in grid]

    def compute_shape_area(grid):
        """Count number of filled cells ('#') in the shape"""
        return sum(cell == '#' for row in grid for cell in row)

    def generate_orientations(grid):
        """Generate all unique rotated/flipped versions of a shape"""
        seen = set()
        orientations = []

        for flip_flag in [False, True]:
            g = [row[:] for row in grid]
            if flip_flag:
                g = flip_grid(g)
            for _ in range(4):
                code = serialize_shape(g)
                if code not in seen:
                    seen.add(code)
                    orientations.append(code)
                g = rotate_grid(g)
        return orientations
    
    # -----------------------------------------
    # Grid placement logic
    # -----------------------------------------

    def update_grid(grid, shape_code, i0, j0, op_code, shape_num=1):
        """Attempt to place/remove/check a shape at a given grid position
           op_code = 0 → check only
           op_code = 1 → place shape
           op_code = 2 → remove shape
           Returns True if placement is valid, False otherwise"""
        can_fit = True
        for i in range(3):
            for j in range(3):
                b = (shape_code >> (3*i+j)) & 1
                if b == 1:
                    if op_code == 0 and grid[i0+i][j0+j] != '.':
                        can_fit = False
                    if op_code == 1:
                        grid[i0+i][j0+j] = shape_num
                    if op_code == 2:
                        grid[i0+i][j0+j] = '.'
        return can_fit

    def termination_heuristic(h, w, i0, j0, shapes_remaining, shape_areas):
        """Prune: The remaining free area in the region must be >= the area required by all shapes still unplaced"""
        required_area = sum(shapes_remaining[k] * shape_areas[k] for k in range(len(shapes_remaining)))
        available_area = 3*(h-i0) + h*(w-3-j0)
        return required_area <= available_area

    def backtrack(h, w, i0, j0, shapes_remaining, shape_areas, code_list, grid=None):
        """Try to place all shapes into an h×w region using DFS backtracking"""
        if sum(shapes_remaining) == 0:
            return True
        if j0 >= w-2:
            return False
        if not termination_heuristic(h, w, i0, j0, shapes_remaining, shape_areas):
            return False
        if grid is None:
            grid = [['.']*w for _ in range(h)]

        # Compute next grid cell
        i0_next = (i0 + 1) % (h-2)
        j0_next = j0 + (i0_next == 0)

        # Try placing each shape
        for k in range(len(shapes_remaining)):
            if shapes_remaining[k] == 0:
                continue
            for code in code_list[k]:
                if not update_grid(grid, code, i0, j0, 0):
                    continue
                shapes_remaining[k] -= 1
                update_grid(grid, code, i0, j0, 1, k+1)
                if backtrack(h, w, i0_next, j0_next, shapes_remaining, shape_areas, code_list, grid):
                    return True
                shapes_remaining[k] += 1
                update_grid(grid, code, i0, j0, 2)

        return backtrack(h, w, i0_next, j0_next, shapes_remaining, shape_areas, code_list, grid)

    # -----------------------------------------
    # Preprocess shapes
    # -----------------------------------------
    code_list = []
    shape_areas = []
    for idx in sorted(shapes.keys()):
        grid = [list(row) for row in shapes[idx]]
        shape_areas.append(compute_shape_area(grid))
        code_set = set(generate_orientations(grid))
        code_list.append(list(code_set))

    # -----------------------------------------
    # Evaluate each region
    # -----------------------------------------
    total = 0
    for w, h, counts in regions:
        if backtrack(h, w, 0, 0, counts[:], shape_areas, code_list):
            total += 1

    return total




if __name__ == "__main__":
    shapes = {}
    regions = []

    with open("Inputs/Day12Input.txt", "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]

    i = 0
    n = len(lines)

    # --- Parse shapes ---
    while i < n:
        line = lines[i].strip()

        if ":" in line and "x" in line.split(":")[0]:
            break

        if line == "":
            i += 1
            continue

        if line.endswith(":") and line[:-1].isdigit():
            idx = int(line[:-1])
            i += 1
            shape = []

            while i < n and lines[i].strip() != "":
                if lines[i].strip().endswith(":") and lines[i].strip()[:-1].isdigit():
                    break

                shape.append(lines[i])
                i += 1

            shapes[idx] = shape

        else:
            i += 1

    # --- Parse regions ---
    while i < n:
        line = lines[i].strip()
        i += 1
        if not line:
            continue

        if ":" in line:
            area, nums = line.split(":")
            w, h = map(int, area.split("x"))
            counts = list(map(int, nums.split()))
            regions.append((w, h, counts))
    
    result_part_one = day12Q1(shapes, regions)
    print("Result for part one: " + str(result_part_one))