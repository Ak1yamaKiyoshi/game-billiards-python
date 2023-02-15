import arcade
import math

# --- Constants ---
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
SCREEN_TITLE = "Cue ball / Billiards"

BALLS_SCALING = 0.35
BOARD_SCALING = 1


class Billiards(arcade.Window):
    def __init__(self) -> None:
        # set up window 
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color((50,100, 100))
        
        self.scene = None        
        self.board = None
        self.cue_balls_list = None
        self.player1_stick1_sprite = None
        self.player1_stick2_sprite = None
        self.mouse_pos_begin = {"x":None, "y":None}
        self.mouse_pos_end = {"x":None, "y":None}
        self.is_dragging_player_cue_ball = None

    def setup(self):
        """ setup for scene"""
        
        # board sprite
        image_src = "sprites/board.png"
        self.board_sprite = arcade.Sprite(image_src, BOARD_SCALING)
        self.board_sprite.center_x = 400
        self.board_sprite.center_y = 500
        
        # cueballs list
        self.cue_balls_list = arcade.SpriteList(use_spatial_hash=False)
        
        b_size = 140*BALLS_SCALING
        balls_start_pos = [
            (400-b_size*2, 700),(400-b_size, 700),(400, 700),(400+b_size, 700),(400+b_size*2, 700),
            (400-b_size/2-b_size, 700-b_size),(400-b_size/2, 700-b_size),(400+b_size/2, 700-b_size),(400+b_size/2+b_size, 700-b_size),
            (400-b_size, 700-b_size*2),(400, 700-b_size*2),(400+b_size, 700-b_size*2),
            (400-b_size/2, 700-b_size*3),(400+b_size/2, 700-b_size*3),
            (400, 700-b_size*4),
        ]
        for i, pos in enumerate(balls_start_pos):
            image_src = "sprites/cue_ball.png"
            cue_ball = arcade.Sprite(image_src, BALLS_SCALING)
            cue_ball.center_x = pos[0]
            cue_ball.center_y = pos[1]
            self.cue_balls_list.append(cue_ball)
            
        cue_ball = arcade.Sprite(image_src, BALLS_SCALING)
        cue_ball.center_x = 400
        cue_ball.center_y = 700-b_size*9
        self.cue_balls_list.append(cue_ball)
        
        self.player1_stick_sprite = arcade.Sprite()

    
    def on_draw(self):
        """ render everything """
        arcade.start_render()
        self.board_sprite.draw()
        self.cue_balls_list.draw()
    
    def on_mouse_motion(self, x, y, dx, dy):
        """ called when mouse moves """
        
    def on_mouse_press(self, x, y, button, modifiers):
        """ called when mouse presed """
        
        ball = arcade.get_sprites_at_point((x, y), self.cue_balls_list)
        if ball == [self.cue_balls_list[15]]:
            self.mouse_pos_begin["x"] = x
            self.mouse_pos_begin["y"] = y
            self.is_dragging_player_cue_ball = True
    
    def on_mouse_release(self, x, y, button, modifiers):
        if self.is_dragging_player_cue_ball:
            self.mouse_pos_end["x"] = x
            self.mouse_pos_end["y"] = y
            print(self.mouse_pos_begin, self.mouse_pos_end)
            angle = math.atan2(self.mouse_pos_end["y"] - self.mouse_pos_begin["y"], self.mouse_pos_end["x"] - self.mouse_pos_begin["x"]) * 180 / math.pi
            dy = self.mouse_pos_end["y"] - self.mouse_pos_begin["y"]
            dx = self.mouse_pos_end["x"] - self.mouse_pos_begin["x"]
            print(f"angle: {angle}, distance: {dy, dx}")
            
            self.cue_balls_list[15].center_x += math.cos(angle)*dx
            self.cue_balls_list[15].center_y += math.sin(angle)*dy
            self.is_dragging_player_cue_ball = None

def main():
    window = Billiards()    
    window.setup()
    arcade.run()
    
if __name__ == "__main__":
    main()