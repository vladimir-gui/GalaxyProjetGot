from kivy import Config, platform
# """ taille fenetre par defaut"""
from kivy.core.audio import SoundLoader
from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout

Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '400')

import random
from kivy.core.window import Window
from kivy.app import App
from kivy.graphics import Color, Line, Quad, Triangle
from kivy.properties import NumericProperty, Clock, ObjectProperty, StringProperty

Builder.load_file("menu.kv")


class MainWidget(RelativeLayout):
    from transforms import transform, transform_2D, transform_perspective
    from user_actions import on_keyboard_up, on_keyboard_down, on_touch_down, on_touch_up

    menu_widget = ObjectProperty()  # connecte au menu_widget kv
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    V_NB_LINES = 8
    V_LINES_SPACING = 0.4  # pourcentage selon largeur ecran
    vertical_lines = []

    H_NB_LINES = 8
    H_LINES_SPACING = 0.15  # pourcentage selon largeur ecran
    horizontal_lines = []

    SPEED = 0.8
    current_offset_y = 0
    current_y_loop = 0

    SPEED_X = 3.5
    current_speed_x = 0
    current_offset_x = 0

    """ definition tuile tile """
    NB_TILES = 16
    tiles = []  # forme QUAD
    tiles_coordinates = []  # coordonnees tile_x, tile_y
    # NUMBER_PRE_FILL_TILES = 16  # nb tiles fixes avant de changer en x

    """ parametres vaisseau"""
    SHIP_WIDTH = 0.1
    SHIP_BASE_Y = 0.035
    SHIP_HEIGHT = 0.04
    ship = None  # initialise instruction triangle
    ship_coordinate = [(0, 0), (0, 0), (0, 0)]

    """gestion game over"""
    state_game_over = False
    state_game_has_started = False

    """ gestion sons """
    sound_begin = None
    sound_galaxy = None
    sound_gameover_impact = None
    sound_gameover_voice = None
    sound_music1 = None
    sound_restart = None

    """Proprietes KV"""
    score_txt = StringProperty()
    menu_title = StringProperty("G A L A X Y")
    menu_button_title = StringProperty("START")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_audio()
        self.init_vertical_lines()
        self.init_horizontal_lines()
        self.init_tiles()
        self.init_ship()
        # self.pre_fill_tiles_coordinates()
        # self.generate_tiles_coordinates() remplace par reset
        self.reset_game()

        if self.is_desktop():  # clavier sur desktop uniquement
            self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self._keyboard.bind(on_key_down=self.on_keyboard_down)
            self._keyboard.bind(on_key_up=self.on_keyboard_up)

        Clock.schedule_interval(self.update, 1.0 / 60.0)  # rafraichissement 60 fps

        self.sound_galaxy.play()

    def init_audio(self):
        self.sound_begin = SoundLoader.load("audio/begin.wav")
        self.sound_galaxy = SoundLoader.load("audio/galaxy.wav")
        self.sound_gameover_impact = SoundLoader.load("audio/gameover_impact.wav")
        self.sound_gameover_voice = SoundLoader.load("audio/gameover_voice.wav")
        self.sound_music1 = SoundLoader.load("audio/music1.wav")
        self.sound_restart = SoundLoader.load("audio/restart.wav")

        self.sound_music1.volume = 1
        self.sound_begin.volume = .25
        self.sound_galaxy.volume = .25
        self.sound_gameover_voice.volume = .25
        self.sound_restart.volume = .25
        self.sound_gameover_impact.volume = .6


    def reset_game(self):
        self.current_offset_y = 0
        self.current_y_loop = 0
        self.current_speed_x = 0
        self.current_offset_x = 0

        self.tiles_coordinates = []
        self.score_txt = f"SCORE : {self.current_y_loop}"
        self.pre_fill_tiles_coordinates()
        self.generate_tiles_coordinates()
        self.state_game_over = False

    def keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard.unbind(on_key_up=self._on_keyboard_up)
        self._keyboard = None

    def is_desktop(self):
        if platform in ('linux', 'win', 'macosx'):
            return True
        return False

    def init_ship(self):
        """creation du vaisseau"""
        with self.canvas:
            Color(0, 0, 0)
            self.ship = Triangle()

    def update_ship(self):
        """repositionne vaisseau si ecran redimensionne """
        center_x = self.width / 2
        base_y = self.SHIP_BASE_Y * self.height
        half_width = self.SHIP_WIDTH * self.width / 2
        ship_height = self.SHIP_HEIGHT * self.height

        # self.transform
        #    2
        # 1     3
        self.ship_coordinate[0] = (center_x - half_width, base_y)
        self.ship_coordinate[1] = (center_x, base_y + ship_height)
        self.ship_coordinate[2] = (center_x + half_width, base_y)

        # x1, y1 = self.transform(self.ship_coordinate[0][0], self.ship_coordinate[0][1])
        x1, y1 = self.transform(*self.ship_coordinate[0])  # !! * permet d'eclater un tuple dans un tuple voir dessus
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
        """recuperation des coordonn??es du tile"""
        xmin, ymin = self.get_tile_coordinates(tile_x, tile_y)
        xmax, ymax = self.get_tile_coordinates(tile_x + 1, tile_y + 1)
        for i in range(0, 3):
            px, py = self.ship_coordinate[i]
            if xmin <= px <= xmax and ymin <= py <= ymax:
                return True
        return False

    def init_tiles(self):
        """ creation de la tuile a suivre pour gagner """
        with self.canvas:
            Color(1, 1, 1)
            for tile in range(0, self.NB_TILES):
                self.tiles.append(Quad())

    def pre_fill_tiles_coordinates(self):
        """ initialise X tiles pour avant que les tiles changent en x"""
        for i in range(0, 10):
            self.tiles_coordinates.append((0, i))

    def generate_tiles_coordinates(self):
        last_x = 0
        last_y = 0

        # suppr donn??es sorties de l'??cran
        # tile_y < self.current_y_loop
        for i in range(len(self.tiles_coordinates)-1, -1, -1):
            if self.tiles_coordinates[i][1] < self.current_y_loop:  # verif si y de la tile < numero loop
                del self.tiles_coordinates[i]

        if len(self.tiles_coordinates) > 0:
            last_coordinate = self.tiles_coordinates[-1]  # recupere la derniere valeur tableau
            last_x = last_coordinate[0]
            last_y = last_coordinate[1] + 1  # incrementation valeur y suivante

        for i in range(len(self.tiles_coordinates), self.NB_TILES):
            r = random.randint(0, 2)  # generation de patern (forme) aleatoire
            # 0 -> en avant
            # 1 -> a droite
            # 2 -> a gauche

            start_index = -int(self.V_NB_LINES / 2) + 1
            end_index = start_index + self.V_NB_LINES - 1

            if last_x <= start_index:
                r = 1
            if last_x >= end_index - 1:
                r = 2

            self.tiles_coordinates.append((last_x, last_y))
            if r == 1:
                last_x += 1
                self.tiles_coordinates.append((last_x, last_y))
                last_y += 1
                self.tiles_coordinates.append((last_x, last_y))
            elif r == 2:
                last_x -= 1
                self.tiles_coordinates.append((last_x, last_y))
                last_y += 1
                self.tiles_coordinates.append((last_x, last_y))
            last_y += 1

    def init_vertical_lines(self):
        """ definition lignes verticales - objet a variables dynamiques donc trait?? dans le py"""
        with self.canvas:
            Color(1, 1, 1)
            # self.line = Line(points=[100, 0, 100, 100])
            for i in range(0, self.V_NB_LINES):
                self.vertical_lines.append(Line())  # ajout des lignes verticales

    def get_line_x_from_index(self, index):
        central_line_x = self.perspective_point_x
        spacing = self.V_LINES_SPACING * self.width
        offset = index - 0.5  # decalage inter ligne ( 0.5 pour centrer sur chemin)
        line_x = central_line_x + offset * spacing + self.current_offset_x
        return line_x

    def get_line_y_from_index(self, index):
        spacing_y = self.H_LINES_SPACING * self.height
        line_y = index * spacing_y - self.current_offset_y
        return line_y

    def get_tile_coordinates(self, tile_x, tile_y):
        tile_y = tile_y - self.current_y_loop
        x = self.get_line_x_from_index(tile_x)
        y = self.get_line_y_from_index(tile_y)
        return x, y

    def update_tiles(self):
        for i in range(0, self.NB_TILES):
            tile = self.tiles[i]
            tile_coordinates = self.tiles_coordinates[i]
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
        start_index = -int(self.V_NB_LINES / 2) + 1
        for i in range(start_index, start_index+self.V_NB_LINES):
            line_x = self.get_line_x_from_index(i)
            x1, y1 = self.transform(line_x, 0)
            x2, y2 = self.transform(line_x, self.height)
            self.vertical_lines[i].points = [x1, y1, x2, y2]

    def init_horizontal_lines(self):
        """ definition lignes horizontales - objet a variables dynamiques donc trait?? dans le py"""
        with self.canvas:
            Color(1, 1, 1)
            for line in range(0, self.H_NB_LINES):
                self.horizontal_lines.append(Line())  # ajout des lignes horizontales

    def update_horizontal_lines(self):
        start_index = -int(self.V_NB_LINES / 2) + 1
        end_index = start_index + self.V_NB_LINES - 1

        xmin = self.get_line_x_from_index(start_index)
        xmax = self.get_line_x_from_index(end_index)

        for i in range(0, self.H_NB_LINES):
            line_y = self.get_line_y_from_index(i)
            x1, y1 = self.transform(xmin, line_y)
            x2, y2 = self.transform(xmax, line_y)
            self.horizontal_lines[i].points = [x1, y1, x2, y2]

    def update(self, dt):
        # print(f"dt: {dt*60} - 1/60 : {1}")
        time_factor = dt*60  # permet de corriger la vitesse d'affichage pour avoir toujours un ressenti de 60fps !

        self.update_vertical_lines()
        self.update_horizontal_lines()
        self.update_tiles()
        self.update_ship()

        if not self.state_game_over and self.state_game_has_started:
            speed_y = self.SPEED * self.height / 100
            self.current_offset_y += speed_y * time_factor  # fais defiler lignes horizont fonction taille ecran

            spacing_y = self.H_LINES_SPACING * self.height
            """ simule lignes infinis"""
            if self.current_offset_y >= spacing_y:
                self.current_offset_y -= spacing_y
                self.current_y_loop += 1  # deplace la tile lors de l'animation
                self.generate_tiles_coordinates()  # maintient et actualise (genere) les coordonnees y des tiles
                self.score_txt = f"SCORE : {self.current_y_loop}"

            speed_x = self.current_speed_x * self.width / 100
            self.current_offset_x += speed_x * time_factor  # fais defiler lignes verticales

        if not self.check_ship_collision() and not self.state_game_over:
            self.state_game_over = True
            self.menu_title = "G A M E  O V E R"
            self.menu_button_title = "RESTART"
            self.menu_widget.opacity = 1
            self.sound_music1.stop()
            self.sound_gameover_impact.play()
            Clock.schedule_once(self.play_voice_game_over, 2.5)  # mise en place delai pour voix game over
            print("GAME OVER")

    def play_voice_game_over(self, dt):
        if self.state_game_over:  # ! evite bug son si clic rapide sur restart
            self.sound_gameover_voice.play()

    def on_menu_button_pressed(self):
        print("START")
        if self.state_game_over:
            self.sound_restart.play()
        else:
            self.sound_begin.play()
        self.sound_music1.play()
        self.reset_game()
        self.state_game_has_started = True
        self.menu_widget.opacity = 0


class GalaxyApp(App):
    pass


GalaxyApp().run()
