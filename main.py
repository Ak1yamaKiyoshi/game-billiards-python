import arcade 
import pymunk 
from math import sqrt


class Ball:
    def __init__(self, body, shape, color=(255, 255, 255)):
        self.body = body
        self.shape = shape
        self.color = color
    
    def draw(self):
        x, y = self.body.position
        r = self.shape.radius
        arcade.draw_circle_filled(x, y, r, self.color)
    
    
class Rect:
    def __init__(self, body, shape, color=(255, 255, 255)):
        self.body = body
        self.shape = shape
        self.color = color
    
    def draw(self):
        x, y = self.body.position
        w, h = self.shape.get_vertices()[2] - self.shape.get_vertices()[0]
        arcade.draw_rectangle_filled(x, y, w, h, self.color)
    

class Window(arcade.Window):
    def __init__(self):
        super().__init__(500, 700, 'Window')
        
        #self.set_location(start_x, 200)
        arcade.set_background_color(arcade.color.BLACK)
        
        # Windows size
        self.width  = 500
        self.height = 700 
        
        # objects in simulaton
        self.balls = []     
        self.walls = []
        self.cue_stick = None
        
        # Balls variables
        self.ball_radius = 15
        self.ball_friction = 0.01
        self.ball_elasticity = 0.8
        self.ball_momentum = 10
        self.ball_mass = 10
        self.ball_color = (255, 255, 255)
        self.ball_player_color = (255, 60, 60)
        self.ball_damping = 0
        
        # Walls variables
        self.wall_color = (60, 60, 60)
        
        # Cue Stick variables 
        self.cue_stick_width = 100
        self.cue_stick_height = 10
        self.cue_stick_color = (255, 255, 255)
        self.cue_stick_friction = 0.9
        self.cue_stick_elasticity = 0.001
        self.cue_stick_is_moving = False
        self.cue_stick_start_pos = [0, 0]
        self.cue_stick_end_pos = [0, 0]
        self.cue_stick_delta_pos = [0, 0]
        self.cue_stick_flag = False
        self.cue_stick_counter = 0
        
        # Set up space
        self.space = pymunk.Space()
        self.space.gravity = (0 , 0)
        self.space.damping = 0.7
        

        # setup everything
        self.setup() 
        
    
    def add_static_rect(self, space, x, y, width, height, color=(255,255,255)):
        """ Adds rectangle with given parameters to given space, returns Rect(body, shape) object """
       
        # Create rectangle
        body = pymunk.Body(10, 100, pymunk.Body.STATIC)
        body.position = x, y
        shape = pymunk.Poly.create_box(body, (width, height))
        
        # add to space and append to rects
        space.add(body, shape)
        return Rect(body, shape, color)
    
    
    def add_KINEMATIC_rect(self, space, x, y, width, height, friction=0.5, elasticity=0, color=(255, 255, 255)):
        """ Adds rectangle with given parameters to given space, returns Rect(body, shape) object """
       
        # Create rectangle
        body = pymunk.Body(0, 0, pymunk.Body.KINEMATIC)
        body.position = x, y
        shape = pymunk.Poly.create_box(body, (width, height))
        
        shape.elasticity = elasticity
        shape.friction = friction
        
        # add to space and append to rects
        space.add(body, shape)
        return Rect(body, shape, color)


    def add_dynamic_ball(self, space, x, y, radius, mass=10, momentum=30, friction=0.5, elasticity=0, color=(255, 255, 255)):
        """ Adds circle with given parameters to given space, returns Ball(body, shape) object  """
        
        # Create ball
        body = pymunk.Body(mass, momentum)
        body.position = x, y
        shape = pymunk.Circle(body, radius)
        
        # Ball properties 
        shape.elasticity = elasticity
        shape.friction = friction
        
        # Add ball to balls array and to space
        space.add(body, shape)
        return Ball(body, shape, color)


    def add_cue_stick(self, space, x, y):
        self.cue_stick = self.add_KINEMATIC_rect(space, x, y, 
                                self.cue_stick_width, self.cue_stick_height, 
                                self.cue_stick_friction, self.cue_stick_elasticity,
                                self.cue_stick_color)
        

    def setup_walls(self): 
        """ Adds rects on the edges of screen and appends it to self.space and self.rects """
        
        # Create walls
        wall_rects = [(self.width//2, 0, self.width, 10),(0, self.height//2, 10, self.height),(self.width//2, self.height, self.width, 10),(self.width, self.height//2, 10, self.height)]
        for i in wall_rects:
            self.walls.append(
                self.add_static_rect(self.space, i[0], i[1], i[2], i[3], self.wall_color)
            )
        
    def setup_balls(self):
        """ Adds balls in triangle formation to self.space """
        
        # Ball start possitions 
        start_x = self.width//2
        start_y = (self.height//2)*1.5
        balls_start_pos = [(start_x-self.ball_radius, start_y),(start_x-self.ball_radius, start_y),(start_x, start_y),(start_x+self.ball_radius, start_y),(start_x+self.ball_radius*2, start_y),(start_x-self.ball_radius/2-self.ball_radius, start_y-self.ball_radius),(start_x-self.ball_radius/2, start_y-self.ball_radius),(start_x+self.ball_radius/2, start_y-self.ball_radius),(start_x+self.ball_radius/2+self.ball_radius, start_y-self.ball_radius),(start_x-self.ball_radius, start_y-self.ball_radius*2),(start_x, start_y-self.ball_radius*2),(start_x+self.ball_radius, start_y-self.ball_radius*2),(start_x-self.ball_radius/2, start_y-self.ball_radius*3),(start_x+self.ball_radius/2, start_y-self.ball_radius*3),(start_x, start_y-self.ball_radius*4) ]
        
        # Create balls
        for (x, y) in balls_start_pos: 
            self.balls.append(
                self.add_dynamic_ball(self.space, x, y, self.ball_radius, self.ball_mass, 
                                    self.ball_momentum, self.ball_friction, self.ball_elasticity,
                                    self.ball_color))
        # Player Ball 
        self.balls.append(
            self.add_dynamic_ball(self.space, start_x, start_y/2, self.ball_radius, self.ball_mass, 
                                self.ball_momentum, self.ball_friction, self.ball_elasticity,
                                self.ball_player_color))


    def setup(self):
        self.setup_balls()
        self.setup_walls()


    def draw_balls(self):
        for obj in self.balls:
            obj.draw()
    
    
    def draw_walls(self):
        for obj in self.walls:
            obj.draw()
            
    def draw_cue_stick(self):
        if self.cue_stick:
            self.cue_stick.draw()
    
    def on_draw(self):
        arcade.start_render()
        self.draw_balls()
        self.draw_walls()
        self.draw_cue_stick()
        
        
        
    def process_cue_stick_movement(self):
        if self.cue_stick_is_moving:
            self.cue_stick_counter += 1
            if self.cue_stick_counter > 10:
                self.space.remove(self.cue_stick.shape)
                self.cue_stick = None   
                self.cue_stick_counter = 0
                self.cue_stick_is_moving = False

    
        
    def on_update(self, delta_time):
        self.space.step(delta_time)
        self.process_cue_stick_movement()
    

    def on_mouse_press(self, x, y, button, modifiers):
        self.cue_stick_start_pos = [x, y]
 
        self.add_cue_stick(self.space, x, y)
        pass
        
    def on_mouse_release(self, x, y, button, modifiers):
        self.cue_stick_end_pos = [x, y]
        self.cue_stick_is_moving = True
        delta = [0,0]
        delta[0] = self.cue_stick_end_pos[0] - self.cue_stick_start_pos[0]
        delta[1] = self.cue_stick_end_pos[1] - self.cue_stick_start_pos[1]
        self.cue_stick_delta_pos = delta
        self.cue_stick.body.velocity = [delta[0]*2, delta[1]*2]
        pass







    
    def on_key_press(self, symbol, modifiers):
        pass
    
    
    def on_mouse_motion(self, x, y, dx, dy):
        pass   



    
    def on_key_release(self, symbol, modifiers):
        pass


Window()
arcade.run()

""" 
Ideas 

"""