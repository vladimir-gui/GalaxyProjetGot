from kivy.app import App
from kivy.graphics import Color, Line
from kivy.properties import NumericProperty
from kivy.uix.widget import Widget


class MainWidget(Widget):
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    VERTICAL_NUMBER_LINES = 7  # nb ligne impaire pour line milieu centrée
    VERTICAL_LINES_SPACING = 0.1  # pourcentage selon largeur ecran
    vertical_lines = []

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.init_vertical_lines()

    def on_parent(self, widget, parent):
        # print(f"Init width : {self.width} - height : {self.height}")
        pass

    def on_size(self, *args):
        """ Taille fenetre temps reel """
        # print(f"Init width : {self.width} - height : {self.height}")
        # self.perspective_point_x = self.width / 2
        # self.perspective_point_y = self.height * 0.75
        self.update_vertical_lines()

    def on_perspective_point_x(self, widget, value):
        """ on_perspective_point_x permet d'appeler directement les variables perspective_point_x """
        print(f"PX : {value}")

    def on_perspective_point_y(self, widget, value):
        print(f"PY : {value}")

    def init_vertical_lines(self):
        """ definition lignes verticales - objet a variables dynamiques donc traité dans le py"""
        with self.canvas:
            Color(1, 1, 1)
            # self.line = Line(points=[100, 0, 100, 100])
            for line in range(0, self.VERTICAL_NUMBER_LINES):
                self.vertical_lines.append(Line())  # ajout des lignes verticales

    def update_vertical_lines(self):
        # self.line.points = [self.perspective_point_x, 0, self.perspective_point_x, 100]
        central_line_x = self.width / 2
        spacing_line_x = self.VERTICAL_LINES_SPACING * self.width
        offset_line = -int(self.VERTICAL_NUMBER_LINES / 2)  # decalage inter ligne
        for line in range(0, self.VERTICAL_NUMBER_LINES):
            x1 = int(central_line_x + offset_line * spacing_line_x)
            y1 = 0
            x2 = x1
            y2 = self.height
            self.vertical_lines[line].points = [x1, y1, x2, y2]
            offset_line += 1


class GalaxyApp(App):
    pass


GalaxyApp().run()
