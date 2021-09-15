def transform(self, x, y):
    """choix affichage 2D ou perspective"""
    # return self.transform_2D(x, y)
    return self.transform_perspective(x, y)


def transform_2D(self, x, y):
    """choix affichage 2D"""
    return int(x), int(y)


def transform_perspective(self, x, y):
    """choix affichage 2D ou perspective"""
    lin_y = y * self.perspective_point_y / self.height
    if lin_y > self.perspective_point_y:
        lin_y = self.perspective_point_y

    diff_x = x - self.perspective_point_x
    diff_y = self.perspective_point_y - lin_y
    factor_y = diff_y / self.perspective_point_y
    # factor_y = factor_y * factor_y
    factor_y = pow(factor_y, 2)  # pow = mise au carre

    offset_x = diff_x * factor_y

    transfor_x = self.perspective_point_x + diff_x * factor_y
    transfor_y = self.perspective_point_y - factor_y * self.perspective_point_y

    return int(transfor_x), int(transfor_y)