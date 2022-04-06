from json import load
from turtle import position
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

# create a window
app = Ursina()

grass_texture = load_texture('assets/grass_block.png')
stone_texture = load_texture('assets/stone_block.png')
brick_texture = load_texture('assets/brick_block.png')
dirt_texture = load_texture('assets/dirt_block.png')
sky_texture = load_texture('assets/skybox.png');
arm_texture = load_texture('assets/arm_texture.png')
punch_sound = Audio('assets/punch_sound', loop = False, autoplay=False)

block_pick = 1

window.fps_counter.enabled = False
window.exit_button.visible = False


def update():
    global block_pick

    if held_keys['left mouse'] or held_keys['right mouse'] :
        hand.active()
    else: 
        hand.passive()

    if held_keys['1']: block_pick = 1
    if held_keys['2']: block_pick = 2
    if held_keys['3']: block_pick = 3
    if held_keys['4']: block_pick = 4

# class to simulate a cube
class Voxel(Button):
    def __init__(self, position = (0,0,0), texture = grass_texture):
        super().__init__(
            parent= scene,
            position = position,
            model = 'assets/block',
            origin_y = 0.5,
            texture = texture,
            color = color.color(0,0,random.uniform(0.9,1)),
            # highlight_color = color.lime,
            scale = 0.5
        )

    # interaction with mouse
    def input(self,key):
        if self.hovered:
            # left click to create cube
            if key == "left mouse down":
                punch_sound.play()
                texture_new = grass_texture
                if block_pick == 1: texture_new = grass_texture
                if block_pick == 2: texture_new = stone_texture
                if block_pick == 3: texture_new = brick_texture
                if block_pick == 4: texture_new = dirt_texture

                voxel = Voxel(position=self.position + mouse.normal, texture = texture_new)
            
            # right click to delete cube
            if key == "right mouse down":
                punch_sound.play()
                destroy(self)

class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent = scene,
            model = 'sphere',
            texture = sky_texture,
            scale = 150,
            double_sided =True
        )

class Hand(Entity):
    def __init__(self):
        super().__init__(
            parent = camera.ui,
            model = 'assets/arm',
            texture = arm_texture,
            scale = 0.2,
            rotation = Vec3(150,-10,0),
            position = Vec2(0.4, -0.6)
        )
    def active(self):
        self.position = Vec2(0.3, -0.5)

    def passive(self):
        self.position = Vec2(0.4, -0.6)


# create chunk or map   
chunkSize = 16
for z in range(chunkSize):
    for x in range(chunkSize):
        voxel = Voxel( position = (x,0,z))

# def input(key):
#     if key == 'left mouse down':
#         hit_info = raycast(camera.world_position, camera.forward, distance=5)
#         if hit_info.hit:
#             Voxel(position=hit_info.entity.position + hit_info.normal)


# create player in first person
player = FirstPersonController()
sky = Sky()
hand = Hand()

# start running the game
app.run()