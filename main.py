from kivy import Config, platform

# """ taille fenetre par defaut"""

Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '400')

from kivy.core.window import Window
from kivy.app import App
from kivy.graphics import Color, Line, Quad
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

    SPEED_OFFSET_Y = 1
    current_offset_y = 0
    current_y_loop = 0

    MOVE_SPEED_X = 12
    current_speed_x = 0
    current_offset_x = 0

    """ definition tuile tile """
    tile = None  # forme QUAD
    tile_x = 1
    tile_y = 2

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_vertical_lines()
        self.init_horizontal_lines()
        self.init_tiles()

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

    def init_tiles(self):
        """ creation de la tuile a suivre pour gagner """
        with self.canvas:
            Color(1, 1, 1)
            self.tile = Quad()

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

    def get_line_y_from_index(self, index):
        spacing_line_y = self.HORIZONTAL_LINES_SPACING * self.height
        line_y = index * spacing_line_y - self.current_offset_y
        return line_y

    def get_tile_coordinates(self, tile_x, tile_y):
        tile_y = tile_y - self.current_y_loop
        x = self.get_line_x_from_index(tile_x)
        y = self.get_line_y_from_index(tile_y)
        return x, y

    def update_tiles(self):
        xmin, ymin = self.get_tile_coordinates(self.tile_x, self.tile_y)
        xmax, ymax = self.get_tile_coordinates(self.tile_x + 1, self.tile_y + 1)

        # 2     3
        #
        # 1     4
        x1, y1 = self.transform(xmin, ymin)
        x2, y2 = self.transform(xmin, ymax)
        x3, y3 = self.transform(xmax, ymax)
        x4, y4 = self.transform(xmax, ymin)

        self.tile.points = [x1, y1, x2, y2, x3, y3, x4, y4]

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
        start_index = -int(self.VERTICAL_NUMBER_LINES / 2) + 1
        end_index = start_index + self.VERTICAL_NUMBER_LINES - 1

        xmin = self.get_line_x_from_index(start_index)
        xmax = self.get_line_x_from_index(end_index)

        for horizontal_line in range(0, self.HORIZONTAL_NUMBER_LINES):
            line_y = self.get_line_y_from_index(horizontal_line)
            x1, y1 = self.transform(xmin, line_y)
            x2, y2 = self.transform(xmax, line_y)
            self.horizontal_lines[horizontal_line].points = [x1, y1, x2, y2]

    def update(self, dt):
        # print(f"dt: {dt*60} - 1/60 : {1}")
        time_factor = dt*60  # permet de corriger la vitesse d'affichage pour avoir toujours un ressenti de 60fps !
        self.update_vertical_lines()
        self.update_horizontal_lines()
        self.update_tiles()

        self.current_offset_y += self.SPEED_OFFSET_Y * time_factor # fais defiler lignes horizontales

        spacing_y = self.HORIZONTAL_LINES_SPACING * self.height
        """ simule lignes infinis"""
        if self.current_offset_y >= spacing_y:
            self.current_offset_y -= spacing_y
            self.current_y_loop += 1  # deplace la tile lors de l'animation

        # self.current_offset_x += self.current_speed_x * time_factor  # fais defiler lignes verticales


class GalaxyApp(App):
    pass


GalaxyApp().run()
