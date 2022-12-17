import time


class Rock:
    def __init__(self, coords, rock_type) -> None:
        self.coords = set(coords)
        self.rock_type = rock_type
    
    def move(self, vec):
        dx, dy = vec
        new_coords = set()
        for coord in self.coords:
            x, y = coord
            new_coords.add((x+dx, y+dy))
        self.coords = new_coords
    
    def get_left(self):
        x,y = min(self.coords)
        return x

    def get_bottom(self):
        x,y = min(self.coords, key=lambda a: a[1])
        return y

    def get_right(self):
        x,y = max(self.coords)
        return x

class RockBuilder:
    def __init__(self) -> None:
        self.rock_count = 0
        self.build_rock = {0: self._build_horizonal_rock,
                           1: self._build_plus_rock,
                           2: self._build_L_rock,
                           3: self._build_vertical_rock,
                           4: self._build_square_rock}

    def build_next_rock(self, bottom_left):
        return self.build_rock[self.rock_count % len(self.build_rock)](bottom_left)

    def _build_horizonal_rock(self, bottom_left):
        self.rock_count += 1
        x,y = bottom_left
        return Rock([(x,y), (x+1,y), (x+2,y), (x+3,y)], "-")

    def _build_plus_rock(self, bottom_left):
        self.rock_count += 1
        x,y = bottom_left
        return Rock([(x+1,y), (x,y+1), (x+1,y+1), (x+2,y+1), (x+1,y+2)], "+")

    def _build_L_rock(self, bottom_left):
        self.rock_count += 1
        x,y = bottom_left
        return Rock([(x,y), (x+1,y), (x+2,y), (x+2,y+1), (x+2,y+2)], "L")

    def _build_vertical_rock(self, bottom_left):
        self.rock_count += 1
        x,y = bottom_left
        return Rock([(x,y), (x,y+1), (x,y+2), (x,y+3)], "|")

    def _build_square_rock(self, bottom_left):
        self.rock_count += 1
        x,y = bottom_left
        return Rock([(x,y), (x+1,y), (x,y+1), (x+1,y+1)], "[]")

class Chamber:
    # |.......| 4
    # |.......| 3
    # |.......| 2
    # |.......| 1
    # +-------+ 0
    # 012345678

    def __init__(self, width, jets) -> None:
        self.width = width
        self.jets = jets
        self.top_y = 0
        self.rocks = set() # rocks above floor
        self.col_heights = [0 for _ in range(width+2)]
        self.normal_col_heights = [0 for _ in range(width+2)]
        self.floor = 0
        self.rock_builder = RockBuilder()
        self.cycle_cache = set()
    
    def spawn_rock(self):
        return self.rock_builder.build_next_rock((3,self.top_y+4))
    
    def intersecting_floor(self, rock):
        return rock.coords & self.rocks or rock.get_bottom() <= self.floor

    def intersecting_wall(self, rock):
        return rock.coords & self.rocks or rock.get_left() <= 0 or rock.get_right() > self.width
        
    def main_loop(self, iterations):
        moves = {'>': (1,0), '<': (-1,0)}
        jet_move_count = 0
        for i in range(iterations):
            print(f"{i}\r", end="")
            move_jet = True
            rock = self.spawn_rock()
            # print(self.normal_col_heights)
            # print(self.col_heights)
            cache_key = f"{rock.rock_type}{jet_move_count}{','.join([str(x) for x in self.normal_col_heights])}"
            if cache_key in self.cycle_cache:
                # print('repeat', i, self.top_y)
                self.cycle_cache.clear()
            self.cycle_cache.add(cache_key)
            while True:
                if move_jet:
                    move_vec = moves[self.jets[jet_move_count]] 
                    jet_move_count = (jet_move_count + 1) % len(self.jets)
                    rock.move(move_vec)
                    if self.intersecting_wall(rock):
                        dx,dy = move_vec
                        rock.move((-dx,-dy))
                else:
                    rock.move((0,-1))
                    if self.intersecting_floor(rock):
                        rock.move((0,1))
                        break
                move_jet = not move_jet

            self.rocks |= rock.coords
            for coord in rock.coords:
                x,y = coord
                if self.col_heights[x] < y:
                    self.col_heights[x] = y
                    self.normal_col_heights[x] = y - self.floor
                    # print("floor", self.floor)
            min_height = min(self.col_heights[1:-1])
            if min_height > self.floor:
                self.floor = min_height - 1
                self.trim_rocks(self.floor)
            self.top_y = max(self.col_heights)

    def trim_rocks(self, height):
        rocks = self.rocks.copy()
        for rock in rocks:
            x,y = rock
            if y < height:
                self.rocks.remove(rock)

    def __repr__(self) -> str:
        output = ""
        for i in range(self.top_y+2):
            y = self.top_y+2-i
            row = "|"
            for x in range(1, self.width+1):
                row += "#" if (x,y) in self.rocks else "."
            row += "|"
            output += row + "\n"
        last = "".join(["-" for _ in range(self.width)])
        output += f"+{last}+"
        return output


with open('input.txt') as f:
    jets = []
    for line in f.readlines():
        line = line.strip()
        jets = [*line]
    
    chamber = Chamber(width=7, jets=jets)
    start = time.time()
    chamber.main_loop(2022)
    end = time.time()
    # print(chamber)
    print(f"Part 1: {chamber.top_y} in {end-start} seconds")    
