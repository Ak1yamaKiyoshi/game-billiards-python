import arcade 

# constants 
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
SCREEN_TITLE = "Billiards"
BALLS_SCALING = 0.5
BOARD_SCALING = 1

class Billiards(arcade.Window): 
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        # Call the parent class and set up the window
        arcade.set_background_color((50 ,100, 100))
        
        
        # Array of ball sprites 
        self.balls_sprite_list = None
        
        self.board_sprite = None
    
    def setup(self):
        # board sprite
        image_src = "sprites/board.png"
        self.board_sprite = arcade.Sprite(image_src, BOARD_SCALING)
        self.board_sprite.center_x = 400
        self.board_sprite.center_y = 500
        
                
        # cueballs list
        self.balls_sprite_list = arcade.SpriteList(use_spatial_hash=True)
        
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
            self.balls_sprite_list.append(cue_ball)
            
        cue_ball = arcade.Sprite(image_src, BALLS_SCALING)
        cue_ball.center_x = 400
        cue_ball.center_y = 700-b_size*9
        self.balls_sprite_list.append(cue_ball)

        
    
    def on_mouse_click(self):
        pass
    
    def on_draw(self):
        self.balls_sprite_list.draw()
        self.board_sprite.draw()
    
def main():
    window = Billiards()
    window.setup()
    arcade.run()
    
if __name__ == "__main__":
    main()