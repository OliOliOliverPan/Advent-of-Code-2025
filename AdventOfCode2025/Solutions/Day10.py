import z3

def day10Q1(manuals):
    ans = 0
    for ln in manuals:
        # --- Parse light diagram, button wiring schematics for each machine ---
        parts = ln.strip().split()
        pattern, *buttons, _ = parts

        pattern = pattern[1:-1]

        buttons = [
            set(map(int, btn[1:-1].split(','))) 
            for btn in buttons
        ]


        # --- Set up Z3 optimization problem ---
        s = z3.Optimize()
        # Record the number of presses of every button in a list
        presses = [z3.Int(f"press{i}") for i in range(len(buttons))]

        # Constraint: The number of presses for each button >= 0
        for p in presses:
            s.add(p >= 0)

        # Constraint: Each light's final state must match the light diagram
        # The light is on if the sum of the presses of buttons that toggle it is odd, off if even
        for i in range(len(pattern)):
            controlling_buttons = [presses[j] for j, btn in enumerate(buttons) if i in btn]
            if pattern[i] == '#':
                s.add(sum(controlling_buttons) % 2 == 1)
            else:
                s.add(sum(controlling_buttons) % 2 == 0)

        # Minimize the total number of button presses for the current machine
        s.minimize(sum(presses))

        assert s.check() == z3.sat
        m = s.model()
        ans += sum(m[p].as_long() for p in presses)

    return ans

def day10Q2(manuals):
    total = 0
    for ln in manuals:
        # --- Parse button wiring schematics, joltage requirements for each machine ---
        parts = ln.strip().split()
        _, *buttons, joltages = parts

        buttons = [
            set(map(int, btn[1:-1].split(',')))
            for btn in buttons
        ]

        joltages = list(map(int, joltages[1:-1].split(',')))
        n = len(joltages)
        m = len(buttons)

        # --- Set up Z3 optimization problem ---
        s = z3.Optimize()
        # Record the number of presses of every button in a list
        presses = [z3.Int(f"p{i}") for i in range(m)]

        # Constraint: The number of presses for each button >= 0
        for p in presses:
            s.add(p >= 0)

        # Constraint: Each joltage counter must reach its target value specified in joltage requirements
        # This means that the sum of presses of all buttons that affect the ith counter must equal joltages[i]
        for i in range(n):
            controlling = [presses[j] for j, btn in enumerate(buttons) if i in btn]
            s.add(sum(controlling) == joltages[i])

        # Minimize the total presses of all buttons for the current machine
        s.minimize(sum(presses))

        assert s.check() == z3.sat
        m_ = s.model()
        total += sum(m_[p].as_long() for p in presses)

    return total

if __name__ == "__main__":
    lines = []
    with open("Inputs/Day10Input.txt", "r", encoding="utf-8") as f:
        for line in f:
            lines.append(line.rstrip("\n"))
    result_part_one = day10Q1(lines)
    print("Result for part one: " + str(result_part_one))
    result_part_two = day10Q2(lines)
    print("Result for part two: " + str(result_part_two))