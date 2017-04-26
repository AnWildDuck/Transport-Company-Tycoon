import pygame, time

def get_neighbours(pos): return [(pos[0] + c[0], pos[1] + c[1]) for c in [(0,1),(0,-1),(1,0),(-1,0)]]

def find_path(road_handler, start, end, info):

    # Show start and end
    for item in []: # [start, end]:
        pygame.draw.circle(info['game_window'], (0, 0, 255), (int((item[0] + 0.5) * info['window']['game_scale']), int((item[1] + 0.5) * info['window']['game_scale'])), 5)

    nodes = road_handler.pos + [start, end]
    return make_path(nodes, start, end)

def make_path(nodes, start, end):

    ends = get_neighbours(end)

    # Candidates stored as (Pos, Parent)

    start_neighbours = get_neighbours(start)
    candidates = []
    for item in start_neighbours:
        candidates.append((item, None))

    calculated_pos = []

    while True:

        # Are there no more options?
        if len(candidates) == 0:
            # print()
            # for i in calculated_pos: print(i)
            return False

        # Have we finished?
        finished = False
        for item in calculated_pos:
            if item[0] in ends:
                end_node = item
                finished = True
                break
        if finished: break

        candidate = candidates[0]

        # Find neighbours
        neighbours = get_neighbours(candidate[0])
        valid_neighbours = []
        for pos in neighbours:
            if pos in nodes:
                valid_neighbours.append(pos)

        # Add neighbours to candidates
        for item in valid_neighbours:

            # Has this item already been looked at?
            okay = True
            for node in candidates + calculated_pos:
                if node[0] == item:
                    okay = False; break

            if okay:
                candidates.append((item, candidate[0]))

        # Add candidate to calculated_pos
        calculated_pos.append(candidate)

        # Remove candidate from candidates
        candidates.pop(0)

    # Backtrack to find path
    path = [end_node]

    while True:

        # Is the path finished?
        finished = False
        for pos in start_neighbours:
            for item in path:
                if item[0] == pos:
                    finished = True
                    break
        if finished: break

        last_node = path[len(path) - 1]
        parent = last_node[1]

        for item in calculated_pos:
            if item[0] == parent:
                if not item in path:
                    path.append(item)
                    break

    # Format path
    new_path = []
    for item in path:
        new_path.append(item[0])

    new_path.append(start)
    new_path.reverse()
    new_path.append(end)
    return new_path

