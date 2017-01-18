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
        # Insert other textures to be loaded here later
        self.load_textures()
        
        self.map = {}
        self.visible = {}
        #self.sectors = {}
        self.batch  = pyglet.graphics.Batch()
        self.perlin_noise_test()
        self.render_all_map()
        self.enable_fog()


    def add_block(self, loc, block_type):
        self.map[loc] = block_type         # future optimization: instead of storing block_type, store block_id (integers instead oflarger objects)

    def _del_block(self, loc):
        if (loc in self.map):
            del self.map[loc]
            self.visible.pop(loc).delete()
        #print (loc in self.visible)

    def show_block(self, loc, block_type):
        cube_coords = C.get_cube_vertices(*loc)
        self.visible[loc] = self.batch.add(24, GL_QUADS, self.block_textures,
                                          ('v3f', cube_coords),
                                          ('t2f', block_type))

    def hide_block(self, loc):
        pass

    def render_map(self, loc):
        pass

    def sector_test(self):      #, loc):
        size = 32
        for i in range(size):
            for j in range(size):
                self.add_block((i,0,j), C.GRASS)

    def render_all_map(self):
        for loc, block_type in self.map.iteritems():
            self.show_block(loc, block_type)

    def del_block(self, loc):
        loc = C.get_closest_coord(*loc)
        self._del_block(loc)

    def place_block(self, loc):
        loc = C.get_closest_coord(*loc)
        if (loc in self.map):
            self._del_block(loc)
        self.add_block(loc, C.SAND)
        self.show_block(loc, C.SAND)

    def hit_test(self, origin, vector, distance=20, increments=10):
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

    def load_textures(self):
        self.block_textures  = self._load_texture('data/textures/blocks.png')
        # Insert other textures to be laoded later (flora, fauna, etc)

    def _load_texture(self, file):
        tex = pyglet.image.load(file).texture
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        return pyglet.graphics.TextureGroup(tex)

    def perlin_noise_test(self):
        size = 64
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

    def chunk_stress_test(self):
        for i in range(CHUNK_SIZE):
            for j in range(CHUNK_SIZE):
                for k in range(CHUNK_SIZE):
                    if (random.random() > 0.9):
                        self.add_block((i,j,k), random.choice(BLOCK_TYPES))    

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
