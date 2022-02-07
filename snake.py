import curses, random, os
from curses import textpad

def create_food(snake, box):
    food = None
    while not food:
        food = [random.randint(box[0][0] + 2 , box[1][0] - 2), random.randint(box[0][1] + 2 , box[1][1] - 2)]
        if food in snake:
            food = None
    return food
def save_score(scorefile, score):
    old_score = 0
    try:
        sf1 = open(scorefile,"r")
        linetab = sf1.read().split(" ")
        old_score = int(linetab[-1])
        sf1.close()
    except:
        sf1 = open(scorefile,"w")
    with open(scorefile,"w") as sf2:
        if score > old_score:
            sf2.write(f"Best score: {score}")
        else:
            sf2.write(f"Best score: {old_score}")
def print_score(stdscr, score,color):
    sh, sw = stdscr.getmaxyx()
    score_text = f"Score: {score}"
    stdscr.addstr(0, sw // 2 - len(score_text) // 2, score_text, color)
    stdscr.refresh()
    
def main(stdscr):
    curses.curs_set(0)
    curses.mousemask(1)
    stdscr.nodelay(1)
    stdscr.timeout(150)
    
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2,curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3,curses.COLOR_CYAN, curses.COLOR_BLACK)
    colors = [curses.color_pair(1), curses.color_pair(2), curses.color_pair(3)]
    sh,sw = stdscr.getmaxyx()
    box = [[1,0],[sh - 2, sw - 2]]
    textpad.rectangle(stdscr,box[0][0], box[0][1], box[1][0], box[1][1])
    
    snake = [[sh // 2,sw // 2 + 1],[sh // 2,sw // 2],[sh // 2,sw // 2 - 1]]
    direction = curses.KEY_RIGHT
    
    keylist = [curses.KEY_BACKSPACE, curses.KEY_MOUSE, curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_UP, curses.KEY_DOWN]
    for y,x in snake:
        stdscr.addstr(y,x,"#", colors[2])
    food = create_food(snake, box)
    stdscr.addstr(food[0], food[1], "*", colors[0])
    score = 0
    print_score(stdscr, score, colors[1])
    mouse_direction = "RIGHT"
    xmouse = ["LEFT","RIGHT"]
    ymouse = ["UP","DOWN"]

    while 1:
        key = stdscr.getch()
        if key in keylist:
            direction = key
            if direction == curses.KEY_MOUSE:
                mouseon = True
                _,x,y,_,_ = curses.getmouse()
                if y < sh // 2 and mouse_direction in xmouse:
                    mouse_direction = "UP"
                elif y > sh // 2 and mouse_direction in xmouse:
                    mouse_direction = "DOWN"
                elif x < sw // 2 and mouse_direction in ymouse:
                    mouse_direction = "LEFT"
                elif x > sw // 2 and mouse_direction in ymouse:
                    mouse_direction = "RIGHT"
          

        head = snake[0]
        if direction == curses.KEY_RIGHT:
            new_head = [head[0], head[1] + 1]
        elif direction == curses.KEY_LEFT:
            new_head = [head[0], head[1] - 1]
        elif direction == curses.KEY_UP:
            new_head = [head[0] - 1, head[1]]
        elif direction == curses.KEY_DOWN:
            new_head = [head[0] + 1, head[1]]
        elif direction == curses.KEY_BACKSPACE:
            break
        elif mouseon:
            if mouse_direction == "UP":
                new_head = [head[0] - 1, head[1]]
            elif mouse_direction == "DOWN":
                new_head =[head[0] + 1, head[1]]
            elif mouse_direction == "LEFT":
                new_head = [head[0], head[1] - 1]
            elif mouse_direction == "RIGHT":
                new_head = [head[0], head[1] + 1]
        snake.insert(0,new_head)
        stdscr.addstr(new_head[0], new_head[1], "#", colors[2])
        if snake[0] == food:
            food = create_food(snake, box)
            stdscr.addstr(food[0], food[1], "*", colors[0])
            score += 1
            print_score(stdscr, score, colors[1])
        else:
            stdscr.addstr(snake[-1][0], snake[-1][1], " ")
            snake.pop()
        
        
            
        if (snake[0][0] in [box[0][0], box[1][0]] or snake[0][1] in [box[0][1], box[1][1]]):
            msg_p1 = "Game Over!\n"
            msg_p2 = "Curses snake game\n"
            msg_p3 = "Based on Indian Pythonista's code\n"
            msg_p4 = "With the help of Tech with Tim's curses tutorial\n"
            stdscr.addstr(sh // 2, sw // 2 - len(msg_p1) // 2, msg_p1,colors[0])
            stdscr.addstr(sh // 2 + 1, sw // 2 - len(msg_p2) // 2, msg_p2,colors[2])
            stdscr.addstr(sh // 2 + 2, sw // 2 - len(msg_p3) // 2, msg_p3,colors[0])
            stdscr.addstr(sh // 2 + 3, sw // 2 - len(msg_p4) // 2, msg_p4,colors[2])
            save_score("scores.txt",score)
            stdscr.nodelay(0)
            stdscr.getch()
            break
        stdscr.refresh()
    
curses.wrapper(main)
