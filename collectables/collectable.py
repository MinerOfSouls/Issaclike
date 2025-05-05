import arcade
#todo sprite details needs to be changed managed by resource handler

#rewrite to use texture animation or use only one row sprites

class Collectable(arcade.Sprite):
    def __init__(self,physics_engine,stats,sprite,sprite_details):
        self.animation_speed = sprite_details[4]
        collectable_sheet = arcade.load_spritesheet(sprite)
        texture_list = collectable_sheet.get_texture_grid(size=(sprite_details[0] , sprite_details[1]), columns=sprite_details[2], count=sprite_details[3])
        super().__init__(texture_list[0],scale=sprite_details[5])
        self.time_elapsed = 0
        self.cur_texture_index =0
        self.textures = texture_list
        self.physics_engine = physics_engine
        self.stats = stats

    def apply_force(self,force):
        self.physics_engine.apply_force(self ,force)

    def update(self, delta_time: float = 1/60, *args, **kwargs):
        self.time_elapsed += delta_time
        if self.time_elapsed > self.animation_speed:
            self.set_texture(self.cur_texture_index)
            self.cur_texture_index = (self.cur_texture_index + 1) % len(self.textures)
            self.time_elapsed = 0
        pass
