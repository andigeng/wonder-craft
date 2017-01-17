# External libraries
from pyglet.gl import *
from pyglet.window import key

# Standard libraries
import math

# Local files
from player import Player
import world
from world import World




class Window(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.world = World()
        self.player = Player((0,0,0))
        pyglet.clock.schedule(self.update)


    def update(self, dt):
        self.player.update(dt)


    def on_mouse_motion(self, x, y, dx, dy):
        self.player.on_mouse_motion(x, y, dx, dy)


    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.set_exclusive_mouse(False)
        if symbol == key.M:
            self.set_exclusive_mouse(True)
        if symbol == key.I:
            self.world.test_func(self.player.pos)
        self.player.on_key_press(symbol, modifiers)


    def on_key_release(self, symbol, modifiers):
        self.player.on_key_release(symbol, modifiers)


    def set_projection(self): 
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()


    def set_model_view(self): 
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()


    def set3d(self): 
        self.set_projection()
        gluPerspective(70, self.width/self.height, 0.05, 1000)
        self.set_model_view();


    def on_draw(self):
        """  """
        self.clear()
        self.set3d()
        
        x, y = self.player.rot
        glRotatef(x, 0, 1, 0)
        glRotatef(-y, math.cos(math.radians(x)), 0, math.sin(math.radians(x)))     # Move this elsewhere
        
        x, y, z = self.player.pos                                                  # no need for math library when it's in player class
        glTranslatef(-x,-y,-z)
        
        self.world.batch.draw()



if __name__ == '__main__':
    window = Window(width=600, height=600, resizable=False)
    window.set_exclusive_mouse(True)
    glClearColor(*world.CLEAR_COLOR)
    glEnable(GL_DEPTH_TEST)
    pyglet.app.run()

