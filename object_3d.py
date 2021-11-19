import pygame as pg 
from matrix_functions import *
# Преобразование в быстрый машинный код для ускорение вычислений
from numba import njit

# Быстрые вычисления
@njit(fastmath=True)
def any_func(arr, a, b):
    return np.any((arr == a) | (arr == b))


class Object3D:
    # def __init__(self, render):
    def __init__(self, render, vertexes, faces):
        self.render = render
        # Однородные координаты
        """ self.vertexes = np.array([(0, 0, 0, 1), (0, 1, 0, 1), (1, 1, 0, 1), (1, 0, 0, 1), 
                                  (0, 0, 1, 1), (0, 1, 1, 1), (1, 1, 1, 1), (1, 0, 1, 1)]) """
        # Создаёт полноценные грани из списков
        self.vertexes = np.array([np.array(v) for v in vertexes])

        # Грани куба
        # Указываем вершины
        # self.faces = np.array([(0, 1, 2, 3), (4, 5, 6, 7), (0, 4, 5, 1), (2, 3, 7, 6), (1, 2, 6, 5), (0, 3, 7, 4)])

        self.faces = np.array([np.array(face) for face in faces])

        # Рисуем оси координат
        # Шрифт
        self.font = pg.font.SysFont("Arial", 30, bold=True)
        # Цвет для граней
        self.color_faces = [(pg.Color("orange"), face) for face in self.faces]
        # Тригер для разрешения движения и отображения вершин
        self.movement_flag, self.draw_vertexes = True, False
        # Надпись для объекта
        self.label = ""

    # Отрисовка фигуры
    def draw(self):
        self.screen_projection()
        self.movement()

    # Движение объекта
    def movement(self):
        if self.movement_flag:
            self.rotate_y(pg.time.get_ticks() % 0.005)

    # Вывод проекции на экран
    def screen_projection(self):
        # Переносим вершины объектов в пространство камеры
        vertexes = self.vertexes @ self.render.camera.camera_matrix()
        # Переносим вершины в пространство отсечения
        vertexes = vertexes @ self.render.projection.projection_matrix
        # Нормализуем координаты вершин
        # reshape - меняет форму матрицы
        vertexes /= vertexes [:, -1].reshape(-1, 1)
        # Отсикает координаты вершин меньше -3 и больше 3 и приравниваем к 0
        # Берём пространство отсечения больше, чтобы к объекту можно было приближаться
        vertexes[(vertexes > 3) | (vertexes < -3)] = 0
        # Умножаем вершины на матрицу преобразования
        vertexes = vertexes @ self.render.projection.to_screen_matrix
        # Выбираем координаты для x,y осей
        vertexes = vertexes[:, :2]

        ## Проход по всем граням объекта
        # for face in self.faces:
            # poligon = vertexes[face]
            # if not np.any((poligon == self.render.H_WIDTH) | (poligon == self.render.H_HEIGHT)):
                ## polygon() - рисует многоугольник по переданному ей массиву координат точек
                # pg.draw.polygon(self.render.screen, pg.Color("orange"), poligon, 3)

        # Проход по всем граням объекта
        for index, color_face in enumerate(self.color_faces):
            color, face = color_face
            poligon = vertexes[face]
            # Обычный вариант
            """ if not np.any((poligon == self.render.H_WIDTH) | (poligon == self.render.H_HEIGHT)):
                pg.draw.polygon(self.render.screen, color, poligon, 1) """
            # Быстрый
            if not any_func(poligon, self.render.H_WIDTH, self.render.H_HEIGHT):
                pg.draw.polygon(self.render.screen, color, poligon, 1)
                if self.label:
                    text = self.font.render(self.label[index], True, pg.Color("white"))
                    self.render.screen.blit(text, poligon[-1])

        # Условие на разрешение строить вершины
        if self.draw_vertexes:
            # Проход по всем вершинам объекта
            for vertex in vertexes:
                # Обычный вариант
                """ if not np.any((vertex == self.render.H_WIDTH) | (vertex == self.render.H_HEIGHT)):
                    pg.draw.circle(self.render.screen, pg.Color("white"), vertex, 2) """
                # Быстрый
                if not any_func(vertex, self.render.H_WIDTH, self.render.H_HEIGHT):
                    pg.draw.circle(self.render.screen, pg.Color("white"), vertex, 2)


    def translate(self, pos):
        # @ - обозначает перемножение матриц
        self.vertexes = self.vertexes @ translate(pos)

    def scale(self, scale_to):
        self.vertexes = self.vertexes @ scale(scale_to)

    def rotate_x(self, angle):
        self.vertexes = self.vertexes @ rotate_x(angle)

    def rotate_y(self, angle):
        self.vertexes = self.vertexes @ rotate_y(angle)

    def rotate_z(self, angle):
        self.vertexes = self.vertexes @ rotate_z(angle)


class Axes(Object3D):
    def __init__(self, render):
        super().__init__(render)
        self.vertexes = np.array([(0, 0, 0, 1), (1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1)])
        self.faces = np.array([(0, 1), (0, 2), (0, 3)])
        self.colors = [pg.Color("red"), pg.Color("green"), pg.Color("blue")]
        self.color_faces = [(color, face) for color, face in zip(self.colors, self.faces)]
        # Запрещаем рисование вершин
        self.draw_vertexes = False
        self.label = "XYZ"