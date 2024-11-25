class Lightbot:
    #To initalize Lightbot, you need to give 2 parameters: Name of the Map info and Instructions text files.
    def __init__(self, map_info_input, instruction_input):
        self.columns, self.rows, self.x, self.y, self.z, self.direction = self.read_map_info(map_info_input)  # Read data from input files. columns and rows are map data. x, y, z are initial coordinates.
        self.terrain_light_info = [[False for _ in range(self.rows)] for _ in range(self.columns)]  #   Direction is an array in form (x,y) which represents which block the lightbot is "looking" at.
        self.terrain_depth_info = [[0 for _ in range(self.rows)] for _ in range(self.columns)]
        self.terrain_color_info = [[False for _ in range(self.rows)] for _ in range(self.columns)] # Initializes full gray array
        self.read_terrain_depth_info(map_info_input)
        self.instructions = self.read_instructions(instruction_input)

    def read_map_info(self, map_info_input):
        with open(map_info_input, 'r') as file:
            lines = file.readlines()
            columns, rows = map(int, lines[0].strip().split(','))
            x, y, z = map(int, lines[1].strip().split(','))
            direction = list(map(int, lines[2].strip().split(',')))
        return columns, rows, x, y, z, direction

    def read_terrain_depth_info(self, map_info_input):
        with open(map_info_input, 'r') as file:
            lines = file.readlines()
            depth_info = lines[3].strip().split(',')  # Read the fourth line for depth info

            for i in range(self.columns):
                for j in range(self.rows):
                    if i * self.rows + j < len(depth_info):
                        self.terrain_depth_info[i][j] = int(depth_info[i * self.rows + j])

    def read_terrain_color_info(self, map_info_input):
        with open(map_info_input, 'r') as file:
            lines = file.readlines()
            color_info = lines[4].strip().split(',')

            for i in range(self.columns):
                for j in range(self.rows):
                    if i * self.rows + j < len(color_info):
                        self.terrain_color_info[i][j] = bool(color_info[i * self.rows + j])

    def read_instructions(self, instruction_input):
        with open(instruction_input, 'r') as file:
            instructions = file.read().replace(" ", "").split(",")
        return instructions

    def driver_code(self):
        for ins in self.instructions:
            if ins == '^':  # Move forward
                self.move_forward()
            elif ins == '@':  # Switch light
                self.switch_light()
            elif ins == '<':  # Turn left
                self.turn_left()
            elif ins == '>':  # Turn right
                self.turn_right()
            elif ins == '*':  # Jump forward
                self.jump_forward()
    # Turning codes are pretty self-explanatory
    def turn_left(self):
        self.direction[0] -= 1
        self.direction[1] += 1

    def turn_right(self):
        self.direction[0] += 1
        self.direction[1] -= 1

    #  If not at the edges, executes the code. Replaces the coordinates with the coord. of the block Lightbot is looking at.
    #  Keeps the relative distance same between Lightbot and the block it is looking
    def move_forward(self):
        if (self.direction[0] <= self.columns & self.direction[1] <= self.rows & self.direction[0] >= 0 & self.direction[1] >= 0):
            tmp_x = self.direction[0]
            tmp_y = self.direction[1]
            self.x = self.direction[0]
            self.y = self.direction[1]
            self.direction[0] += self.direction[0] - tmp_x
            self.direction[1] += self.direction[1] - tmp_y
    #If the block Lightbot is looking is higher or lower then 1 block, does nothing.
    def jump_forward(self):
        dir_x = self.direction[0]
        dir_y = self.direction[1]
        if(self.terrain_depth_info[dir_x][dir_y] == self.terrain_depth_info[self.x][self.y] + 1):
            self.move_forward()
            self.z += 1
        if (self.terrain_depth_info[dir_x][dir_y] == self.terrain_depth_info[self.x][self.y] - 1):
            self.move_forward()
            self.z -= 1

    # In Lightbot, switching the light when it is on switches off the light. So it is sensible to use a XOR gate.
    def switch_light(self):
        self.terrain_light_info[self.x][self.y] = self.terrain_light_info[self.x][self.y] != True

    def print_final_map(self):
        # Print the final state of terrain_light_info from bottom to top
        for i in range(self.columns - 1, -1, -1):  # Start from the bottom row
            row = []
            for j in range(self.rows):
                # 1 if lit, 0 if not
                row.append(1 if self.terrain_light_info[i][j] else 0)
            print(" ".join(map(str, row)))
# In the future, I plan to seperate the map initialization and instructions. First you initialize the map, then you give the instructions. This way, you can play the game
# several times with the same map without recreating the map each time. Also implement a destructor, as I don't know how to do so in Python.
