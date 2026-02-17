import arcade

SCREEN_WIDTH = 1000
SCREEN_HEIGHT= 600
SCREEN_TITLE = "A Basic Platformer"

class myGame(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.SKY_BLUE)