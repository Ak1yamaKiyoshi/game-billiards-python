import arcade 
from math import sqrt

class Window(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.set_location(400, 200)
        arcade.set_background_color(arcade.color.WHITE)
        
        self.width  = width   
        self.height = height 
        
        self.balls = arcade.SpriteList()
        for i in range(15): 
            self.balls.append(arcade.Sprite("./sprites/cue_ball.png", 0.5, hit_box_algorithm="Simple"))
            self.balls[i].center_y = 100
            self.balls[i].center_x = 70+i*75
    def setup(self):
        pass

    def on_draw(self):
        arcade.start_render()
        self.balls.draw()

    def on_update(self, delta_time):
    
        # Move items in the physics engine
        self.physics_engine.step()
                    
    def on_mouse_press(self, x, y, button, modifiers):
        pass

    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_key_press(self, symbol, modifiers):
        pass
    
    def on_key_release(self, symbol, modifiers):
        pass

Window(1280, 720, 'Window')
arcade.run()