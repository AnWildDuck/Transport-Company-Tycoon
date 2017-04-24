
'''
Nodes = {Pos: Neighbours,}
Start and end are positions

All Positions are in the format (x, y)
'''

def find_path(road_handler, start, end):

    pos = road_handler.pos
    outs = road_handler.outs
    names = road_handler.img_names

    # Is the start next to a road?
    valid = False
    for xc, yc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        new_pos = start[0] + xc, start[1] + yc
        if new_pos in pos: valid = True; break

    # Is the end next to a road?
    for xc, yc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        new_end = end[0] + xc, end[1] + yc
        if new_end in pos: valid = True; break

    if not valid: return False

    nodes = sort_nodes(pos, outs, names)
    path = get_path(nodes, new_pos, new_end)

    if path:
        path.append(start)
        path.reverse()
        path.append(end)


    return path


def get_path(nodes, start, end):

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


# positions in format [(x,y),]
def sort_nodes(positions, neighbours, img_names): # All inputs are just lists inside of the road handler
    nodes = {}

    # A road will become a node if it is a corner, intersection or cul-de-sac
    for index in range(len(positions)):

        pos = positions[index]
        outs = neighbours[index]
        img_name = img_names[index]

        neighbouring_pos = [] # Keep track of all positions that can be reached from the current pos

        # Do we care about this?
        if img_name != 'straight' or outs != 2:

            # For each direction
            for xc, yc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:

                ext_pos = list(pos)
                while True:

                    # Move ext_pos in direction
                    last_pos = list(ext_pos)
                    ext_pos[0] += xc
                    ext_pos[1] += yc

                    # Is it still valid?
                    if ext_pos in positions:
                        continue

                    else: # This is the end of the road
                        if not tuple(last_pos) in positions:
                            neighbouring_pos.append((last_pos[0] - xc, last_pos[1] - yc))
                            break

            # Add to nodes
            nodes[pos] = neighbouring_pos
    return nodes
