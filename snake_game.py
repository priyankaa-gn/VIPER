import curses
import time
import random

#GAME FRAME MAP
    #Frame begins
    # Read keys
    # Update snake head
    # Check wall, food, bomb
    # clear()
    # draw border
    # draw snake
    # draw food
    # refresh()
    # Frame ends

def main(stdscr):
    curses.curs_set(0) #turns off cursor blinking 
    stdscr.clear()   #clears the screen 
    height,width = stdscr.getmaxyx() #gets the dimensions of the terminal window

# ---------------- INTRO ----------------
    
    #adding text to the centre of the terminal as an intro
    text = [
        "██╗   ██╗██╗██████╗ ███████╗██████╗", 
        " ██║   ██║██║██╔══██╗██╔════╝██╔══██╗",
        " ██║   ██║██║██████╔╝█████╗  ██████╔╝",
        " ╚██╗ ██╔╝██║██╔═══╝ ██╔══╝  ██╔══██╗",
        "  ╚████╔╝ ██║██║     ███████╗██║  ██║",
         "  ╚═══╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝",
    ]  
    y_start = (height // 2) - (len(text) // 2)
    for i, line in enumerate(text):
        x = (width // 2) - (len(line) // 2)
        stdscr.addstr(y_start + i, x, line)

    stdscr.refresh() #refresh to update the screen
    time.sleep(1)   #pauses the game for 2 sec
     

# ---------------- GAME WINDOW ----------------
    #building the game window
    box_height = height // 2 #dimension of game box(half the terminal)
    box_width = width // 2

    # Top-left corner coordinates (to center the box) 
    start_y = (height - box_height) // 2
    start_x = (width - box_width) // 2

    # Create the game window
    game_window = curses.newwin(box_height, box_width, start_y, start_x)

    # Draw border around the window
    game_window.box()

    # Add a title at the top of the box
    title = "** VIPER **" 
    title_x = (box_width // 2) - (len(title) // 2)
    game_window.addstr(0, title_x, title)

    # Refresh both windows
    stdscr.refresh()
    game_window.refresh()

    # Pause for a moment so you can see it
    stdscr.addstr(start_y + box_height + 1, start_x, "Press any key to continue...")
    stdscr.refresh()
    stdscr.getch() #waits for user input before exiting

    stdscr.clear()  #removes the 'press any key to continue' text after the usear input
    stdscr.refresh()

    stdscr.nodelay(True)
    # Set a refresh rate (snake movement speed)
    stdscr.timeout(100)  # milliseconds (100ms per frame)

# ---------------- COLORS ----------------
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_GREEN)   # snake
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)     # food
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_BLACK)  # bombs
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)    # border/title


# ---------------- INITIAL SNAKE ----------------
    snake = [
        [start_y + box_height // 2, start_x + box_width // 2 + 1],
        [start_y + box_height // 2, start_x + box_width // 2],
        [start_y + box_height // 2, start_x + box_width // 2 - 1],
    ]

    direction = curses.KEY_RIGHT


# ---------------- FOOD ----------------
    # Spawn first food INSIDE the box (not on walls)
    food = [
        random.randint(start_y + 1, start_y + box_height - 2),
        random.randint(start_x + 1, start_x + box_width - 2)
    ]

# ---------------- BOMBS ----------------
    #Spawn bombs that breaks the game once touched by the snake, multiple bombs are placed so we use a list
    bombs = []
    

# ---------------- GAME LOOP ----------------
    while True:
        key = stdscr.getch()

        # If user pressed a key,it moves right, if no key is pressed it moves right as it is the default direction that is set
        if key != -1:
            if key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
                direction = key

        head = snake[0].copy()   # copy the head coordinates to avoid memory change in the original coordinates

        if direction == curses.KEY_UP:
            head[0] -= 1   # move up (row -1)
        elif direction == curses.KEY_DOWN:
            head[0] += 1   # move down (row +1)
        elif direction == curses.KEY_LEFT:
            head[1] -= 1   # move left (col -1)
        elif direction == curses.KEY_RIGHT:
            head[1] += 1   # move right (col +1)


        # ---------------- WRAP AROUND ----------------
        #When snake moves off the right side it appears on the left and when it moves of the top it appears at the bottom
        if head[0] <= start_y:
            head[0] = start_y + box_height - 2
        elif head[0] >= start_y + box_height - 1:
            head[0] = start_y + 1

        if head[1] <= start_x:
            head[1] = start_x + box_width - 2
        elif head[1] >= start_x + box_width - 1:
            head[1] = start_x + 1
    
        snake.insert(0, head)    # add new head to front


        # ---------------- FOOD EATEN ----------------
        #check if food is eaten 
        if head == food or head == [food[0], food[1] + 1]:
            #food disappears automatically as we clear each frame
            #do not pop(), let the snake grow
            #new food is spawn once head == food 
            food = [
            random.randint(start_y + 1, start_y + box_height - 2),
            random.randint(start_x + 1, start_x + box_width - 3)
            ]
        else:   
            snake.pop()              # remove tail (movement)


        # ---------------- BOMB SPAWNING ----------------
        #random.random() returns a random float between 0.0 and 1.0, if the float is less than 0.02 a bomb appears (2% chance of appaearing)
        if random.random() < 0.02 and len(bombs) < 8:
            new_bomb = [
                random.randint(start_y + 1, start_y + box_height - 2),
                random.randint(start_x + 1, start_x + box_width - 3)]
            if new_bomb not in snake and new_bomb != food:
                bombs.append(new_bomb)    

        # ---------------- BOMB COLLISION ----------------
        #checks if the snake and bomb coordinates are same
        for by, bx in bombs:
            if head == [by, bx] or head == [by, bx+1]:
                return #exits the funtion aka the game

        # ---------------- DRAWING ----------------
        game_window.clear()      #to clear the trails left by the snake 
        game_window.box()        #to add the box that got erased dur to .clear()

        # Add title at top of box
        tx = (box_width // 2) - (len(title) // 2)
        game_window.addstr(0, tx, title)


         # draw food
        fy, fx = food
        game_window.addstr(fy - start_y, fx - start_x, '🍎', curses.color_pair(2))

         # draw bombs
        for by, bx in bombs:
            game_window.addstr(by - start_y, bx - start_x, '💣', curses.color_pair(3))
 
        # Draw each part of the snake,the snake has global terminal coordinates and we have to convert them to the game window coordinates
        for y, x in snake:
            game_window.addstr(y - start_y, x - start_x, '🬋', curses.color_pair(1)) #adds character in the given coordinates ( ▀ character for future use)
    

        #UPDATES SCREEN
        game_window.refresh()

curses.wrapper(main) 
 #Initializes curses (sets up screen, disables line buffering, etc.)Calls your function (passing in the stdscr object),Cleans up and resets the terminal when your code finishes (even if it crashes)

