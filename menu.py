from kivy.uix.relativelayout import RelativeLayout


class MenuWidget(RelativeLayout):
    """ relativeLayout utilise directement la taille du parent"""

    def on_touch_down(self, touch):
        """ desactive le bouton sur game over = opacite 0 """
        if self.opacity == 0:
            return False
        return super(RelativeLayout, self).on_touch_down(touch)
