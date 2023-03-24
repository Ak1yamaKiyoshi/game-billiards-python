import arcade 
import pymunk 
import math


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
        a = math.degrees(self.body.angle*-1)
        arcade.draw_rectangle_filled(x, y, w, h, self.color, a)
    
    
class RectIllusin: 
    def __init__(self, x, y, width, height, color, angle=0):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.angle=math.degrees(angle*-1)
        
    def draw(self):
        arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height, self.color, self.angle)


class Window(arcade.Window):
    def __init__(self):
        super().__init__(500, 700, 'Window')
        
        # window variables
        arcade.set_background_color(arcade.color.AMAZON)
        
        # Windows size
        self.width  = 800
        self.height = 800
        
        # objects in simulaton
        self.balls = []     
        self.walls = []
        self.holes = []
        self.cue_stick = None
        self.cue_stick_trail = None
        
        self.simulation_body_types = {
            "dynamic":pymunk.Body.DYNAMIC,
            "kinematic":pymunk.Body.KINEMATIC,
            "static":pymunk.Body.STATIC
        }
        
        # Balls variables
        self.ball_radius = 10
        self.ball_friction = 0.01
        self.ball_elasticity = 0.8
        self.ball_momentum = 10
        self.ball_mass = 10
        self.ball_color = (255, 255, 255)
        self.ball_player_color = (255, 60, 60)
        
        # Walls variables
        self.wall_color = (60, 60, 60)
        self.wall_friction = 0
        self.wall_elasticity = 0.9999999
        self.wall_horizontal_offset = 200
        self.wall_vertical_offset = 100
        
        # Hole variables
        self.hole_color = (20, 20, 20)
        self.hole_offset = 15

        # Cue Stick variables 
        self.cue_stick_width = self.ball_radius 
        self.cue_stick_height = 10
        self.cue_stick_color = (255, 255, 255)
        self.cue_stick_friction = 0.9
        self.cue_stick_elasticity = 0.00001
        self.cue_stick_is_moving = False
        self.cue_stick_start_pos = [0, 0]
        self.current_delta_between_stick_and_player_ball = None
        
        # Set up space
        self.space = pymunk.Space()
        self.space.gravity = (0 , 0)
        self.space.damping = 0.4666

        self.score = 0

        # setup everything
        self.setup() 
        
        
    def add_rect(self, space, x, y, width, height, friction=0.5, elasticity=0.5, color=(255, 255, 255), angle=0, type = "DYNAMIC"):
        """  """
        # Create rectangle body with given body type 
        body = pymunk.Body(10, 100, self.simulation_body_types[type.lower()])
        #   body properties 
        body.position = x, y
        body.angle = angle
        # Create rectangle shape 
        shape = pymunk.Poly.create_box(body, (width, height))
        #   rectangle properties 
        shape.elasticity = elasticity
        shape.friction = friction
        # add rectangle to simulation 
        space.add(body, shape) 
        # Return Rect object with draw methods
        return Rect(body, shape, color=color) 


    def add_ball(self, space, x, y, radius, mass=10, momentum=30, friction=0.5, elasticity=0, color=(255, 255, 255), type = "DYNAMIC"):
        """  """
        # Create ball body with given body type 
        body = pymunk.Body(mass, momentum, self.simulation_body_types[type.lower()])
        #   body properties 
        body.position = x, y
        # Create ball shape 
        shape = pymunk.Circle(body, radius)
        #   ball properties 
        shape.elasticity = elasticity
        shape.friction = friction
        # add rectangle to simulation 
        space.add(body, shape)
        # Return Rect object with draw methods
        return Ball(body, shape, color)
    
    def remove_ball(self, ball):
        self.space.remove(ball.shape)
        self.balls[self.balls.index(ball)]       = None

    def distance_between_two_coordinates(self, pos1, pos2):
            return (pos2[1] - pos1[1])+(pos2[0] - pos1[0])


    def calculate_angle_between_cue_stick_start_pos_and_player_ball(self):
        pos1 = self.cue_stick_start_pos
        pos2 = self.balls[-1].body.position
        try:
            return math.atan((pos2[1] - pos1[1])/(pos2[0] - pos1[0]))
        except:
            return 0

    def cue_stick_remove(self):
        # Remove cue stick shape from simulation 
        self.space.remove(self.cue_stick.shape)
        # Reset parameters 
        self.cue_stick = None   
        self.cue_stick_is_moving = False
        self.current_delta_between_stick_and_player_ball = None  


    def cue_stick_update(self):
        # If cue stick exists and if its moving 
        if self.cue_stick_is_moving and self.cue_stick:
            # Get current position of cue stick and ball
            pos1 = self.cue_stick.body.position
            pos2 = self.balls[-1].body.position
            """ 
            save prev delta compare with current, 
            if they >=,  delete stick, 
            else, ignore (stick still not touched the ball, and still not missed yet)
            """
            # calculate current delta
            currentDelta = round(math.sqrt(math.pow((pos2[0] - pos1[0]), 2) + math.pow((pos2[1] - pos1[1]), 2)), 0)
            # if delta is increasing, or equals that means that stick missed or touched the ball 
            if self.current_delta_between_stick_and_player_ball and currentDelta >= self.current_delta_between_stick_and_player_ball:
                self.cue_stick_remove() 
                return
            # update current delta field  
            self.current_delta_between_stick_and_player_ball = currentDelta
        
        
    def cue_stick_update_angle(self):
        if self.cue_stick:
            self.cue_stick.body.angle = self.calculate_angle_between_cue_stick_start_pos_and_player_ball()
        
    def add_cue_stick(self, space, x, y):
        self.cue_stick = self.add_rect(space, x, y, 
                                self.cue_stick_width, self.cue_stick_height, 
                                self.cue_stick_friction, self.cue_stick_elasticity,
                                self.cue_stick_color, 
                                self.calculate_angle_between_cue_stick_start_pos_and_player_ball(),
                                "KINEMATIC"
                                )
    
    def setup_walls(self): 
        # Create walls
        wall_rects = [(self.width//2, 0+self.wall_vertical_offset, self.width-self.wall_horizontal_offset*2, 10),
                      (self.wall_horizontal_offset , self.height//2, 10, self.height-self.wall_vertical_offset*2),
                      (self.width//2, self.height-self.wall_vertical_offset, self.width-self.wall_horizontal_offset*2, 10),
                      (self.width-self.wall_horizontal_offset , self.height//2, 10, self.height-self.wall_vertical_offset*2)
                    ]
        for i in wall_rects:
            self.walls.append(
                self.add_rect(self.space, i[0], i[1], i[2], i[3], self.wall_friction, self.wall_elasticity, self.wall_color, type="STATIC")
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
                self.add_ball(self.space, x, y, self.ball_radius, self.ball_mass, 
                                    self.ball_momentum, self.ball_friction, self.ball_elasticity,
                                    self.ball_color))
        # Player Ball 
        self.balls.append(
            self.add_ball(self.space, start_x, start_y/2, self.ball_radius, self.ball_mass, 
                                self.ball_momentum, self.ball_friction, self.ball_elasticity,
                                self.ball_player_color))
        
    def setup_holes(self):
        # Left Holes
        self.holes.append(RectIllusin(self.hole_offset + self.wall_horizontal_offset, 
                                    self.hole_offset+self.wall_vertical_offset,self.ball_radius*2 ,   
                                    self.ball_radius*2,     
                                    self.hole_color))
        self.holes.append(RectIllusin(self.hole_offset + self.wall_horizontal_offset, 
                                    self.height-self.hole_offset-self.wall_vertical_offset,        
                                    self.ball_radius*2,     
                                    self.ball_radius*2,self.hole_color))
        # Right Holes
        self.holes.append(RectIllusin(self.width-self.hole_offset-self.wall_horizontal_offset, 
                                      self.height -self.hole_offset -self.wall_vertical_offset,
                                      self.ball_radius*2,self.ball_radius*2,
                                      self.hole_color))
        self.holes.append(RectIllusin(self.width-self.hole_offset-self.wall_horizontal_offset,
                                      self.hole_offset+self.wall_vertical_offset,
                                      self.ball_radius*2,self.ball_radius*2,
                                      self.hole_color))  
        # Middle holes
        self.holes.append(RectIllusin(self.width-self.hole_offset-self.wall_horizontal_offset, 
                                      self.height/2 -self.hole_offset ,
                                      self.ball_radius*2,
                                      self.ball_radius*2,self.hole_color))
        self.holes.append(RectIllusin(10+self.wall_horizontal_offset,
                                      self.height/2 -self.hole_offset ,
                                      self.ball_radius*2,
                                      self.ball_radius*2,
                                      self.hole_color))
    
    def balls_check_if_collide_with_holes(self):
        for ball in self.balls:
            if ball:
                b_x = ball.body.position[0]
                b_y = ball.body.position[1]
                for hole in self.holes:
                    if b_x > hole.x and b_x < hole.x + hole.width:
                        if b_y >= hole.y-5 and b_y < hole.y + hole.height:
                            self.remove_ball(ball)  
                            self.score += 1

    def setup(self):
        self.setup_balls()
        self.setup_walls()
        self.setup_holes()
        
        
    def draw_holes(self):
        for obj in self.holes:
            obj.draw()


    def draw_balls(self):
        for obj in self.balls:
            if obj: obj.draw()
    
    
    def draw_walls(self):
        for obj in self.walls:
            obj.draw()
            
            
    def draw_cue_stick(self):
        if self.cue_stick:
            self.cue_stick.draw()
    
    
    def draw_cue_stick_trail(self):
        if self.cue_stick_trail:
            self.cue_stick_trail.draw()
    
    
    def on_draw(self):
        arcade.start_render()
        self.draw_balls()
        self.draw_walls()
        self.draw_holes()
        self.draw_cue_stick()
        self.draw_cue_stick_trail()
        arcade.draw_text(f"Score: {self.score}",
                    self.width/2-150,
                    10,
                    arcade.color.BLACK,
                    50,
                    width=300,
                    align="center")

    def on_update(self, delta_time): 
        self.space.step(delta_time)
        self.cue_stick_update()
        self.cue_stick_update_angle()
        self.cue_stick_trail_update()
        self.balls_check_if_collide_with_holes()



    def on_mouse_press(self, x, y, button, modifiers):
        if not self.cue_stick:
            self.cue_stick_start_pos = [x, y]
            self.add_cue_stick(self.space, x, y)

            
    def cue_stick_trail_update(self):
        if self.cue_stick and not self.cue_stick_is_moving:
            self.cue_stick_trail = None
            ball_pos = self.balls[-1].body.position
            self.cue_stick_trail = RectIllusin(
                self.cue_stick.body.position[0],
                self.cue_stick.body.position[1],
                self.distance_between_two_coordinates( ball_pos, self.cue_stick.body.position*100),
                5,
                (50, 255, 100),
                self.calculate_angle_between_cue_stick_start_pos_and_player_ball()
            )
            
            
    def on_mouse_motion(self, x, y, dx, dy):
        if self.cue_stick and not self.cue_stick_is_moving:
            self.cue_stick_start_pos = [x, y]
            self.cue_stick.body.position = [x, y]
            
        
    def on_mouse_release(self, x, y, button, modifiers):
        if self.cue_stick:
            self.cue_stick_is_moving = True
            delta = [0, 0]

            ball_pos = self.balls[-1].body.position
            delta[0] = ball_pos[0] - self.cue_stick_start_pos[0]
            delta[1] = ball_pos[1] - self.cue_stick_start_pos[1]
            self.cue_stick.body.velocity = [delta[0]*3, delta[1]*3]
            self.cue_stick_trail = None
        
        
Window()
arcade.run()