""" 
Functions for manipulating coordinates.
"""

__all__ = [
	'get_cube_vertices', 
	'tex_coord',
	'tex_coords',
	'get_closest_coord'
	]


CUBE_HALF_SIZE = 0.5
TEXTURE_GRID_SIZE = 8


def get_closest_coord(x, y, z):
	""" Input: 3D coordinate. Output: rounded 3D coordinate to nearest integers.
	"""
	x = int(round(x))
	y = int(round(y))
	z = int(round(z))
	return x, y, z


def get_cube_vertices(x, y, z, w=CUBE_HALF_SIZE):
	""" Takes in a 3D coordinate, and returns 24 3D coordinates in the form of a
	72 float tuple. Each group of 4 coordinates represents a cube face.
	"""
	return (
		x-w,y+w,z-w, x-w,y+w,z+w, x+w,y+w,z+w, x+w,y+w,z-w,		# top
		x-w,y-w,z-w, x+w,y-w,z-w, x+w,y-w,z+w, x-w,y-w,z+w,		# bottom 
		x-w,y-w,z-w, x-w,y-w,z+w, x-w,y+w,z+w, x-w,y+w,z-w,		# left side
		x+w,y-w,z+w, x+w,y-w,z-w, x+w,y+w,z-w, x+w,y+w,z+w,		# right side
		x-w,y-w,z+w, x+w,y-w,z+w, x+w,y+w,z+w, x-w,y+w,z+w,		# front side
		x+w,y-w,z-w, x-w,y-w,z-w, x-w,y+w,z-w, x+w,y+w,z-w		# back side
	)


def tex_coord(x, y, n=1.0/TEXTURE_GRID_SIZE):
	""" Returns 2D coordinates for a square. This represents a single face from
	the texture atlas. """
	dx = x * n
	dy = y * n
	return dx,dy, dx+n,dy, dx+n,dy+n, dx,dy+n


def tex_coords(top, bottom, side):
	""" Returns 2D coordinates for 6 squares in the form of a 48 float tuple. Each
	group of 4 coordinates represents a square face. """
	top 	 = tex_coord(*top)
	bottom = tex_coord(*bottom)
	side 	 = tex_coord(*side)
	return top + bottom + side*4


GRASS  = tex_coords((0,0), (2,0), (1,0))
DIRT   = tex_coords((2,0), (2,0), (2,0))
STONE  = tex_coords((3,0), (3,0), (3,0))
SAND   = tex_coords((0,1), (0,1), (0,1))
WOOD   = tex_coords((1,2), (1,2), (0,2))
LEAF   = tex_coords((2,2), (2,2), (2,2))
TEST   = tex_coords((7,7), (7,7), (7,7))
WATER  = tex_coords((6,7), (6,7), (6,7))
PLANK  = tex_coords((0,3), (0,3), (0,3))
COBBLE = tex_coords((0,4), (0,4), (0,4))


CHUNK_SIZE = 16
BLOCK_TYPES = [GRASS, STONE, SAND, WOOD]


"""
def get_object_bounds(x, y, z, w=0.2, h=1.8):
	# Input: 3D coordinate. Output: 24 coordinates representing the 8 vertices 
	# of the box bounding objects.
	return (
		x-w, y,   z-w,	# top upper left
		x-w, y,   z+w, 	# top lower left
		x+w, y,   z-w, 	# top upper right
		x+w, y,   z+w,	# top lower right
		x-w, y-h, z-w, 	# botttom upper left 
		x-w, y-h, z+w, 	# botttom lower left
		x+w, y-h, z-w, 	# botttom upper right
		x+w, y-h, z+w,	# bottom  lower right
	)
"""