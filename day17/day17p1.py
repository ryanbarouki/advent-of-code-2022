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
        self.bottom_y = 0
        self.floor_and_rock = set([(x,0) for x in range(0,width+2)]) # floor
        self.rock_builder = RockBuilder()
    
    def spawn_rock(self):
        return self.rock_builder.build_next_rock((3,self.bottom_y+4))
    
    def intersecting(self, rock):
        return rock.coords & self.floor_and_rock or rock.get_left() <= 0 or rock.get_right() > self.width
        
    def main_loop(self, iterations):
        moves = {'>': (1,0), '<': (-1,0)}
        down = (0,-1)
        jet_move_count = 0
        for i in range(iterations):
            move_jet = True
            rock = self.spawn_rock()
            while True:
                if move_jet:
                    move_vec = moves[self.jets[jet_move_count]] 
                    jet_move_count = (jet_move_count + 1) % len(self.jets)
                else:
                    move_vec = down
                rock.move(move_vec)
                if self.intersecting(rock):
                    dx,dy = move_vec
                    rock.move((-dx,-dy))
                    if not move_jet:
                        break
                move_jet = not move_jet
            self.floor_and_rock |= rock.coords
            self.bottom_y = max(self.floor_and_rock, key=lambda a: a[1])[1]

    def __repr__(self) -> str:
        output = ""
        for i in range(self.bottom_y+2):
            y = self.bottom_y+2-i
            row = "|"
            for x in range(1, self.width+1):
                row += "#" if (x,y) in self.floor_and_rock else "."
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

    print(len(jets)) 
    chamber = Chamber(width=7, jets=jets)
    chamber.main_loop(2022)
    # print(chamber)
    print(f"Part 1: {chamber.bottom_y}")    
