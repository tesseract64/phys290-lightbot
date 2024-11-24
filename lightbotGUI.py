from vpython import *
from lightbotKernel import Lightbot


class LightbotGUI(Lightbot):
    def initializeTerrain(self):
        #Initialize the terrain
        for i in range(self.rows):
            for j in range(self.columns):
                renk = color.white
                if self.terrain_light_info[i][j] == True:
                    renk = color.blue
                cube = box(pos=vector(i, 0, j), size=vector(1, 0.01 * self.terrain_depth_info[i][j] + 1, 1), color=renk)
        

        