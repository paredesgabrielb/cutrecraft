from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

# create a window
app = Ursina()

# class to simulate a cube
class Voxel(Button):
    def __init__(self, position = (0,0,0)):
        super().__init__(
            parent= scene,
            position = position,
            model = 'cube',
            origin_y = 0.5,
            texture = 'grass',
            color = color.rgb(255,255,255),
            highlight_color = color.lime,
        )

    # interaction with mouse
    def input(self,key):
        if self.hovered:
            # left click to create cube
            if key == "left mouse down":
                    voxel = Voxel(position=self.position + mouse.normal)
            # right click to delete cube
            if key == "right mouse down":
                    destroy(self)

# create chunk or map   
chunkSize = 16
for z in range(chunkSize):
    for x in range(chunkSize):
        voxel = Voxel( position = (x,0,z))

# create player in first person
player = FirstPersonController()

# start running the game
app.run()