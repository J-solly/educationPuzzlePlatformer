import arcade
import random

SCREEN_WIDTH = 1250
SCREEN_HEIGHT = 750
SCREEN_TITLE = "spell game"

PLAYER_SPEED = 6
JUMP_SPEED = 20
GRAVITY = 1

class spellGame(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.SKY_BLUE)

        self.player_list = None
        self.wall_list = None
        self.bullet_list = None
        self.player = None
        self.physics_engine = None
        self.keys_held = set()
        
        # NEW: Keep track of which way the player is facing. Default to RIGHT.
        self.facing_direction = "RIGHT" 
        
    def setup(self):
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()

        #----------------------
        # setting up the player
        #----------------------
        """
        player_texture = arcade.make_soft_circle_texture(40, arcade.color.BLUE, outer_alpha=255)
        self.player = arcade.Sprite()
        self.player.texture = player_texture
        """
        self.player = arcade.SpriteSolidColor(40, 40, color=arcade.color.BLUE)
        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = SCREEN_HEIGHT // 2
        self.player_list.append(self.player)

        #----------------------
        # setting up the ground
        #----------------------
        ground_texture = arcade.make_soft_square_texture(SCREEN_WIDTH, arcade.color.GREEN, outer_alpha=255)
        ground = arcade.Sprite()
        ground.texture = ground_texture
        ground.width = SCREEN_WIDTH
        ground.height = 40
        ground.center_x = SCREEN_WIDTH // 2
        ground.center_y = 20
        self.wall_list.append(ground)

        #-----------------------------
        #setting up the physics engine
        #-----------------------------
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player, self.wall_list, gravity_constant=GRAVITY
        )

        for i in range(1, 10):
            y = random.randint(50, 750)
            x = random.randint(1, 1250)
            platform_texture = arcade.make_soft_square_texture(SCREEN_WIDTH, arcade.color.DARK_GRAY, outer_alpha=255)
            platform = arcade.Sprite()
            platform.texture = platform_texture
            platform.width = 150
            platform.height = 20
            platform.center_x = x
            platform.center_y = y
            self.wall_list.append(platform)
            
    def on_draw(self):
        self.clear()

        self.wall_list.draw()
        self.player_list.draw()
        self.bullet_list.draw()
        
    def on_key_press(self, key, modifier):
        if key == arcade.key.Q:
            # NEW: Made the bullet wide instead of tall (15 wide, 5 tall)
            # NEW FIXED LINE
            bullet = arcade.SpriteSolidColor(15, 5, color=arcade.color.RED)

            # NEW: Center the bullet vertically with the player
            bullet.center_y = self.player.center_y

            # NEW: Check which way we are facing to set position and velocity
            if self.facing_direction == "RIGHT":
                bullet.left = self.player.right # Spawn on the right side of player
                bullet.change_x = 15            # Shoot right
            elif self.facing_direction == "LEFT":
                bullet.right = self.player.left # Spawn on the left side of player
                bullet.change_x = -15           # Shoot left

            # Add the bullet to the list
            self.bullet_list.append(bullet)
        else:
            self.keys_held.add(key)
            self.update_player_velocity()
            
    def on_key_release(self, key, modifier):
        if key in self.keys_held:
            self.keys_held.remove(key)
        self.update_player_velocity()
        
    def update_player_velocity(self):
        #---------------------
        #side to side controls
        #---------------------
        if arcade.key.A in self.keys_held:
            self.player.change_x = -PLAYER_SPEED
            # NEW: Remember that we moved left
            self.facing_direction = "LEFT" 
            
        elif arcade.key.D in self.keys_held:
            self.player.change_x = PLAYER_SPEED
            # NEW: Remember that we moved right
            self.facing_direction = "RIGHT" 
            
        else:
            self.player.change_x = 0

        if (arcade.key.SPACE in self.keys_held) and self.physics_engine.can_jump():
            self.player.change_y = JUMP_SPEED
    
    def on_update(self, delta_time):
        self.physics_engine.update()
        self.bullet_list.update()

        # NEW: Clean up bullets that fly off-screen horizontally instead of vertically
        for bullet in self.bullet_list:
            if bullet.left > SCREEN_WIDTH or bullet.right < 0:
                bullet.remove_from_sprite_lists()

        #--------------------------------
        #keeping the player in the screen
        #--------------------------------
        if self.player.left < 0:
            self.player.left = 0
        if self.player.right > SCREEN_WIDTH:
            self.player.right = SCREEN_WIDTH

def main():
    game = spellGame()
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()