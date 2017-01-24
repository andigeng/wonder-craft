# External libraries
from pyglet.gl import *
from pyglet import image
from pyglet.graphics import TextureGroup
from noise import pnoise1, pnoise2, snoise2

# Standard libraries
import random

# Local files
import cubes as C


    
CLEAR_COLOR = (0.5, 0.7, 1, 1)
ZERO = (0, 0, 0)


class World(object):
    """ """
    def __init__(self):
        # Textures
        self.block_textures = None
        self.load_textures()
        
        # Tracks what blocks are in the world.
        self.map = {}
        # Tracks what blocks are visible in the world. Each coordinate links to
        # a set of 24 Pyglet vertices. When an object is deleted from here,
        # it is no longer rendered.
        self.visible = {}

        # This manages vertex lists for batched rendering.
        self.batch  = pyglet.graphics.Batch()

        self.perlin_noise_test()
        self.render_all_map()
        #self.enable_fog()


    def add_block(self, loc, block_type):
        """ Adds a block to the world without making it visible. """
        self.map[loc] = block_type         # future optimization: instead of storing block_type, store block_id (integers instead oflarger objects)


    def del_block(self, loc):
        """ Deletes a block from the world, and removes it from render batch. 
        """
        loc = C.get_closest_coord(*loc)
        if (loc in self.map):
            del self.map[loc]
            self.visible.pop(loc).delete()


    def show_block(self, loc, block_type):
        """ Adds a block to the render batch. """
        cube_coords = C.get_cube_vertices(*loc)
        self.visible[loc] = self.batch.add(24, GL_QUADS, self.block_textures,
                                          ('v3f', cube_coords),
                                          ('t2f', block_type))

    
    def render_all_map(self):
        """ Takes all blocks from the world, and adds it to the render batch.
        Only use this once, at the beginning before anything else is added. 
        """
        for loc, block_type in self.map.iteritems():
            self.show_block(loc, block_type)


    def place_block(self, loc):
        """ Called when a player tries to place a block. """
        loc = C.get_closest_coord(*loc)
        if (loc in self.map):
            self.del_block(loc)
        self.add_block(loc, C.SAND)
        self.show_block(loc, C.SAND)


    def hit_test(self, origin, vector, distance=20, increments=10):
        """ Hit test for first block. Returns coordinates of first block that 
        is hit, in addition to the empty space before it. """
        x, y, z = origin
        dx, dy, dz = vector
        dx, dy, dz = dx/increments, dy/increments, dz/increments
        for k in range(increments*distance):
            block_loc = x + k*dx, y + k*dy, z + k*dz
            block_loc = C.get_closest_coord(*block_loc)
            if (block_loc in self.map):
                j = k-1
                empty_loc = C.get_closest_coord(x+j*dx, y+j*dy, z+j*dz)
                return block_loc, empty_loc
        return None, None


    def collision_adjust(self, loc, height=1.8, width=0.2):
        """ Very inelegant implementation of collision detection. Polish this up
        later. """
        x, y, z = loc
        stop_x, stop_y, stop_z = False, False, False
        padding = (1-width)/2

        # Check if there is ground below
        rx, ry, rz = C.get_closest_coord(x, y, z)
        if ((rx,ry,rz) in self.map):
            y = ry + 0.5
            stop_y = True

        # Check the sides of the player
        print(rx+1, ry+1, rz)
        if ((rx+1,ry+1,rz) in self.map):
            x = rx - 0.5
            stop_x = True
        elif ((rx-1,ry+1,rz) in self.map):
            x = rx + 0.5
            stop_x = True
        elif ((rx,ry+1,rz+1) in self.map):
            z = rz - 0.5
            stop_z = True
        elif ((rx,ry+1,rz-1) in self.map):
            z = rz + 0.5
            stop_z = True
        
        return x, y, z, stop_x, stop_y, stop_z


    def load_textures(self):
        self.block_textures  = self._load_texture('data/textures/blocks.png')
        # Insert other textures to be laoded later (flora, fauna, etc)


    def _load_texture(self, file):
        tex = pyglet.image.load(file).texture
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        return pyglet.graphics.TextureGroup(tex)


    def perlin_noise_test(self):
        """ Use basic perlin noise to generate rolling landscape. """
        size = 128
        for i in range(size):
            for j in range(size):
                x = float(i)/20
                y = float(j)/20
                k = pnoise2(x, y)*7

                if k < -2:
                    self.add_block(C.get_closest_coord(i, k, j), C.SAND)
                    self.add_block(C.get_closest_coord(i, k-1, j), C.SAND)
                else:
                    self.add_block(C.get_closest_coord(i, k, j), C.GRASS)
                    self.add_block(C.get_closest_coord(i, k-1, j), C.DIRT)
                    if random.random() > 0.99:
                        self.add_tree((i, k+1, j), random.randint(2,4))


    def add_tree(self, loc, size):
        x, y, z = loc
        x, y, z = C.get_closest_coord(x, y, z)
        for i in range(0, size):
            self.add_block((x, y+i,z), C.WOOD)
        self.make_square_base((x,y+size,z), 1, C.LEAF)
        self.make_cross_base((x,y+size+1,z), 1, C.LEAF)

                    
    def make_square_base(self, loc, size, block_type):
        """ Takes an integer, creates a horizontal square of size 2*size+1 at coordinates. """
        x, y, z = loc
        x, y, z = C.get_closest_coord(x, y, z)
        for i in range(-size, size+1):
            for j in range(-size, size+1):
                self.add_block((x+i, y, z+j), block_type) 


    def make_cross_base(self, loc, size, block_type):
        x, y, z = loc
        x, y, z = C.get_closest_coord(x, y, z)
        for i in range(-size, size+1):
            self.add_block((x+i,y,z), block_type)
        for i in range(-size, size+1):
            if i != 0:
                self.add_block((x,y,z+i), block_type)


    def enable_fog(self):
        glEnable(GL_FOG)
        glFogfv(GL_FOG_COLOR, (GLfloat*4)(*CLEAR_COLOR))
        glFogi(GL_FOG_MODE, GL_LINEAR)          # Linear fog calculations
        glFogf(GL_FOG_START, 35)                # Start fog distance 35 units
        glFogf(GL_FOG_END, 50)  


    def save_world(self, file):
        """ """
        pass


    def load_world(self, file):
        """ """
        pass                
