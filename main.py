from kivy.app import App
from kivy.properties import NumericProperty
from kivy.uix.widget import Widget


class MainWidget(Widget):
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        # print(f"Init width : {self.width} - height : {self.height}")

    def on_parent(self, widget, parent):
        # print(f"Init width : {self.width} - height : {self.height}")
        pass

    def on_size(self, *args):
        """ Taille fenetre temps reel """
        # print(f"Init width : {self.width} - height : {self.height}")
        # self.perspective_point_x = self.width / 2
        # self.perspective_point_y = self.height * 0.75
        pass

    def on_perspective_point_x(self, widget, value):
        """ on_perspective_point_x permet d'appeler directement les variables perspective_point_x """
        print(f"PX : {value}")

    def on_perspective_point_y(self, widget, value):
        print(f"PY : {value}")


class GalaxyApp(App):
    pass

GalaxyApp().run()
