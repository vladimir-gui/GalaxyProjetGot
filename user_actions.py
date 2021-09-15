from kivy.uix.relativelayout import RelativeLayout


def on_keyboard_down(self, keyboard, keycode, text, modifiers):
    if keycode[1] == "left":
        self.current_speed_x = self.SPEED_X
    if keycode[1] == "right":
        self.current_speed_x = -self.SPEED_X


def on_keyboard_up(self, keyboard, keycode):
    self.current_speed_x = 0


def on_touch_down(self, touch):
    """ active le decalage vaisseau tanque touche appuyée """
    # state_game_over = False
    # state_game_has_started = False

    if not self.state_game_over and self.state_game_has_started:
        if touch.x < self.width / 2:
            self.current_speed_x = self.SPEED_X
        else:
            self.current_speed_x = -self.SPEED_X
    return super(RelativeLayout, self).on_touch_down(touch)  # !! permet de gerer clic dans MainWidget et dependances


def on_touch_up(self, touch):
    self.current_speed_x = 0
