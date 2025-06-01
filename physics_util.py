from arcade import Sprite, PymunkPhysicsEngine
import pymunk


def update_sprite(engine: PymunkPhysicsEngine, sprite: Sprite) -> None:
    """
    Updates a Sprite's Shape to match it's current hitbox.
    Credit: Cleptomania from the arcade developer team
    Args:
        sprite: The Sprite to update
        engine: physics engine to preform operation on
    """
    physics_object = engine.sprites[sprite]
    old_shape = physics_object.shape
    assert old_shape is not None, "Tried to update the shape for a Sprite which does not currently have a shape"

    # Set the physics shape to the sprite's hitbox
    poly = sprite.hit_box.points
    scaled_poly = [[x * sprite.scale_x for x in z] for z in poly]
    shape = pymunk.Poly(physics_object.body, scaled_poly, radius=old_shape.radius)  # type: ignore

    shape.collision_type = old_shape.collision_type
    shape.elasticity = old_shape.elasticity
    shape.friction = old_shape.friction

    engine.space.remove(old_shape)
    engine.space.add(shape)
    physics_object.shape = shape
