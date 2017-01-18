# External libraries
from pyglet.window import key

# Standard libraries
import math as m


DEFAULT_SPEED = 0.2
MOUSE_SENS    = 0.1



class Player(object):   
    """ Represents the player within the game. Holds the states and methods
    needed to handle movement.
    """

    def __init__(self, loc=(0,0,0)):
        # Position Attributes
        self.loc = loc
        self.original_loc = loc
        self.rot = (0, 0)
        
        # Movement attributes
        self.move_right     = 0
        self.move_forward   = 0
        self.move_upward    = 0

        # State attributes
        self.speed = DEFAULT_SPEED
        self.collision = False  # implement later
        self.fly = True         
    
    """
    Reimplement the way that event handling works later. Right now, it doesn't
    make much sense, and mouse movement is too janky.
    """

    def update(self, dt):
        """ Updates the location of the player given a unit of time. """
        x, y, z = self.loc
        dx, dy, dz = self.get_velocity()
        self.loc = x + dx, y + dy, z - dz


    def on_mouse_motion(self, x, y, dx, dy):
        """ Called from Window whenever the mouse moves. """
        x, y = self.rot
        x, y = x+dx*MOUSE_SENS, y+dy*MOUSE_SENS
        y = max(-90, min(90, y))
        #print(x,y)
        self.rot = x, y


    def on_key_press(self, symbol, modifiers):
        """ Called from Window whenever key is pressed. """
        if symbol == key.W:
            self.move_forward += 1
        elif symbol == key.S:
            self.move_forward -= 1
        elif symbol == key.A:
            self.move_right -= 1
        elif symbol == key.D:
            self.move_right += 1    
        elif symbol == key.LSHIFT:
            self.speed = DEFAULT_SPEED * 8
        elif symbol == key.O:               
            self.loc = self.original_loc    


    def on_key_release(self, symbol, modifiers):
        """ Called from Window whenever keyis depressed. """
        if symbol == key.W:
            self.move_forward -= 1
        elif symbol == key.S:
            self.move_forward += 1
        elif symbol == key.A:
            self.move_right += 1
        elif symbol == key.D:
            self.move_right -= 1
        elif symbol == key.LSHIFT:
            self.speed = DEFAULT_SPEED


    def get_velocity(self):
        """ Returns 3D vector representing the current velocity of player. """
        rx, rz = self.rot
        s = self.speed
        mult = m.cos(m.radians(rz))

        dz = (m.cos(m.radians(rx))    * self.move_forward -
              m.cos(m.radians(90-rx)) * self.move_right) * s * mult
        dy = (m.cos(m.radians(90-rz)) * self.move_forward) * s
        dx = (m.sin(m.radians(rx))    * self.move_forward + 
              m.sin(m.radians(90-rx)) * self.move_right) * s * mult

        #print (dx, dy, dz)
        return dx, dy, dz


    def get_sight_vector(self):
        """ Returns 3D unit vector representing where the player is looking. """
        rx, rz = self.rot
        mult = m.cos(m.radians(rz))

        dz = m.sin(m.radians(rx-90)) * mult
        dy = m.sin(m.radians(rz))
        dx = m.cos(m.radians(rx-90)) * mult

        #print("sight length: {}".format(m.sqrt(dx**2 + dy**2 + dz**2)))
        #print(dx, dy, dz)
        return dx, dy, dz