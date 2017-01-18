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
        self.player = Player((32,12,32))
        pyglet.clock.schedule(self.update)


    def update(self, dt):
        self.player.update(dt)


    def on_mouse_motion(self, x, y, dx, dy):
        self.player.on_mouse_motion(x, y, dx, dy)

    def on_mouse_release(self, x, y, button, modifiers):
        vec = self.player.get_sight_vector()
        print(vec)
        block_loc, empty_loc = self.world.hit_test(self.player.loc, vec)
        print(block_loc)
        print(empty_loc)
        if block_loc != None:
            if button == pyglet.window.mouse.RIGHT: #print('LEFT')
                self.world.place_block(empty_loc)
            if button == pyglet.window.mouse.LEFT:
                self.world.del_block(block_loc)


    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.set_exclusive_mouse(False)
        if symbol == key.M:
            self.set_exclusive_mouse(True)
        if symbol == key.Y:
            self.world.del_block(self.player.loc)
        if symbol == key.T:
            self.world.place_block(self.player.loc)
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

    def set2d(self):
        #self.set_projection()
        glColor3f(0.0, 0.0, 0.0);
        glRectf(-0.75,0.75, 0.75, -0.75);


    def on_draw(self):
        """  """
        self.clear()
        self.set3d()
        
        x, y = self.player.rot
        glRotatef(x, 0, 1, 0)
        glRotatef(-y, math.cos(math.radians(x)), 0, math.sin(math.radians(x)))     # Move this elsewhere
        
        x, y, z = self.player.loc                                                  # no need for math library when it's in player class
        glTranslatef(-x,-y,-z)
        
        #self.set2d()

        self.world.batch.draw()



if __name__ == '__main__':
    window = Window(width=600, height=600, resizable=False)
    window.set_exclusive_mouse(True)
    glClearColor(*world.CLEAR_COLOR)
    glEnable(GL_DEPTH_TEST)
    pyglet.app.run()

