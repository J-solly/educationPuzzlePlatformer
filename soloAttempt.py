import arcade

SCREEN_WIDTH = 1250
SCREEN_HEIGHT = 750
SCREEN_TITLE = "my solo attempt"

PLAYER_SPEED = 7
JUMP_SPEED = 25
GRAVITY = 1

class gameAttempt(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.NAVY_BLUE)

        self.player_list = None
        self.wall_list = None
        self.player = None
        self.physics_engine = None
        self.keys_held = set()

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        # setting up player
        player_texture = arcade.make_soft_square_texture(40, arcade.color.RED, outer_alpha=255)
        self.player = arcade.Sprite()
        self.player.texture = player_texture
        self.player.width = 40
        self.player.height = 40
        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = SCREEN_HEIGHT // 2
        self.player_list.append(self.player)

        # setting up environment
        ground_texture = arcade.make_soft_square_texture(SCREEN_WIDTH, arcade.color.GREEN, outer_alpha=255)
        ground = arcade.Sprite()
        ground.texture = ground_texture
        ground.width = SCREEN_WIDTH
        ground.height = 40
        ground.center_x = SCREEN_WIDTH // 2
        ground.center_y = 20
        self.wall_list.append(ground)

        #gravity/physics engine

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player, self.wall_list, gravity_constant=GRAVITY
        )

        #platforms
        for x in range(300, SCREEN_WIDTH - 300, 300):
            platform_texture = arcade.make_soft_square_texture(SCREEN_WIDTH, arcade.color.ASH_GREY, outer_alpha=255)
            platform = arcade.Sprite()
            platform.texture = platform_texture
            platform.width = 150
            platform.height = 20
            platform.center_x = x
            platform.center_y = 250
            self.wall_list.append(platform)

    def on_draw(self):
        self.clear()

        #draws the walls and player
        self.wall_list.draw()
        self.player_list.draw()

    def on_key_press(self, key, modifiers):
        self.keys_held.add(key)
        self.update_player_velocity()
    
    def on_key_release(self, key, modifiers):
        if key in self.keys_held:
            self.keys_held.remove(key)
        self.update_player_velocity()

    def update_player_velocity(self):
        #side to side
        if arcade.key.A in self.keys_held or arcade.key.LEFT in self.keys_held:
            self.player.change_x = -PLAYER_SPEED
        elif arcade.key.D in self.keys_held or arcade.key.RIGHT in self.keys_held:
            self.player.change_x = PLAYER_SPEED
        else:
            self.player.change_x = 0
        
        #jump logic
        if (arcade.key.SPACE in self.keys_held or arcade.key.UP in self.keys_held or arcade.key.W in self.keys_held) and self.physics_engine.can_jump():
            self.player.change_y = JUMP_SPEED
    
    def on_update(self, delta_time):
        self.physics_engine.update()

        #keeps play in screen
        if self.player.left < 0:
            self.player.left = 0
        if self.player.right > SCREEN_WIDTH:
            self.player.right = SCREEN_WIDTH

def main():
    game = gameAttempt()
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()
