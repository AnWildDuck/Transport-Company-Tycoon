
'''
Nodes = {Pos: Neighbours,}
Start and end are positions

All Positions are in the format (x, y)
'''

def find_path(nodes, start, end):

    # Candidates to be stored as [(pos, parent pos, cost)]
    start_candidate = start, None, 0
    candidates = [start_candidate]

    # Positions with all calculations done
    # In format [(pos, parent pos, cost)], same as candidates
    calculated_pos = []

    while True: # Loop through all candidates
        stop = False

        # Sort candidates by cost (Low to high)
        candidates.sort(key = lambda x: x[2])

        # Has the end been found?
        for item in calculated_pos:
            if item[0] == end:
                stop = True
                break

        # Extra stop variable needed because 'break' only works inside one loop
        if stop: break

        # Are there no more options?
        if len(candidates) == 0:
            return False

        # Choose position to search
        candidate = candidates[0]

        # Does it have any neighbours?
        if candidate[0] in nodes:

            # What are its neighbours?
            neighbours = nodes[candidate[0]]

            # Add neighbours to candidates
            for pos in neighbours:

                # Work out cost to get to here
                last_change = abs(candidate[0][0] - pos[0]) + abs(candidate[0][1] - pos[1])
                cost = last_change + candidate[2]

                # Has this new position already been worked out?
                searched_pos = [i[0] for i in calculated_pos + candidates]

                if not pos in searched_pos:
                    value = pos, candidate[0], cost

                    # Add
                    candidates.append(value)

        # Add candidate to calculated_pos
        calculated_pos.append(candidate)

        # Remove from candidates
        candidates.pop(0)

    # Backtrack to find path
    path = [end]
    while True:

        # Have we made it back?
        if start in path: break

        last_pos = path[len(path) - 1]

        # Find parent
        for item in calculated_pos:
            if item[0] == last_pos:
                parent = item[1]

        # Add parent to path
        path.append(parent)

    return path


nodes = {
    (0,0): [(1,0),(0,1)],
    (1,0): [(1,1), (2,0), (0,0)],
    (2,0): [(2,1)],
}

start = (0,0)
end = (2,0)

print(find_path(nodes, start, end))