#maiding Kotobulka

def check_five_in_row(board, player, x, y):
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]  # Все направления для проверки
    for dx, dy in directions:
        count = 1  # Начинаем с 1, так как уже установлен символ в позиции (x, y)
        count += count_direction(board, player, x, y, dx, dy)  # Считаем в одном направлении
        count += count_direction(board, player, x, y, -dx, -dy)  # Считаем в обратном направлении
        if count >= 5:
            return True
    return False

def count_direction(board, player, x, y, dx, dy):
    count = 0
    nx, ny = x + dx, y + dy
    while 0 <= nx < len(board) and 0 <= ny < len(board[0]) and board[nx][ny] == player:
        count += 1
        nx, ny = nx + dx, ny + dy
    return count

i = int(input())
if i == 1:
    y, x =15, 15
if i == 2:
    y, x = 19, 19
m = [[0 for j in range(y)] for i in range(x)]
m[x // 2][y // 2] = 1
for i in range(x):
    print(m[i])
xod = 1
c = -1
scet1, scet2 = 0, 0
while xod < x * y:
    x1, y1 = map(int, input().split())
    if (x1 < x) and (y1 < y):
        if m[x1][y1] == 0:
            if c < 0:
                m[x1][y1] = -1
            else:
                m[x1][y1] = 1
            for i in range(x):
                print(m[i])
            if check_five_in_row(m, 1, x1, y1) or check_five_in_row(m, -1, x1, y1):
                print(f"Player {1 if m[x1][y1] == 1 else 2} wins!")
                break
            if xod == x*y -1:
                print ('Draw')
                break
            c *= -1
            xod += 1