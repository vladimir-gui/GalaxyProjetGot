from kivy import Config, platform
# """ taille fenetre par defaut"""

Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '400')

import random
from kivy.core.window import Window
from kivy.app import App
from kivy.graphics import Color, Line, Quad, Triangle
from kivy.properties import NumericProperty, Clock
from kivy.uix.widget import Widget


class MainWidget(Widget):
    from transforms import transform, transform_2D, transform_perspective
    from user_actions import on_keyboard_up, on_keyboard_down, on_touch_down, on_touch_up
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    VERTICAL_NUMBER_LINES = 8
    VERTICAL_LINES_SPACING = 0.2  # pourcentage selon largeur ecran
    vertical_lines = []

    HORIZONTAL_NUMBER_LINES = 8
    HORIZONTAL_LINES_SPACING = 0.15  # pourcentage selon largeur ecran
    horizontal_lines = []

    SPEED_OFFSET_Y = 1.0
    current_offset_y = 0
    current_y_loop = 0

    MOVE_SPEED_X = 3.4
    current_speed_x = 0
    current_offset_x = 0

    """ definition tuile tile """
    NUMBER_TILES = 8
    tiles = []  # forme QUAD
    tiles_coordinates = []  # coordonnees tile_x, tile_y
    NUMBER_PRE_FILL_TILES = 15  # nb tiles fixes avant de changer en x

    """ parametres vaisseau"""
    ship = None  # initialise instruction triangle
    SHIP_WIDTH_PERCENT = 0.1
    SHIP_BASE_Y_PERCENT = 0.04
    SHIP_HEIGHT_PERCENT = 0.035
    ship_coordinate = [(0, 0), (0, 0), (0, 0)]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_vertical_lines()
        self.init_horizontal_lines()
        self.init_tiles()
        self.init_ship()
        self.pre_fill_tiles_coordinates()
        self.generate_tiles_coordinates()

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

    def pre_fill_tiles_coordinates(self):
        """ initialise X tiles pour avant que les tiles changent en x"""
        for i in range(0, self.NUMBER_PRE_FILL_TILES):
            self.tiles_coordinates.append((0, i))

    def init_ship(self):
        """creation du vaisseau"""
        with self.canvas:
            Color(0, 0, 0)
            self.ship = Triangle()

    def update_ship(self):
        """repositionne vaisseau si ecran redimensionne """
        center_x = self.width / 2
        base_y = self.SHIP_BASE_Y_PERCENT * self.height
        half_width = self.SHIP_WIDTH_PERCENT * self.width / 2
        ship_height = self.SHIP_HEIGHT_PERCENT * self.height

        # self.transform
        #    2
        # 1     3
        self.ship_coordinate[0] = (center_x - half_width, base_y)
        self.ship_coordinate[1] = (center_x, base_y + ship_height)
        self.ship_coordinate[2] = (center_x + half_width, base_y)

        x1, y1 = self.transform(*self.ship_coordinate[0])  # !! * permet d'eclater un tuple dans un tuple voir dessous
        # x1, y1 = self.transform(self.ship_coordinate[0][0], self.ship_coordinate[0][1])
        x2, y2 = self.transform(*self.ship_coordinate[1])
        x3, y3 = self.transform(*self.ship_coordinate[2])
        self.ship.points = [x1, y1, x2, y2, x3, y3]

    def check_ship_collision(self):
        for i in range(0, len(self.tiles_coordinates)):
            tile_x, tile_y = self.tiles_coordinates[i]
            if tile_y > self.current_y_loop + 1:
                return False  # Game over
            if self.check_ship_collision_with_tile(tile_x, tile_y):
                return True  # ok
        return False

    def check_ship_collision_with_tile(self, tile_x, tile_y):
        """recuperation des coordonnées du tile"""
        xmin, ymin = self.get_tile_coordinates(tile_x, tile_y)
        xmax, ymax = self.get_tile_coordinates(tile_x + 1, tile_y + 1)
        for i in range(0, 3):
            px, py = self.ship_coordinate[i]
            if xmin <= px <= xmax and ymin <= py <= ymax:
                return True
                # print("point dans le tile")
        return False

    def init_tiles(self):
        """ creation de la tuile a suivre pour gagner """
        with self.canvas:
            Color(1, 1, 1)
            for tile in range(0, self.NUMBER_TILES):
                self.tiles.append(Quad())

    def generate_tiles_coordinates(self):
        last_x = 0
        last_y = 0

        # suppr données sorties de l'écran
        # tile_y < self.current_y_loop
        for i in range(len(self.tiles_coordinates)-1, -1, -1):
            if self.tiles_coordinates[i][1] < self.current_y_loop:  # verif si y de la tile < numero loop
                del self.tiles_coordinates[i]

        if len(self.tiles_coordinates) > 0:
            last_coordinate = self.tiles_coordinates[-1]  # recupere la derniere valeur tableau
            last_x = last_coordinate[0]
            last_y = last_coordinate[1] + 1  # incrementation valeur y suivante

        for coordinates in range(len(self.tiles_coordinates), self.NUMBER_TILES):
            random_x = random.randint(0, 2)  # generation de patern (forme) aleatoire
            # 0 -> en avant
            # 1 -> a droite
            # 2 -> a gauche

            start_index = -int(self.VERTICAL_NUMBER_LINES / 2) + 1
            end_index = start_index + (self.VERTICAL_NUMBER_LINES - 1) -1

            if last_x <= start_index:
                random_x = 1
            if last_x >= end_index:
                random_x = 2

            self.tiles_coordinates.append((last_x, last_y))
            if random_x == 1:
                last_x += 1
                self.tiles_coordinates.append((last_x, last_y))
                last_y += 1
                self.tiles_coordinates.append((last_x, last_y))
            elif random_x == 2:
                last_x -= 1
                self.tiles_coordinates.append((last_x, last_y))
                last_y += 1
                self.tiles_coordinates.append((last_x, last_y))
            last_y += 1

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
        for id_tiles in range(0, self.NUMBER_TILES):
            tile = self.tiles[id_tiles]
            tile_coordinates = self.tiles_coordinates[id_tiles]
            xmin, ymin = self.get_tile_coordinates(tile_coordinates[0], tile_coordinates[1])
            xmax, ymax = self.get_tile_coordinates(tile_coordinates[0] + 1, tile_coordinates[1] + 1)

            # 2     3
            #
            # 1     4
            x1, y1 = self.transform(xmin, ymin)
            x2, y2 = self.transform(xmin, ymax)
            x3, y3 = self.transform(xmax, ymax)
            x4, y4 = self.transform(xmax, ymin)

            tile.points = [x1, y1, x2, y2, x3, y3, x4, y4]

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
        self.update_ship()

        speed_y = self.SPEED_OFFSET_Y * self.height / 100
        self.current_offset_y += speed_y * time_factor # fais defiler lignes horizont fonction taille ecran

        spacing_y = self.HORIZONTAL_LINES_SPACING * self.height
        """ simule lignes infinis"""
        if self.current_offset_y >= spacing_y:
            self.current_offset_y -= spacing_y
            self.current_y_loop += 1  # deplace la tile lors de l'animation
            self.generate_tiles_coordinates()  # maintient et actualise (genere) les coordonnees y des tiles

        self_x = self.current_speed_x * self.width / 100
        self.current_offset_x += self_x * time_factor  # fais defiler lignes verticales

        if not self.check_ship_collision():
            print("GAME OVER")


class GalaxyApp(App):
    pass


GalaxyApp().run()
