# -*- coding: utf-8 -*-

# Игра "Крестики - Нолики"
# Автор: Захаров Александр

s = '-'
kr_nol = 'X'
n_gamer = 1
# en_game = ''
# Поле размером 3 х 3 заполняем символом '-'
board_temp = [[s for x in range(3)] for y in range(3)]

# Заносим выигрышные варианты
winn_var = [[[a, b] for a in range(len(board_temp))] for b in range(len(board_temp[0]))] \
           + [[[b, a] for a in range(len(board_temp))] for b in range(len(board_temp[0]))] \
           + [[[a, a] for a in range(len(board_temp))]] \
           + [[[a, len(board_temp) - 1 - a] for a in range((len(board_temp) - 1), -1, -1)]]


# Функция прорисовки поля заданного размера
def print_board(board):
    print(' ', end='  ')
    for i in range(len(board[0])):
        print(i, end='  ')
    print()
    n = 0
    for y in board:
        print(n, end='  ')
        n += 1
        for x in y:
            print(x, end='  ')
        print()
    print()


# Проверяем победил ли игрок
def check_winner(board, w_var):
    global s
    t = []
    for a in w_var:
        for b in a:
            x, y = b
            t.append(board[x][y])
        if len(set(t)) == 1 and s not in t:
            return True
        t.clear()


# Спрашивае о повторе игры.
def restart_game():
    global kr_nol
    global n_gamer
    global board_temp
    en_game = str.lower(input('Ещё партию? (Y - Да, N - Нет): '))
    if en_game == 'y':
        kr_nol = 'X'
        n_gamer = 1
        board_temp = [[s for x in range(3)] for y in range(3)]
        return True
    else:
        return False


print('Игра "Крести - Нолики"')
print('Игрок 1 играет Крестиком "Х", Игрок 2 играет Ноликом "О" \n')


while True:
    print_board(board_temp)
    x = int(input(f'Игрок {n_gamer}, введите координаты клетки по Горизонтали:'))
    y = int(input(f'Игрок {n_gamer}, введите координаты клетки по Вертикали:'))
    print()
    # Проверка правильности ввода цифр
    if 0 > x or x > (len(board_temp[0]) - 1) or 0 > y or y > (len(board_temp[0]) - 1):
        print('ОШИБОЧНЫЙ ВВОД! Попробуйте ещё раз.\n')
        continue
    # Проверка занята ли клетка
    if board_temp[y][x] == s:
        board_temp[y][x] = kr_nol
    else:
        print('КЛЕТКА ЗАНЯТА!!! Поробуйте ещё раз. \n')
        continue
    if check_winner(board_temp, winn_var):
        print(f'Игрок {n_gamer}, ВЫ ВЫИГРАЛИ!!! \n')
        if restart_game():
            continue
        else:
            break

    if True not in [s in board_temp[i] for i in range(len(board_temp))]:
        print('Ничья')
        if restart_game():
            continue
        else:
            break

    if n_gamer == 1:
        n_gamer = 2
        kr_nol = 'O'
    else:
        n_gamer = 1
        kr_nol = 'X'
