'''
    PONG game in command line
    implemented with curses library in python
    Date : 2024-Feb-23
'''
import curses
import time

stdscr = curses.initscr()

curses.noecho()
curses.cbreak()
stdscr.keypad(True)
stdscr.nodelay(True)
curses.curs_set(False)

## CONSTANTS
ROW_MAX = curses.LINES
COL_MAX = curses.COLS
# print(ROW_MAX, COL_MAX)

TABLE_ROW_MIN = 3
TABLE_ROW_MAX = ROW_MAX

TABLE_COL_MIN = 0
TABLE_COL_MAX = COL_MAX

PADDLE_COL_SHIFT = 4

PADDLE_CHAR = '\u2588'
PADDLE_H = 10
PADDLE_W = 1

BALL_CHAR = '\u2588'
BALL_H = 1
BALL_W = 1

class Paddle:
    def __init__(self, stdscr, r=0, c=0, side='left') -> None:
        self.stdscr = stdscr
        self.r = r
        self.c = c
        self.side = side

        self.score = 0
    # def move(self, r, c):
    #     self.r = r
    #     self.c = c
    def up(self):
        if self.r > TABLE_ROW_MIN:
            self.r -= 1

    def down(self):
        if self.r + PADDLE_H < TABLE_ROW_MAX:
            self.r += 1

    def draw(self):
        for i in range(PADDLE_H):
            self.stdscr.addstr(self.r+i, self.c, PADDLE_W*PADDLE_CHAR)

    def is_touched(self, ball):
        if ball.c == self.c and ball.r >= self.r and ball.r <= self.r + PADDLE_H:
            # for _ in range(1000):
            #     a = 10
            return True
        return False
        
    
class Ball:
    def __init__(self, stdscr, r=10, c=10) -> None:
        self.stdscr = stdscr
        self.r = r
        self.c = c

        self.dr = 1
        self.dc = 1

        self.vr = -1
        self.vc = -1

    def goto_center(self):
        self.c = TABLE_COL_MAX // 2
        self.r = TABLE_ROW_MAX // 2

    def draw(self):
        for i in range(BALL_H):
            self.stdscr.addstr(self.r+i, self.c, BALL_W*BALL_CHAR)




p1 = Paddle(stdscr, r=ROW_MAX // 2 - PADDLE_H // 2, c=0+PADDLE_COL_SHIFT)
p2 = Paddle(stdscr, r=ROW_MAX // 2 - PADDLE_H // 2, c=COL_MAX - PADDLE_COL_SHIFT)
ball = Ball(stdscr, r=TABLE_ROW_MAX//2, c=TABLE_COL_MAX//2)

p1.draw()
p2.draw()
ball.draw()
stdscr.refresh()

counter = 0
while True:
    try:
        key = stdscr.getkey()
    except:
        key = None

    if key == 'q':              break
    elif key == 'w':            p1.up()     # p1.r -= 1
    elif key == 's':            p1.down()   # p1.r += 1
    elif key == 'KEY_UP':       p2.up()
    elif key == 'KEY_DOWN':     p2.down()
    

    counter += 1    ## delay for ball moving
    if counter == 35:
        counter = 0

        ## move the ball
        ball.r += ball.dr * ball.vr
        ball.c += ball.dc * ball.vc

        if ball.r >= TABLE_ROW_MAX:
            ball.r = TABLE_ROW_MAX-1
            ball.vr *= -1

        if ball.r <= TABLE_ROW_MIN:
            ball.r = TABLE_ROW_MIN
            ball.vr *= -1

        if ball.c > p2.c:
            ball.goto_center()
            ball.vc *= -1

            p1.score += 1

        if ball.c < p1.c:
            ball.goto_center()
            ball.vc *= -1

            p2.score += 1

        if p2.is_touched(ball) or p1.is_touched(ball):
            ball.c -= ball.dc * ball.vc
            ball.vc *= -1

    stdscr.clear()

    stdscr.addstr(TABLE_ROW_MIN-3, COL_MAX // 4, f'Player 1: {p1.score}', curses.A_REVERSE)
    stdscr.addstr(TABLE_ROW_MIN-3, 3 * COL_MAX // 4, f'Player 2: {p2.score}')
    
    stdscr.addstr(TABLE_ROW_MIN-2, COL_MAX // 4, 'Up / Down Arrow Key')
    stdscr.addstr(TABLE_ROW_MIN-2, 3 * COL_MAX // 4, 'w / s Key')
    
    stdscr.addstr(TABLE_ROW_MIN-1, 0, '\u2588'*COL_MAX)
    
    p1.draw()
    p2.draw()
    ball.draw()

    stdscr.refresh()
