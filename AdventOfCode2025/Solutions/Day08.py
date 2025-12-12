from itertools import combinations
import math

def day08Q1(boxes, connection_limit):

    conjunctions = list(combinations(boxes, 2))
    conjunctions.sort(key=lambda pair: math.dist(pair[0], pair[1]))

    circuit = []
    connections_done = 0

    for a, b in conjunctions:
        if connections_done == connection_limit:
            break

        ca = cb = None
        for c in circuit:
            if a in c:
                ca = c
            if b in c:
                cb = c

        if ca and cb:
            if ca is cb:
                connections_done += 1

            else:
                ca.update(cb)
                circuit.remove(cb)
                connections_done += 1

        elif ca and not cb:
            ca.add(b)
            connections_done += 1

        elif cb and ca is None:
            cb.add(a)
            connections_done += 1

        elif not ca and not cb:
            circuit.append(set([a, b]))
            connections_done += 1


    circuit.sort(key = lambda x: len(x), reverse = True)
    res = 0
    if len(circuit) >= 3:
        top3 = circuit[:3]
        res = math.prod(len(c) for c in top3)
    else:
        res = math.prod(len(c) for c in circuit) * (1 ** (3 - len(circuit)))
    return res


def day08Q2(boxes):

    conjunctions = list(combinations(boxes, 2))
    conjunctions.sort(key=lambda pair: math.dist(pair[0], pair[1]))

    group = {p: i for i, p in enumerate(boxes)}

    for a, b in conjunctions:
        ga, gb = group[a], group[b]

        if ga == gb:
            continue
        
        # Merge gb into ga
        for x in group:
            if group[x] == gb:
                group[x] = ga
        
        # Check whether all boxes are connected within the same circuit
        if len(set(group.values())) == 1:
            return a[0] * b[0] # Obtain the product of X coordinates of the last two boxes




if __name__ == '__main__':
    points = []

    with open("Inputs/Day08Input.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            x, y, z = line.split(",")
            points.append((int(x), int(y), int(z)))
    result_part_one = day08Q1(points, 1000)
    print("Result for part one: " + str(result_part_one))
    result_part_two = day08Q2(points)
    print("Result for part two: " + str(result_part_two))