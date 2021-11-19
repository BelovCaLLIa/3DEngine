import pygame as pg
from object_3d import *
from camera import *
from projection import *


class SoftwareRender:
    def __init__(self):
        # Инициализация библиотеки
        pg.init()
        # Разрешение
        self.RES = self.WIDTH, self.HEIGHT = 1600, 900
        # Поврхность для отрисовки
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        # Настройка желаймого кол-ва кадров
        self.FPS = 60
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.createObjects()

    # Создание объектов
    def createObjects(self):
        # self.camera = Camera(self, [0.5, 1, -4])
        self.camera = Camera(self, [0, 0.5, -4])
        self.projection = Projection(self)

        # Вариант с объектом
        self.object = self.get_object_from_file('3DEngine/resources/Alpine_Renault_A110_\'63.obj')

        # Вариант сцены с системой координат
        """ 
        self.object = Object3D(self)

        # Смещаем объект
        self.object.translate([0.2, 0.4, 0.2])
        # Поворачиваем на 30 градусов
        # self.object.rotate_y(math.pi / 6)
        
        # Система координат
        self.axes = Axes(self)
        self.axes.translate([0.7, 0.9, 0.7])
        self.world_axes = Axes(self)
        self.world_axes.movement_flag = False
        self.world_axes.scale(2.5)
        self.world_axes.translate([0.0001, 0.0001, 0.0001]) """

    # Парсер вершин
    def get_object_from_file(self, filename):
        vertex, faces = [], []
        with open(filename) as f:
            for line in f:
                if line.startswith('v '):
                    vertex.append([float(i) for i in line.split()[1:]] + [1])
                elif line.startswith('f'):
                    faces_ = line.split()[1:]
                    faces.append([int(face_.split('/')[0]) - 1 for face_ in faces_])
        return Object3D(self, vertex, faces)

    # Отрисовка
    def draw(self):
        self.screen.fill(pg.Color("darkslategray"))
        """ # Отрисовка координат
        self.world_axes.draw()
        self.axes.draw() """
        # Отрисовка объекта
        self.object.draw()

    # Обновление
    def run(self):
        while True:
            self.draw()
            # Управление камерой
            self.camera.control()
            # Проверка на выход из программы
            [exit() for event in pg.event.get() if event.type == pg.QUIT]
            # Вывод в заголовок FPS
            pg.display.set_caption(str(self.clock.get_fps()))
            # Обновим поверхность отрисовки
            pg.display.flip()
            self.clock.tick(self.FPS)


if __name__ == '__main__':
    # Создаём экземпляр
    app = SoftwareRender()
    # Вызываем метод обновления
    app.run()