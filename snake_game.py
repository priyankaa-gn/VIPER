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

# ----------------------------------------------------------
# MAIN GAME
# ----------------------------------------------------------
def main(stdscr):
    curses.curs_set(0) #turns off cursor blinking 

# ---------------- COLORS ----------------
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_GREEN)   # snake
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)     # food
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_BLACK)  # bombs
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)    # border/title

    stdscr.clear()   #clears the screen 
    height,width = stdscr.getmaxyx() #gets the dimensions of the terminal window

# ---------------- INTRO ----------------
    intro_h = height // 2
    intro_w = width // 2
    intro_y = (height - intro_h) // 2
    intro_x = (width - intro_w) // 2

    intro_win = curses.newwin(intro_h, intro_w, intro_y, intro_x)
    intro_win.box()
    #adding text to the centre of the terminal as an intro
    text = [
        "██╗   ██╗██╗██████╗ ███████╗██████╗", 
        " ██║   ██║██║██╔══██╗██╔════╝██╔══██╗",
        " ██║   ██║██║██████╔╝█████╗  ██████╔╝",
        " ╚██╗ ██╔╝██║██╔═══╝ ██╔══╝  ██╔══██╗",
        "  ╚████╔╝ ██║██║     ███████╗██║  ██║",
        "   ╚═══╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝",
    ]  
    y_start = (height // 2) - (len(text) // 2)
    for i, line in enumerate(text):
        x = (width // 2) - (len(line) // 2)
        stdscr.addstr(y_start + i, x, line)

    # Fullscreen suggestion
    fs_msg = "For best experience, use FULLSCREEN"
    stdscr.addstr(y_start + len(text) + 2, (width // 2) - (len(fs_msg) // 2), fs_msg, curses.A_BOLD)

    stdscr.refresh() #refresh to update the screen
    time.sleep(2.5)   #pauses the game for 2 sec
     

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
    title = "༼ VIPER 🐍..🍎..💣 ༽" 
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
        if random.random() < 0.02:  # 2% chance of spawning per frame

            # If bombs reach half capacity (4), randomly remove one to "move" it
            if len(bombs) >= 4:
                bombs.pop(random.randint(0, len(bombs)-1))

            # Only allow max 8 bombs at once
            if len(bombs) < 8:
                new_bomb = [
                    random.randint(start_y + 1, start_y + box_height - 2),
                    random.randint(start_x + 1, start_x + box_width - 3)
                ]

                # ensure bomb doesn't spawn on snake or food
                if new_bomb not in snake and new_bomb != food:
                    bombs.append(new_bomb)     

        # ---------------- BOMB COLLISION ----------------
        #checks if the snake and bomb coordinates are same
        # Also triggered when user presses Q to quit
        quit_pressed = (key in (ord('q'), ord('Q')))

        bomb_hit = False
        for by, bx in bombs:
            if head == [by, bx] or head == [by, bx + 1]:
                bomb_hit = True
                break

        if bomb_hit or quit_pressed:

            #------------- OUTRO SCREEN ------------------
                game_window.clear()
                game_window.border()
                game_window.refresh() # to avoid having the score shown on the top right after the game ends

                #ASCII art for score
                score_art = r'''
                 _______  _______  _______  _______    _______           _______  _______ 
                (  ____ \(  ___  )(       )(  ____ \  (  ___  )|\     /|(  ____ \(  ____ )
                | (    \/| (   ) || () () || (    \/  | (   ) || )   ( || (    \/| (    )|
                | |      | (___) || || || || (__      | |   | || |   | || (__    | (____)|
                | | ____ |  ___  || |(_)| ||  __)     | |   | |( (   ) )|  __)   |     __)
                | | \_  )| (   ) || |   | || (        | |   | | \ \_/ / | (      | (\ (   
                | (___) || )   ( || )   ( || (____/\  | (___) |  \   /  | (____/\| ) \ \__
                (_______)|/     \||/     \|(_______/  (_______)   \_/   (_______/|/   \__/                                                                                                
                    '''.splitlines()
                height_win, width_win = game_window.getmaxyx()
                ascii_height = len(score_art)
                ascii_width = max(len(line) for line in score_art)

                # Determine max number of lines that fit
                max_lines = height_win - 4  # leave space for score/instructions
                start_line = max(1, (height_win - min(ascii_height, max_lines)) // 2)

                # Draw ASCII art, clipped to width and available lines
                for i, line in enumerate(score_art[:max_lines]):
                    clipped = line[:width_win - 2]  # leave margin
                    game_window.addstr(start_line + i, 1, clipped, curses.color_pair(4))

                # Draw numeric score below ASCII
                score_text = f"Score : {len(snake) - 3}"
                score_y = min(start_line + len(score_art), height_win - 3)
                score_x = max(1, (width_win - len(score_text)) // 2)
                game_window.addstr(score_y, score_x, score_text, curses.color_pair(2))

                # Draw restart instructions
                instr = "Press [R] to Restart  |  Any other key to Exit"
                instr_y = min(score_y + 2, height_win - 2)
                instr_x = max(1, (width_win - len(instr)) // 2)
                game_window.addstr(instr_y, instr_x, instr, curses.color_pair(4))

                game_window.refresh()
                #remove the nodelay to avoid outro vanishing
                game_window.nodelay(False)

                # wait for user before exiting
                key = game_window.getch()
                if key in (ord('r'), ord('R')):
                    return main(stdscr)  # restart the game
                else:
                    return  # exit the game

        # ---------------- DRAWING ----------------
        game_window.clear()      #to clear the trails left by the snake 
        game_window.box()        #to add the box that got erased dur to .clear()

        # Quit message bottom-left
        quit_msg = "Quit : [Q]"
        game_window.addstr(box_height - 1, 2, quit_msg, curses.color_pair(4))

        # Add title at top of box
        tx = (box_width // 2) - (len(title) // 2)
        game_window.addstr(0, tx, title)

        # ---------- SCORE DRAWING ----------
        score_text = f"Score: {len(snake) - 3}"
        game_window.addstr(0, 2, score_text, curses.color_pair(4))

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

