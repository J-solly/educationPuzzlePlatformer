import arcade
import random

SCREEN_WIDTH = 1250
SCREEN_HEIGHT = 750     
SCREEN_TITLE = "William Test"

PLAYER_SPEED = 10               
JUMP_SPEED = 20
GRAVITY = 1


class one_player_game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH,SCREEN_HEIGHT,SCREEN_TITLE)
        arcade.set_background_color(arcade.color.AIR_FORCE_BLUE)

        self.player_list = None
        self.wall_list = None
        self.player = None
        self.physics_engine = None
        self.keys_held = set()

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()


        player_one_texture = arcade.make_soft_circle_texture(40, arcade.color.AMETHYST, outer_alpha=255)
        self.player_one = arcade.Sprite() 
        self.player_one.texture = player_one_texture
        self.player_one.width = 40
        self.player_one.height = 40
        self.player_one.center_x = SCREEN_WIDTH // 4
        self.player_one.center_y = SCREEN_HEIGHT // 2
        self.player_list.append(self.player_one)

        ground_texture = arcade.make_soft_square_texture(SCREEN_WIDTH, arcade.color.DARK_GREEN, outer_alpha=255)
        ground = arcade.Sprite()
        ground.texture = ground_texture
        ground.width = SCREEN_WIDTH
        ground.height = 40
        ground.center_x = SCREEN_WIDTH // 2
        ground.center_y = 20
        self.wall_list.append(ground)


        self.physics_engine_one = arcade.PhysicsEnginePlatformer(
            self.player_one, self.wall_list, gravity_constant= GRAVITY
        )

        for x in range(300, SCREEN_WIDTH-300, 300):
            y = random.randint(50,200)
            platform_texture = arcade.make_soft_square_texture(SCREEN_WIDTH, arcade.color.DARK_GRAY, outer_alpha=255)
            platform = arcade.Sprite()
            platform.texture = platform_texture
            platform.width = 150
            platform.height = 20
            platform.center_x = x
            platform.center_y = y
    def on_draw(self):
        self.clear()

        self.wall_list.draw()
        self.player_list.draw()
    
    def on_key_press(self, key, modifier):
        self.keys_held.add(key)
        self.update_player_velocity()

    def on_key_release(self, key, modifier):
        if key in self.keys_held:                
            self.keys_held.remove(key)
        self.update_player_velocity()
    
    def update_player_velocity(self):
        if arcade.key.LEFT in self.keys_held:
            self.player_one.change_x = -PLAYER_SPEED
        elif arcade.key.RIGHT in self.keys_held:
            self.player_one.change_x = PLAYER_SPEED
        else:
            self.player_one.change_x = 0

        if(arcade.key.UP in self.keys_held) and self.physics_engine_one.can_jump():
            self.player_one.change_y = JUMP_SPEED

    def on_update(self, delta_time):
        self.physics_engine_one.update()
        self.physics_engine_one.update()

        if self.player_one.left < 0:
            self.player_one.left = 0
        if self.player_one.right > SCREEN_WIDTH:
            self.player_one.right = SCREEN_WIDTH

def main():
    game = one_player_game()
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()

    
            




    


