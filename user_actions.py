def on_keyboard_down(self, keyboard, keycode, text, modifiers):
    if keycode[1] == "left":
        self.current_speed_x = self.MOVE_SPEED_X
    if keycode[1] == "right":
        self.current_speed_x = -self.MOVE_SPEED_X


def on_keyboard_up(self, keyboard, keycode):
    self.current_speed_x = 0


def on_touch_down(self, touch):
    """ active le decalage vaisseau tanque touche appuyée """
    if touch.x < self.width / 2:
        self.current_speed_x = self.MOVE_SPEED_X
    else:
        self.current_speed_x = -self.MOVE_SPEED_X


def on_touch_up(self, touch):
    self.current_speed_x = 0