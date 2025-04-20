# import arcade
# from rooms import Map
# class PhysicsHandler:
#     def __init__(self, physics_engine,playerSpirete, map:Map):
#         self.physics_engine = physics_engine
#         self.map = map
#
#     def on_setup(self):
#         def door_player_handler(sprite_a, sprite_b, arbiter, space, data):
#
#             door = arbiter.shapes[0]
#             self.map.change_room(sprite_a, space)
#             print("Rock")
#
#         self.physics_engine.add_collision_handler(
#             "bullet",
#             "rock",
#             post_handler=door_player_handler(),
#         )
#