import pygame
import time

pygame.font.init()
pygame.mixer.init()
WIDTH = 1000
HEIGHT = int(WIDTH * .7)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect4Super")
WORD_FONT = pygame.font.SysFont('comicsans', 35)
WIN_FONT = pygame.font.SysFont('comicsans', 70)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
FPS = 60
SIZE = 75

RED_COIN = pygame.image.load('./assets/redcoin.png')
RED_COIN = pygame.transform.scale(RED_COIN, (SIZE, SIZE))

YELLOW_COIN = pygame.image.load('./assets/yellowcoin.png')
YELLOW_COIN = pygame.transform.scale(YELLOW_COIN, (SIZE, SIZE))

BOARD = pygame.image.load('./assets/board.png')

FALL_SOUND = pygame.mixer.Sound('./assets/fallsound.wav')
WIN_SOUND = pygame.mixer.Sound('./assets/winsound.wav')

def set_up():
    global current_piece
    global board
    global filled_pieces
    global move_num
    filled_pieces = []
    move_num = 0
    board = []
    x_piece = 181
    y_piece = 155
    for i in range(6):
        board.append([])
        for j in range(7):
            k = [(x_piece, y_piece), False]
            board[i].append(k)
            x_piece += 90
        x_piece = 181
        y_piece += 87


def print_board():
    global board
    for row in board:
        r = ""
        for item in row:
            r += " " + str(item)
        print(r)


def draw_window(piece):
    global move_num
    WIN.fill(BLACK)
    WIN.blit(WORD_FONT.render("CONNECT4SUPER", 1, WHITE), (690, 0))
    if move_num % 2 == 0:
        text = WORD_FONT.render("RED PLAYER", 1, RED)
    else:
        text = WORD_FONT.render("YELLOW PLAYER", 1, YELLOW)
    WIN.blit(text, (0, 0))
    WIN.blit(BOARD, (95, 128))
    for p in filled_pieces:
        WIN.blit(p[1], (p[0][0], p[0][1]))
    WIN.blit(current_piece, (piece.x, piece.y))
    pygame.display.update()


def piece_fall(piece):
    global move_num
    WIN.fill(BLACK)
    WIN.blit(WORD_FONT.render("CONNECT4SUPER", 1, WHITE), (690, 0))
    if move_num % 2 == 0:
        text = WORD_FONT.render("RED PLAYER", 1, RED)
    else:
        text = WORD_FONT.render("YELLOW PLAYER", 1, YELLOW)
    WIN.blit(text, (0, 0))
    WIN.blit(current_piece, (piece.x, piece.y))
    WIN.blit(BOARD, (95, 128))
    for p in filled_pieces:
        WIN.blit(p[1], (p[0][0], p[0][1]))
    pygame.display.update()


def check_win():
    if check_hori() or check_ver() or check_dia():
        return True


def check_hori():
    global board
    for row in range(5, -1, -1):
        count = 1
        for col in range(1, 7):
            if board[row][col][1] is not False:
                if board[row][col - 1][1] == board[row][col][1]:
                    count += 1
                else:
                    count = 1
            if count == 4:
                print('hori')
                return True


def check_ver():
    global board
    for col in range(0, 7, 1):
        count = 1
        for row in range(5, 0, -1):
            if board[row][col][1] is not False:
                if board[row - 1][col][1] == board[row][col][1]:
                    count += 1
                else:
                    count = 1
            if count == 4:
                print("ver")
                return True


def check_dia():
    global board
    global current_piece
    m, a, b = 1, 0, 4
    for check in range(2):
        for row in range(5, 2, -1):
            for item in range(a, b):
                for i in range(4):
                    if board[row - i][item + (m * i)][1] != current_piece:
                        break
                else: # no break
                    print("dia")
                    return True
        m, a, b = -1, 3, 7


# moving horizontal is +- 90
# moving vertical is += 87
def fill_board():
    x = 181
    y = 155
    for i in range(6):
        for j in range(7):
            if i != 0 or j != 0:
                if i % 2 == 0:
                    WIN.blit(RED_COIN, (x, y))
                else:
                    WIN.blit(YELLOW_COIN, (x, y))
            x += 90
        x = 181
        y += 87


def main():
    set_up()
    global current_piece
    global board
    global filled_pieces
    global move_num
    piece = pygame.Rect(451, 50, SIZE, SIZE)
    clock = pygame.time.Clock()
    if move_num % 2 == 0:
        current_piece = RED_COIN
    else:
        current_piece = YELLOW_COIN
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and piece.y == 50:
                    open_slot = 154
                    for row in board:
                        for item in row:
                            if item[0][0] == piece.x and item[1] is False and item[0][1] > open_slot:
                                open_slot = item[0][1]
                    if open_slot > 154:
                        FALL_SOUND.play()
                        while piece.y < open_slot:
                            piece.y += 10
                            piece_fall(piece)
                        pos = (piece.x, open_slot)
                        filled_pieces.append([pos, current_piece])
                        for i in board:
                            for j in i:
                                if pos == j[0]:
                                    j[1] = current_piece
                        if check_win():
                            end_game()
                        piece.y = 50
                        move_num += 1
                        if move_num % 2 == 0:
                            current_piece = RED_COIN
                        else:
                            current_piece = YELLOW_COIN
        keys_pressed = pygame.key.get_pressed()
        if (keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]) and piece.x > 181:
            piece.x -= 90
            time.sleep(0.1)
        elif (keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]) and piece.x < 721:
            piece.x += 90
            time.sleep(0.1)
        if run is not False:
            draw_window(piece)
    end_game()


def end_game():
    global current_piece
    global filled_pieces
    WIN.fill(BLACK)
    if current_piece == RED_COIN:
        color = RED
    else:
        color = YELLOW
    WIN_SOUND.play()
    text = WIN_FONT.render("CONNECT FOUR!", 1, color)
    WIN.blit(BOARD, (95, 128))
    for p in filled_pieces:
        WIN.blit(p[1], (p[0][0], p[0][1]))
    WIN.blit(text, (WIDTH/2 - text.get_width()/2, 0))
    subtext = WORD_FONT.render("(space to rematch)", 1, color)
    WIN.blit(subtext, (WIDTH/2 - subtext.get_width()/2, 80))
    pygame.display.update()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                main()
    pygame.quit()


if __name__ == "__main__":
    main()
