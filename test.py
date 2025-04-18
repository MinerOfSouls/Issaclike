import arcade
from arcade.gui import UIManager

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(800, 600, "Game Menu Example")
        self.ui_manager = UIManager()

    def on_draw(self):
        arcade.start_render()
        self.ui_manager.on_draw()

    def setup(self):
        label = arcade.gui.UILabel(400, 550, "Slider Value: 0", font_size=20)
        self.ui_manager.add_ui_element(label)

        slider = arcade.gui.UISlider(400, 450, 200, 20, min_value=0, max_value=100, value=0)
        slider.on_update = self.on_slider_update
        self.ui_manager.add_ui_element(slider)

    def on_slider_update(self, value):
        self.ui_manager.get_element_by_id("label").text = f"Slider Value: {value}"

def main():
    game = MyGame()
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()