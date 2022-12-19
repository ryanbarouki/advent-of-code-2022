from collections import deque
import re
    
def collect_resources(resources, robots):
    for robot in robots:
        if robots[robot] != 0:
            resources[robot] += robots[robot]
    return resources

def trim_moves(moves):
    if 'geode' in moves:
        return [moves['geode']]
    elif 'obsidian' in moves:
        return [moves['obsidian']]
    return moves.values()

def get_possible_moves(blueprint, resources, robots, depth):
    moves = {}
    can_make_robot = {'ore': True, 'clay': True, 'obsidian': True, 'geode': True}
    for robot in blueprint:
        new_resources = resources.copy()
        new_robots = robots.copy()
        can_make_robot[robot] = True
        for material in blueprint[robot]:
            if resources[material] < blueprint[robot][material]:
                can_make_robot[robot] = False
                break
        if can_make_robot[robot]:
            for material in blueprint[robot]:
                new_resources[material] = resources[material] - blueprint[robot][material]
            new_robots[robot] += 1
            moves[robot] = (collect_resources(new_resources, robots), new_robots)
    # do nothing move
    moves['nothing'] = (collect_resources(resources, robots), robots)
    
    return trim_moves(moves, depth)

def hash(resources, robots):
    res_hash = ",".join([str(resources[x]) for x in resources])
    robot_hash = ",".join([str(robots[x]) for x in robots])
    return f"{res_hash}-{robot_hash}"


def update_resources(resources, robots):
    for robot in robots:
        if robots[robot] != 0:
            resources[robot] += 1
    return resources

def bfs_moves(blueprint, resources, robots):
    visited = set()
    queue = deque()
    start = (resources, robots)
    queue.append((start, 1))
    visited.add(hash(*start))
    final_moves = []

    i = 0
    max_depth = 24
    while len(queue) > 0:
        i += 1
        # print(f"{i}\r", end="")
        (resources, robots), depth = queue.popleft()
        if depth > max_depth:
            final_moves.append(resources)
            continue
        possibilities = get_possible_moves(blueprint, resources, robots, depth) if depth <= max_depth else []
        for move in possibilities:
            if hash(*move) not in visited:
                queue.append((move, depth+1))
                visited.add(hash(*move))
    return final_moves

with open('input.txt') as f:
    resources = {'ore': 0, 'clay': 0, 'obsidian': 0, 'geode': 0}
    robots = {'ore': 1, 'clay': 0, 'obsidian': 0, 'geode': 0}
    blueprints = []
    for line in f.readlines():
        line = line.strip()
        nums = [int(s) for s in re.findall(r'\d+', line)]
        bp_num, ore_robot_ores, clay_robot_ores, \
        obsidian_robot_ores, obsidian_robot_clay, \
        geode_robot_ores, geode_robot_obsidian = nums

        blueprint = {'ore': {'ore': ore_robot_ores, 'clay': 0, 'obsidian': 0},
                    'clay': {'ore': clay_robot_ores, 'clay': 0, 'obsidian': 0},
                    'obsidian': {'ore': obsidian_robot_ores, 'clay': obsidian_robot_clay, 'obsidian': 0},
                    'geode': {'ore': geode_robot_ores, 'clay': 0, 'obsidian': geode_robot_obsidian}
        }
        blueprints.append(blueprint)

    blueprint1 = {'ore': {'ore': 4, 'clay': 0, 'obsidian': 0},
                'clay': {'ore': 2, 'clay': 0, 'obsidian': 0},
                'obsidian': {'ore': 3, 'clay': 14, 'obsidian': 0},
                'geode': {'ore': 2, 'clay': 0, 'obsidian': 7}
    }
    blueprint2 = {'ore': {'ore': 2, 'clay': 0, 'obsidian': 0},
                'clay': {'ore': 3, 'clay': 0, 'obsidian': 0},
                'obsidian': {'ore': 3, 'clay': 8, 'obsidian': 0},
                'geode': {'ore': 3, 'clay': 0, 'obsidian': 12}
    }
    blueprints = [blueprint1, blueprint2]
    quality = 0
    for i, blueprint in enumerate(blueprints):
        resources = {'ore': 0, 'clay': 0, 'obsidian': 0, 'geode': 0}
        robots = {'ore': 1, 'clay': 0, 'obsidian': 0, 'geode': 0}
        final_moves = bfs_moves(blueprint, resources, robots)
        max_geodes = sorted(final_moves, key=lambda x: x['geode']).pop()['geode']
        print(f"blueprint {i+1} max geodes: {max_geodes}")
        quality += (i+1)*max_geodes
    print(f"Part 1: quality level is {quality}")
