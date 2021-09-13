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
    from transforms import transform, transform_2D, transform_perspective
    from user_actions import on_keyboard_up, on_keyboard_down, on_touch_down, on_touch_up
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    VERTICAL_NUMBER_LINES = 4
    VERTICAL_LINES_SPACING = 0.1  # pourcentage selon largeur ecran
    vertical_lines = []

    HORIZONTAL_NUMBER_LINES = 8
    HORIZONTAL_LINES_SPACING = 0.15  # pourcentage selon largeur ecran
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
        self._keyboard.unbind(on_key_up=self._on_keyboard_down)
        self._keyboard = None

    def is_desktop(self):
        if platform in ('linux', 'win', 'macosx'):
            return True
        return False

    def init_vertical_lines(self):
        """ definition lignes verticales - objet a variables dynamiques donc traité dans le py"""
        with self.canvas:
            Color(1, 1, 1)
            # self.line = Line(points=[100, 0, 100, 100])
            for line in range(0, self.VERTICAL_NUMBER_LINES):
                self.vertical_lines.append(Line())  # ajout des lignes verticales

    def get_line_x_from_index(self, index):
        central_line_x = self.perspective_point_x
        spacing_line_x = self.VERTICAL_LINES_SPACING * self.width
        offset_line = index - 0.5  # decalage inter ligne ( 0.5 pour centrer sur chemin)
        line_x = central_line_x + offset_line * spacing_line_x + self.current_offset_x
        return line_x

    def update_vertical_lines(self):
        # -1 0 1 2 -- si VERTICAL_NUMBER_LINES = 4
        start_index = -int(self.VERTICAL_NUMBER_LINES / 2) + 1
        for vertical_line in range(start_index, start_index+self.VERTICAL_NUMBER_LINES):
            line_x = self.get_line_x_from_index(vertical_line)
            x1, y1 = self.transform(line_x, 0)
            x2, y2 = self.transform(line_x, self.height)
            self.vertical_lines[vertical_line].points = [x1, y1, x2, y2]

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

    def update(self, dt):
        # print(f"dt: {dt*60} - 1/60 : {1}")
        time_factor = dt*60  # permet de corriger la vitesse d'affichage pour avoir toujours un ressenti de 60fps !
        self.update_vertical_lines()
        self.update_horizontal_lines()

        # self.current_offset_y += self.SPEED_OFFSET_Y * time_factor # fais defiler lignes horizontales

        spacing_y = self.HORIZONTAL_LINES_SPACING * self.height
        """ simule lignes infinis"""
        if self.current_offset_y >= spacing_y:
            self.current_offset_y -= spacing_y

        # self.current_offset_x += self.current_speed_x * time_factor  # fais defiler lignes verticales


class GalaxyApp(App):
    pass


GalaxyApp().run()
