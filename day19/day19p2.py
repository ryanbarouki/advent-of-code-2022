from collections import deque
import re
    
def hash(resources, robots):
    res_hash = ",".join([str(resources[x]) for x in resources])
    robot_hash = ",".join([str(robots[x]) for x in robots])
    return f"{res_hash}-{robot_hash}"

class MoveSearch:
    def __init__(self, blueprint, max_depth, max_ore, max_clay, max_obsidian) -> None:
        self.blueprint = blueprint
        self.resources = {'ore': 0, 'clay': 0, 'obsidian': 0, 'geode': 0}
        self.robots = {'ore': 1, 'clay': 0, 'obsidian': 0, 'geode': 0}
        self.max_depth = max_depth
        self.max_ore_cost = max_ore
        self.max_clay_cost = max_clay 
        self.max_obsidian_cost = max_obsidian

    def collect_resources(self, resources, robots):
        for robot in robots:
            if robots[robot] != 0:
                resources[robot] += robots[robot]
        return resources

    def trim_moves(self, moves, depth):
        if 'geode' in moves:
            return [moves['geode']]
        return moves.values()

    def get_possible_moves(self, resources, robots, depth):
        moves = {}
        can_make_robot = {'ore': True, 'clay': True, 'obsidian': True, 'geode': True}
        for robot in self.blueprint:
            if robot == 'ore' and resources['ore'] > self.max_ore_cost*(self.max_depth - depth):
                continue
            if robot == 'ore' and robots['ore'] > max_ore_cost:
                continue
            if robot == 'clay' and resources['clay'] > self.max_clay_cost*(self.max_depth - depth):
                continue
            if robot == 'clay' and robots['clay'] > max_clay_cost:
                continue
            if robot == 'obsidian' and resources['obsidian'] > self.max_obsidian_cost*(self.max_depth - depth):
                continue
            if robot == 'obsidian' and robots['obsidian'] > max_obsidian_cost:
                continue
            new_resources = resources.copy()
            new_robots = robots.copy()
            can_make_robot[robot] = True
            for material in self.blueprint[robot]:
                if resources[material] < self.blueprint[robot][material]:
                    can_make_robot[robot] = False
                    break
            if can_make_robot[robot]:
                for material in blueprint[robot]:
                    new_resources[material] = resources[material] - blueprint[robot][material]
                new_robots[robot] += 1
                moves[robot] = (self.collect_resources(new_resources, robots), new_robots)
        # do nothing move
        moves['nothing'] = (self.collect_resources(resources, robots), robots)
        
        return self.trim_moves(moves, depth)

    def bfs_moves(self):
        visited = set()
        queue = deque()
        start = (self.resources, self.robots)
        queue.append((start, 1))
        visited.add(hash(*start))
        final_moves = []

        i = 0
        while len(queue) > 0:
            i += 1
            # print(f"{i}\r", end="")
            (resources, robots), depth = queue.popleft()
            if depth > self.max_depth:
                final_moves.append(resources)
                continue
            possibilities = self.get_possible_moves(resources, robots, depth) if depth <= self.max_depth else []
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

        max_ore_cost = max(ore_robot_ores, clay_robot_ores, obsidian_robot_ores)
        max_clay_cost = obsidian_robot_clay
        max_obsidian_cost = geode_robot_obsidian

        blueprint = {'ore': {'ore': ore_robot_ores, 'clay': 0, 'obsidian': 0},
                    'clay': {'ore': clay_robot_ores, 'clay': 0, 'obsidian': 0},
                    'obsidian': {'ore': obsidian_robot_ores, 'clay': obsidian_robot_clay, 'obsidian': 0},
                    'geode': {'ore': geode_robot_ores, 'clay': 0, 'obsidian': geode_robot_obsidian}
        }
        blueprints.append((blueprint, max_ore_cost, max_clay_cost, max_obsidian_cost))

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
    # blueprints = [(blueprint1, 4, 14, 7), (blueprint2, 3, 8, 12)]
    quality = 1
    for i, (blueprint, max_ore, max_clay, max_obsidian) in enumerate(blueprints[0:3]):
        move_search = MoveSearch(blueprint, 32, max_ore, max_clay, max_obsidian)
        final_moves = move_search.bfs_moves()
        max_geodes = sorted(final_moves, key=lambda x: x['geode']).pop()['geode']
        print(f"blueprint {i+1} max geodes: {max_geodes}")
        quality *= max_geodes
    print(f"Part 1: quality level is {quality}")
