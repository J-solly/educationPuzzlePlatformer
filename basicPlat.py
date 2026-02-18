import arcade

# --- Constants ---
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Basic platformer"

PLAYER_SPEED = 5
JUMP_SPEED = 25
GRAVITY = 1

LEVEL_WIDTH = 2000
LEVEL_HEIGHT = 1200

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.SKY_BLUE)

        self.player_list = None
        self.wall_list = None
        self.player = None
        self.physics_engine = None
        self.keys_held = set()

        # FIXED FOR 3.x: Initialize without arguments.
        # It will automatically match the window size.
        self.camera = arcade.camera.Camera2D()

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        # Player setup
        self.player = arcade.SpriteSolidColor(40, 60, arcade.color.RED)
        self.player.center_x = LEVEL_WIDTH // 2
        self.player.center_y = LEVEL_HEIGHT // 2
        self.player_list.append(self.player)

        # Environment setup
        ground = arcade.SpriteSolidColor(LEVEL_WIDTH, 40, arcade.color.GREEN)
        ground.center_x = LEVEL_WIDTH // 2
        ground.center_y = 20
        self.wall_list.append(ground)

        for x in range(300, LEVEL_WIDTH - 300, 300):
            platform = arcade.SpriteSolidColor(150, 20, arcade.color.BROWN)
            platform.center_x = x
            platform.center_y = 250
            self.wall_list.append(platform)

        # Physics engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player, self.wall_list, gravity_constant=GRAVITY
        )

    def on_draw(self):
        self.clear()
        
        # FIXED FOR 3.x: Tell the window to use this camera's view
        self.camera.use()
        
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
        # Horizontal movement
        if arcade.key.A in self.keys_held or arcade.key.LEFT in self.keys_held:
            self.player.change_x = -PLAYER_SPEED
        elif arcade.key.D in self.keys_held or arcade.key.RIGHT in self.keys_held:
            self.player.change_x = PLAYER_SPEED
        else:
            self.player.change_x = 0

        # Jump logic
        if (arcade.key.SPACE in self.keys_held or arcade.key.UP in self.keys_held) and self.physics_engine.can_jump():
            self.player.change_y = JUMP_SPEED

    def on_update(self, delta_time):
        self.physics_engine.update()

        # FIXED FOR 3.x: To keep the player centered, just set the 
        # camera position to the player's position.
        # This replaces the old viewport math.
        self.camera.position = (self.player.center_x, self.player.center_y)

def main():
    game = MyGame()
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()