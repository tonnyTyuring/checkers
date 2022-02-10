for i in range(255):
    print(str(i) + ") " + chr(i) + "  ", end="")
    i += 1
    if (i % 5 == 0):
        print()


def sign(int):
    if int > 0:
        return (1)
    elif int == 0:
        return (0)
    else:
        return (-1)


print("--------------------------")

def isAbleToEat(figure, team, enemy, isprint=True):
    can_eat = False
    if board[figure[0]][figure[1]] == team[0]:
        for i in [-2, 2]:
            for j in [-2, 2]:
                if 0 <= figure[0] + i <= 7 and 0 <= figure[1] + j <= 7:
                    if (board[figure[0] + sign(i)][figure[1] + sign(j)] == (enemy[0] or enemy[1])) \
                            and (board[figure[0] + i][figure[1] + j] == ' '):
                        if isprint:
                            print(figure, "-eat->", figure[0] + i, figure[1] + j)
                        can_eat = True
    if board[figure[0]][figure[1]] == team[1]:
        for i in [-1, 1]:
            for j in [-1, 1]:
                for k in range(2, 7):
                    if 0 <= figure[0] + k * i <= 7 and 0 <= figure[1] + k * j <= 7:
                        if (board[figure[0] + k * i][figure[1] + k * j] == ' ') \
                                and (board[figure[0] + (k - 1) * i][figure[1] + (k - 1) * j] == (enemy[0] or enemy[1])):
                            if isprint:
                                print(figure, "-eat->", figure[0] + k * i, figure[1] + k * j)
                            can_eat = True
                            break
    if can_eat:
        return True
    return False


def canFigureGo(figure, team):
    can_go = False
    if board[figure[0]][figure[1]] == team[0]:
        for i in [-1]:
            for j in [-1, 1]:
                if 0 <= figure[0] + i <= 7 and 0 <= figure[1] + j <= 7:
                    if board[figure[0] + i][figure[1] + j] == ' ':
                        print(figure, "-go->", figure[0] + i, figure[1] + j)
                        can_go = True
    if board[figure[0]][figure[1]] == team[1]:
        for i in [-1, 1]:
            for j in [-1, 1]:
                for k in range(1, 7):
                    if 0 <= figure[0] + k * i <= 7 and 0 <= figure[1] + k * j <= 7:
                        if board[figure[0] + k * i][figure[1] + k * j] == ' ':
                            print(figure, "-go->", figure[0] + i, figure[1] + j)
                            can_go = True
    if can_go:
        return True
    return False


def flip(board):
    board_buf = [['#' if i % 2 == (0 if j % 2 == 0 else 1) else ' ' for i in range(8)] for j in range(8)]
    row = len(board)
    collumn = len(board[0])
    while row > 0:
        while collumn > 0:
            board_buf[len(board) - row][len(board[0]) - collumn] = board[row - 1][collumn - 1]
            collumn -= 1
        row -= 1
        collumn = len(board[0])

    return board_buf


def turn(team, enemy, board):
    for c in board:
        print(c)

    can_eat = False
    can_go = False
    dead = True
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == team[0] or board[i][j] == team[1]:
                if isAbleToEat((i, j), team, enemy):
                    can_eat = True
                dead = False

    if can_eat:
        print("you need to eat one of those")

    else:
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == (team[0] or team[1]):
                    if canFigureGo((i, j), team):
                        can_go = True

    if can_eat or can_go:
        figure = [int(input("row: ")), int(input("column: "))]
        if 0 <= figure[0] <= 7 and 0 <= figure[1] <= 7:
            if board[figure[0]][figure[1]] == team[0]:
                print("it is your checker")
                while can_eat:
                    print("this is your current figure:", figure)
                    if isAbleToEat(figure, team, enemy):
                        print("you need to eat one of those")
                        print("where to go?")
                        next_position = [int(input("row: ")), int(input("column: "))]
                        print(next_position)
                        if 0 <= next_position[0] <= 7 and 0 <= next_position[1] <= 7:
                            if board[next_position[0]][next_position[1]] == ' ':
                                print("this is empty place")
                                if (board[figure[0] + sign(next_position[0] - figure[0])] \
                                        [figure[1] + sign(next_position[1] - figure[1])] \
                                        == enemy[0] or \
                                    board[figure[0] + sign(next_position[0] - figure[0])] \
                                        [figure[1] + sign(next_position[1] - figure[1])] \
                                        == enemy[1]) and \
                                        abs(next_position[0] - figure[0]) == 2 and\
                                        abs(next_position[1] - figure[1]) == 2:

                                    if next_position[0] == 0:
                                        board[next_position[0]][next_position[1]] = team[1]
                                    else:
                                        board[next_position[0]][next_position[1]] = team[0]

                                    board[figure[0]][figure[1]] = ' '
                                    board[figure[0] + sign(next_position[0] - figure[0])] \
                                        [figure[1] + sign(next_position[1] - figure[1])] = ' '

                                    print("Nom nom")

                                    if isAbleToEat(next_position, team, enemy, isprint=False):
                                        figure = next_position
                                        for c in board:
                                            print(c)
                                        print("continue to eat")
                                    else:
                                        can_eat = False
                                        break
                                else:
                                    turn(team, enemy, board)
                                    print("no, you need to eat")
                            else:
                                turn(team, enemy, board)
                                print("it is wrong place")
                        else:
                            turn(team, enemy, board)
                            print("it is wrong place")
                    else:
                        turn(team, enemy, board)
                        print("but chose figure that can eat")
                else:
                    next_position = [int(input("row: ")), int(input("column: "))]
                    print(next_position)
                    if 0 <= next_position[0] <= 7 and 0 <= next_position[1] <= 7:
                        if board[next_position[0]][next_position[1]] == ' ':
                            print("this is epty place")
                            if next_position[0] - figure[0] == -1 and abs(next_position[1] - figure[1]) == 1:
                                print("right place")

                                if next_position[0] == 0:
                                    board[next_position[0]][next_position[1]] = team[1]
                                else:
                                    board[next_position[0]][next_position[1]] = team[0]

                                board[figure[0]][figure[1]] = ' '

                                print("turn end")
                                return True

                            else:
                                turn(team, enemy, board)
                                print("it is wrong place")

                        else:
                            turn(team, enemy, board)
                            print("this place is engaged")

                    else:
                        turn(team, enemy, board)
                        print("next position is out of bord")
            elif board[figure[0]][figure[1]] == team[1]:
                print("it is your checker queen")
                while can_eat:
                    print("this is your current figure: ", figure)
                    if isAbleToEat(figure, team, enemy):
                        print("you need to eat one of those")
                        print("where to go?")
                        next_position = [int(input("row: ")), int(input("column: "))]
                        print(next_position)
                        if 0 <= next_position[0] <= 7 and 0 <= next_position[1] <= 7:
                            if board[next_position[0]][next_position[1]] == ' ':
                                print("this is empty place")
                                if (board[figure[0] + next_position[0] - sign(next_position[0] - figure[0])] \
                                        [figure[1] + next_position[0] - sign(next_position[1] - figure[1])] \
                                        == enemy[0] or \
                                    board[figure[0] + next_position[0] - sign(next_position[0] - figure[0])] \
                                        [figure[1] + next_position[0] - sign(next_position[1] - figure[1])] \
                                        == enemy[1]) and \
                                        abs(next_position[0] - figure[0]) == abs(next_position[1] - figure[1]):

                                    board[next_position[0]][next_position[1]] = team[1]

                                    board[figure[0]][figure[1]] = ' '
                                    board[figure[0] + sign(next_position[0] - figure[0])] \
                                        [figure[1] + sign(next_position[1] - figure[1])] = ' '

                                    print("Nom nom")

                                    if isAbleToEat(next_position, team, enemy, isprint=False):
                                        figure = next_position
                                        for c in board:
                                            print(c)
                                        print("continue to eat")
                                    else:
                                        can_eat = False
                                        break
                            else:
                                turn(team, enemy, board)
                                print("no, you need to eat eat")
                        else:
                            turn(team, enemy, board)
                            print("it is wrong place")
                    else:
                        turn(team, enemy, board)
                        print("but chose figure that can eat")
                else:
                    next_position = [int(input("row: ")), int(input("column: "))]
                    print(next_position)
                    if 0 <= next_position[0] <= 7 and 0 <= next_position[1] <= 7:
                        if board[next_position[0]][next_position[1]] == ' ':
                            print("this is epty place")
                            if next_position[0] - figure[0] == abs(next_position[1] - figure[1]):
                                print("right place")

                                board[next_position[0]][next_position[1]] = team[1]

                                board[figure[0]][figure[1]] = ' '

                                print("turn end")

                            else:
                                turn(team, enemy, board)
                                print("it is wrong place")
                        else:
                            turn(team, enemy, board)
                            print("this place is engaged")
                    else:
                        turn(team, enemy, board)
                        print("next position is out of bord")
            else:
                turn(team, enemy, board)
                print("it is not your")

    if dead:
         print("team: ", enemy, " win")
         return False

    else:
        print("your turn end")
        return True


# Заполнение поля
board = [['#' if i % 2 == (0 if j % 2 == 0 else 1) else ' ' for i in range(8)] for j in range(8)]

team1 = ['o', 'O']
team2 = ['ø', 'Ø']

for i in range(3):
    for j in range(len(board[i])):
        if board[i][j] == ' ':
            board[i][j] = team2[0]

for i in range(3):
    for j in range(len(board[i])):
        if board[5 + i][j] == ' ':
            board[5 + i][j] = team1[0]

while (turn(team1, team2, board)):
    team1, team2 = team2, team1
    board = flip(board)
    print("board flip")
