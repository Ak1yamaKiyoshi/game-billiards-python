import arcade
import pymunk

class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.space = pymunk.Space()
        self.space.gravity = (0, -1000)
        self.rectangles = []

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            body = pymunk.Body(10, 100)
            body.position = x, y
            shape = pymunk.Poly.create_box(body, (50, 50))
            self.space.add(body, shape)
            self.rectangles.append(shape)

    def on_draw(self):
        arcade.start_render()
        for rectangle in self.rectangles:
            x, y = rectangle.body.position
            w, h = rectangle.get_vertices()[2] - rectangle.get_vertices()[0]
            arcade.draw_rectangle_filled(x, y, w, h, arcade.color.RED)

    def on_update(self, delta_time):
        self.space.step(delta_time)

if __name__ == '__main__':
    game = MyGame(800, 600, 'Rectangle on Mouse Press')
    arcade.run()