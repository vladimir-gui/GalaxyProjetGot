from kivy import Config, platform

# """ taille fenetre par defaut"""

Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '400')

from kivy.core.window import Window
from kivy.app import App
from kivy.graphics import Color, Line
from kivy.properties import NumericProperty, Clock
from kivy.uix.widget import Widget


class MainWidget(Widget):
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    VERTICAL_NUMBER_LINES = 10
    VERTICAL_LINES_SPACING = 0.25  # pourcentage selon largeur ecran
    vertical_lines = []

    HORIZONTAL_NUMBER_LINES = 10
    HORIZONTAL_LINES_SPACING = 0.10  # pourcentage selon largeur ecran
    horizontal_lines = []

    SPEED_OFFSET_Y = 4
    current_offset_y = 0

    MOVE_SPEED_X = 12
    current_speed_x = 0
    current_offset_x = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_vertical_lines()
        self.init_horizontal_lines()

        if self.is_desktop():  # clavier sur desktop uniquement
            self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self._keyboard.bind(on_key_down=self.on_keyboard_down)
            self._keyboard.bind(on_key_up=self.on_keyboard_up)
            Clock.schedule_interval(self.update, 1.0 / 60.0)  # rafraichissement 60 fps

    def keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def is_desktop(self):
        if platform in ('linux', 'win', 'macosx'):
            return True
        return False

    def on_parent(self, widget, parent):
        # print(f"Init width : {self.width} - height : {self.height}")
        pass

    def on_size(self, *args):
        pass
        # """ Taille fenetre temps reel """
        # # print(f"Init width : {self.width} - height : {self.height}")
        # # self.perspective_point_x = self.width / 2
        # # self.perspective_point_y = self.height * 0.75
        # self.update_vertical_lines()
        # self.update_horizontal_lines()

    def on_perspective_point_x(self, widget, value):
        pass
        # """ on_perspective_point_x permet d'appeler directement les variables perspective_point_x """
        # print(f"PX : {value}")

    def on_perspective_point_y(self, widget, value):
        pass
        # print(f"PY : {value}")

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
        offset_line = -int(self.VERTICAL_NUMBER_LINES / 2) + 0.5  # decalage inter ligne ( 0.5 pour centrer sur chemin)
        for vertical_line in range(0, self.VERTICAL_NUMBER_LINES):
            line_x = int(central_line_x + offset_line * spacing_line_x + self.current_offset_x)
            x1, y1 = self.transform(line_x, 0)
            x2, y2 = self.transform(line_x, self.height)
            self.vertical_lines[vertical_line].points = [x1, y1, x2, y2]
            offset_line += 1

    def init_horizontal_lines(self):
        """ definition lignes horizontales - objet a variables dynamiques donc traité dans le py"""
        with self.canvas:
            Color(1, 1, 1)
            for line in range(0, self.HORIZONTAL_NUMBER_LINES):
                self.horizontal_lines.append(Line())  # ajout des lignes horizontales

    def update_horizontal_lines(self):
        central_line_x = self.width / 2
        spacing_line_x = self.VERTICAL_LINES_SPACING * self.width
        offset_line = -int(self.VERTICAL_NUMBER_LINES / 2) + 0.5  # decalage inter ligne ( 0.5 pour centrer sur chemin)

        xmin = central_line_x + offset_line * spacing_line_x + self.current_offset_x
        xmax = central_line_x - offset_line * spacing_line_x + self.current_offset_x
        spacing_y = self.HORIZONTAL_LINES_SPACING * self.height
        for horizontal_line in range(0, self.HORIZONTAL_NUMBER_LINES):
            line_y = horizontal_line * spacing_y - self.current_offset_y  # current_offset_y decale ligne
            x1, y1 = self.transform(xmin, line_y)
            x2, y2 = self.transform(xmax, line_y)
            self.horizontal_lines[horizontal_line].points = [x1, y1, x2, y2]

    def transform(self, x, y):
        """choix affichage 2D ou perspective"""
        # return self.transform_2D(x, y)
        return self.transform_perspective(x, y)

    def transform_2D(self, x, y):
        """choix affichage 2D"""
        return int(x), int(y)

    def transform_perspective(self, pt_x, pt_y):
        """choix affichage 2D ou perspective"""
        linear_y = pt_y * self.perspective_point_y / self.height

        diff_x = pt_x - self.perspective_point_x
        diff_y = self.perspective_point_y - linear_y
        factor_y = diff_y / self.perspective_point_y
        # factor_y = factor_y * factor_y
        factor_y = pow(factor_y, 2)  # pow = mise au carre

        transfor_x = self.perspective_point_x + diff_x * factor_y
        transfor_y = self.perspective_point_y - factor_y * self.perspective_point_y

        return int(transfor_x), int(transfor_y)

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

    def update(self, dt):
        # print(f"dt: {dt*60} - 1/60 : {1}")
        time_factor = dt*60  # permet de corriger la vitesse d'affichage pour avoir toujours un ressenti de 60fps !
        self.update_vertical_lines()
        self.update_horizontal_lines()

        self.current_offset_y += self.SPEED_OFFSET_Y * time_factor # fais defiler lignes horizontales

        spacing_y = self.HORIZONTAL_LINES_SPACING * self.height
        """ simule lignes infinis"""
        if self.current_offset_y >= spacing_y:
            self.current_offset_y -= spacing_y

        # self.current_offset_x += self.MOVE_SPEED_X * time_factor  # fais defiler lignes verticales
        self.current_offset_x += self.current_speed_x * time_factor  # fais defiler lignes verticales


class GalaxyApp(App):
    pass


GalaxyApp().run()
