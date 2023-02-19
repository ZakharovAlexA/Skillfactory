# Игра: Морской бой
# Автор: Захаров Александр

from random import randint


class Dot:
    """Класс точек на поле"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x}, {self.y})"


class Ship:
    """Класс Корабль на игровом поле"""
    def __init__(self, bow, lenght, vector):
        self.bow = bow
        self.lenght = lenght
        self.vector = vector
        self.lives = lenght

    # Метод определяет точки корабля
    @property
    def dots(self):
        ship_dots = []
        for i in range(self.lenght):
            cur_x = self.bow.x
            cur_y = self.bow.y
            # Ориетирован по вертикали
            if self.vector == 0:
                cur_x += i
            # Ориетирован по горизонтали
            elif self.vector == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots

    # Определяем было ли попадание в корабль
    def shooten(self, shot):
        return shot in self.dots


class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "Этот выстрел мимо доски! Прицельтесь лучше!"


class BoardAlreadyShotException(BoardException):
    def __str__(self):
        return "Вы уже стреляли по этой клетке"


class BoardWrongShipException(BoardException):
    pass


class Board:
    """Класс игровой доски"""
    def __init__(self, hid=False, size=6):  # hid - скрывать ли поле; size - размер поля
        self.size = size
        self.hid = hid
        self.busy = []
        self.ships = []
        self.count = 0
        self.field = [["O"] * size for _ in range(size)]

    # Проверка выпала ли точка из поля
    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    # Добавить корабль на доску
    def add_ship(self, ship):

        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "█"
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    # Добавим контур вокруг корабля
    def contour(self, ship, marker=False):  # marker указывает заполнять точками "." контур или нет
        offset = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in offset:
                cntr = Dot(d.x + dx, d.y + dy)
                if not (self.out(cntr)) and cntr not in self.busy:
                    if marker:
                        self.field[cntr.x][cntr.y] = "."
                    self.busy.append(cntr)

    # Формирование кадра игрового поля
    def __str__(self):
        frame = ""
        frame += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            frame += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hid:
            frame = frame.replace("█", "O")
        return frame

    # Проверка выстрела
    def shot(self, d):
        if self.out(d):
            raise BoardOutException()

        if d in self.busy:
            raise BoardAlreadyShotException()

        self.busy.append(d)

        for ship in self.ships:
            if ship.shooten(d):
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, marker=True)
                    print("Корабль потоплен!")
                    return False
                else:
                    print("Корабль ранен!")
                    return True

        self.field[d.x][d.y] = "T"
        print("Мимо!")
        return False

    # Обнуление информации о занятых полях перед началом игры
    def begin(self):
        self.busy = []


class Player:
    """Класс Игрок"""
    def __init__(self, board, rival):
        self.board = board
        self.rival = rival
        self.cnt = -1
        # Формируем шаблон ходов компьютера (не случайным образом)
        self.sh = []
        for x in range(0, 6, 2):
            for y in range(0, 6, 2):
                self.sh.append((x, y))

        for x in range(1, 6, 2):
            for y in range(0, 6, 2):
                self.sh.append((x, y))

        for x in range(0, 6, 2):
            for y in range(1, 6, 2):
                self.sh.append((x, y))

        for x in range(1, 6, 2):
            for y in range(1, 6, 2):
                self.sh.append((x, y))

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.rival.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    """Класс ИИ Игрока"""
    def ask(self):
        self.cnt += 1
        # ИИ ходит по заранее определенному шаблону
        print(f"Ход компьютера: {self.sh[self.cnt][0] + 1} {self.sh[self.cnt][1] + 1}")
        return Dot(self.sh[self.cnt][0], self.sh[self.cnt][1])


class User(Player):
    """Класс 'Живого' Игрока"""
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()

            if len(cords) != 2:
                print(" Введите 2 координаты! ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print(" Введите числа! ")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)


class Game:
    """Класс Игра (основной класс игры)"""
    def __init__(self, size=6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True

        self.ai = AI(co, pl)
        self.us = User(pl, co)

    # Расстановка кораблей на поле
    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):
        lens = [3, 2, 2, 1, 1, 1, 1]    # Корабли размером 3, 2 и 1 поле
        board = Board(size=self.size)
        attempts = 0
        for i in lens:
            while True:
                attempts += 1
                if attempts > 2000:     # пробуем расставить корабли на поле до 2000 раз
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), i, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    # Игровой цикл
    def loop(self):
        num = 0
        while True:
            print("-" * 20)
            print("Ваша доска:")
            print(self.us.board)
            print("-" * 20)
            print("Доска компьютера:")
            print(self.ai.board)
            if num % 2 == 0:
                print("-" * 20)
                print("Ходит игрок!")
                repeat = self.us.move()
            else:
                print("-" * 20)
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                print("-" * 20)
                print("ВЫ выиграли!")
                break

            if self.us.board.count == 7:
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1


print("-------------------")
print("       ИГРА        ")
print("   МОРСКОЙ БОЙ     ")
print(" Человек           ")
print("     против        ")
print("         компьютера")
print("-------------------")
print(" формат ввода: x y ")
print(" x - номер строки  ")
print(" y - номер столбца ")

b = Game()
b.loop()
