# Морской Бой
from random import randint
from copy import deepcopy as copy
from os import system as sys

deskSize = 6
ds1 = deskSize - 1
numLst = "1 2 3 4 5 6".split()
life = 7


class Desk:

    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

    def __str__(self):
        lines = [' |' + '|'.join(numLst) + '|   |' + '|'.join(numLst) + '|']
        lines.extend(
            [
                str(ind + 1) + '|' + '|'.join(map(self.player1.change, self.player1.map[ind])) + '|  '
                + str(ind + 1) + '|' + '|'.join(map(self.player2.change, self.player2.map[ind])) + '|'
                for ind in range(deskSize)
            ]
        )
        line = '\n'.join(lines)
        return line

    def play(self):
        while True:
            print("Прием. Ваш ход. Передайте координаты для выстрела.")
            self.player1.hit(self.player2)
            if self.player2.health == 0:
                print(self.player1.name, "Победа!", self, sep='\n')
                return 0
            sys("cls")
            self.player2.hit(self.player1)
            if self.player1.health == 0:
                print(self.player1.name, "Поражение!", self, sep='\n')
                return 0

            # hit(Attacker, Defender, int(input()), int(input()))
            # hit(Defender, Attacker, int(input()), int(input()))


class Ship:
    def __init__(self, xcords, ycords):  # конструктор
        self.size = len(ycords)  # количество клеточек
        self.health = self.size  # жизнь
        self.xcords = copy(xcords)  # массив кординат по икс длинной с размер
        self.ycords = copy(ycords)  # массив координат по игрик длинной с размер
        self.value = [1] * self.size  # массив значений
# 6 кораблей
# количество x размер)
# 1x3
# 2x2
# 4x1

# Тех. значение чисел
# 0 - пустая клетка,
# 1 - ячейка корабля,
# (-1) - поврежденная ячейка,
# 2 - ячейка периметра корабля,


class Player:
    def __init__(self, name='comp', autocreate=True):
        self.name = name
        self.health = life  # Количество живых клеток
        self.map = [[0] * deskSize for i in range(deskSize)]
        self.fleet = []  # Пустой массив для класса корабль
        if autocreate:
            ''' Заполнение кораблями массива'''
            try:
                xcords, ycords = self.createCords(3)
                self.fleet.append(Ship(xcords, ycords))  # 1x3
                for i in range(2):
                    xcords, ycords = self.createCords(2)
                    self.fleet.append(Ship(xcords, ycords))
                for i in range(2):
                    xcords, ycords = self.createCords(1)
                    self.fleet.append(Ship(xcords, ycords))
            except Exception as e:
                raise e
        else:
            try:

                lines = [' |' + '|'.join(numLst) + '|   |' + '|'.join(numLst) + '|']
                lines.extend(
                    [
                        str(ind + 1) + '|' + '|'.join(['0']*deskSize) + '|  '
                        + str(ind + 1) + '|' + '|'.join(['0']*deskSize) + '|'
                        for ind in range(deskSize)
                    ]
                )
                map0 = '\n'.join(lines)
                print(map0)
                print("Давай введем координаты для кораблей", "\n", "Начнем с 3-клеточного")
                while True:
                    xcords, ycords = [], []
                    for i in range(3):
                        x, y = self.getCords()
                        xcords.append(x)
                        ycords.append(y)
                    if self.freePlace(xcords, ycords) and self.checkPerimetr(xcords, ycords):
                        for ind in range(len(ycords)):
                            self.map[ycords[ind]][xcords[ind]] = 1
                            self.paintPerimetr(xcords, ycords)
                        break
                    print("Ошибка")
                self.fleet.append(Ship(xcords, ycords))
                print("Продолжим для 2-клеточного")
                for i in range(2):
                    while True:
                        xcords.clear()
                        ycords.clear()
                        for i in range(2):
                            x, y = self.getCords()
                            xcords.append(x)
                            ycords.append(y)
                        if self.freePlace(xcords, ycords) and self.checkPerimetr(xcords, ycords):
                            for ind in range(len(ycords)):
                                self.map[ycords[ind]][xcords[ind]] = 1
                                self.paintPerimetr(xcords, ycords)
                            break
                        print("Ошибка, заново введите координаты для 2 клеточного")
                    self.fleet.append(Ship(xcords, ycords))
            except Exception as e:
                raise e

    def change(self, num):
        if self.name == "comp":
            if num == -1:
                return 'x'
            elif num == 3:
                return 'T'
            else:
                return 'o'
        else:
            if num == 1:
                return "•"
            elif num == -1:
                return 'x'
            elif num == 3:
                return 'T'
            else:
                return 'o'

    def getCords(self):
        if self.name == "comp":
            x, y = randint(0, deskSize), randint(0, deskSize)
        else:
            x, y = tuple(map(int, input("x y: ").split()))
        return x-1, y-1

    def createCords(self, size):  # Создаем координаты
        vertical = bool(randint(0, 1))  # Опеределяем ось
        if vertical:  # print('Вертикально')
                x = randint(0, ds1)  # Случайное знач для х
                y = randint(0, (ds1 - size))  # Случайное значение для у, в пределах границ
                # Проверка Места для Корабля и его границ
                xcords = [x] * size
                ycords = [y + i for i in range(size)]
                if self.freePlace(xcords, ycords) and self.checkPerimetr(xcords, ycords):
                    for y1 in ycords:
                        self.map[y1][x] = 1
                    self.paintPerimetr(xcords, ycords)
                    return xcords, ycords
                else:
                    return self.createCords(size)
        elif not vertical:  # print('Горизонтально')
                y = randint(0, ds1)
                x = randint(0, (ds1 - size))
                ycords = [y] * size
                xcords = [x + i for i in range(size)]
                # Првоерка места для корабля и его границ
                if self.freePlace(xcords, ycords) and self.checkPerimetr(xcords, ycords):

                    for x1 in xcords:
                        self.map[y][x1] = 1
                    self.paintPerimetr(xcords, ycords)
                    return xcords, ycords
                else:
                    return self.createCords(size)

    def paintPerimetr(self, xcords, ycords):  # Помечаем периметр
        size = len(xcords)
        vertical = all([x == xcords[0] for x in xcords])
        if vertical:  # Вертикально?
            x = xcords[0]
            self.paintPixel(x, min(ycords) - 1)  # 2 Точки на линии корабля
            self.paintPixel(x, max(ycords) + 1)
            for i in range(size + 2):  # 2 Линии вдоль корабля
                self.paintPixel(x - 1, min(ycords) - 1 + i)
                self.paintPixel(x + 1, min(ycords) - 1 + i)
        else:  # Горизонтльно
            y = ycords[0]
            self.paintPixel(min(xcords) - 1, y)
            self.paintPixel(max(xcords) + 1, y)
            for i in range(size + 2):
                self.paintPixel(min(xcords) - 1 + i, y - 1)
                self.paintPixel(min(xcords) - 1 + i, y + 1)
        return True

    def paintPixel(self, x, y):  # Помечаем пиксель периметра
        if any([x < 0, y < 0, x > ds1, y > ds1]):  # Если за границами, то пропустить
            return False
        else:
            self.map[y][x] = 2  # Значение вокруг корабля 2
            return True

    def borderPointOk(self, x, y):  # Проверка пикселя окружения  корабля
        if any([x < 0, x > ds1, y < 0, y > ds1]):
            return True  # границы поля
        if self.map[y][x] == 2:
            return True  # границы корабля
        return self.map[y][x] == 0  # Пустая

    def checkPerimetr(self, xcords, ycords):  # Проверка окружения корабля
        size = len(xcords)
        vertical = all([x == xcords[0] for x in xcords])

        if vertical:  # вертикально?
            if not self.borderPointOk(xcords[0], min(ycords) - 1) or not self.borderPointOk(xcords[0], max(ycords) + 1):
                return False  # края
            for i in range(size + 2):  # полосы вдоль
                for j in range(3):
                    if not self.borderPointOk(xcords[0] - 1 + j, min(ycords) - 1 + i):
                        return False
                    elif i == size + 1:  # последний элемент
                        return True
            #  return True
        else:  # горизонтально
            if not self.borderPointOk(min(xcords) - 1, ycords[0]) or not self.borderPointOk(max(xcords) + 1, ycords[0]):
                return False  # края - 2 Точки на линии корабля
            for i in range(size + 2):  # полосы вдоль
                for j in range(3):
                    if not self.borderPointOk(min(xcords) - 1 + i, ycords[0] - 1 + j):
                        return False
                    elif i == size + 1:  # последний элемент
                        return True
            #return True

    def freePixel(self, x, y):  # Проверка на постановку пикселя корабля
        return self.map[y][x] == 0

    def freePlace(self, xcords, ycords):  # Проверка пересечения кораблей
        return all([self.freePixel(xcords[i], ycords[i]) for i in range(len(xcords))])

    def hit(self, defender):
        comp = self.name == "comp"
        if not comp:
            print(desk)
        x, y = self.getCords()
        # Проверка данных
        if any([x > ds1, y > ds1, x < 0, y < 0]):
            if not comp:
                print(self.name, ", ты вышел за пределы поля: x,y[0,", str(ds1), "]")
            return self.hit(defender)

        if (defender.map[y][x] == -1) or (defender.map[y][x] == 3):
            if not comp:
                print(self.name, "Ты сюда стрелял!")
            return self.hit(defender)

        # Мимо кораблей
        if (defender.map[y][x] == 2) or (defender.map[y][x] == 0):
            # Отметить выстрел у противника
            defender.map[y][x] = 3
            return print(self.name, "Мимо!")

        # Попал
        if defender.map[y][x] == 1:
            # Отметить попадение у себя и противника
            defender.map[y][x] = -1
            for ind, ship in enumerate(defender.fleet):
                if x in ship.xcords and y in ship.ycords:
                    self.fleet[ind].health -= 1
                    self.health -= 1
                    if self.fleet[ind].health == 0:
                        print("Убил")
                        if defender.health == 0:
                            print(self.name, 'победил!')
                            return 0
                        return self.hit(defender)
                    else:
                        print("Ранил!")
                        self.hit(defender)

# Тех. значение чисел
# 0 - пустая клетка,
# 1 - ячейка корабля,
# (-1) - поврежденная ячейка,
# 2 - ячейка периметра корабля,


me = Player(input("What is your name?"), bool(input("Autocreate: True or False")))
comp = Player()
desk = Desk(me, comp)
desk.play()
print()
print(desk)


