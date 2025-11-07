from tkinter import *
from functools import partial

from config import P1_COLOR, P1_NAME, P2_COLOR, P2_NAME, B_COLOR, P_WIDTH, INTERVAL, ROOT

# Track last piece selected
last_piece_selected = {
    "key": '',
    "color": 'gray',
    "player": '',
    "piece": '',
    "placed": False
}

# Track last piece played
last_piece_played = {
    "key": '',
    "player": '',
    "space": [],
}

# Track game board state
game_board_state = [
    ["0x0", "1x0", "2x0", "3x0"],
    ["0x1", "1x1", "2x1", "3x1"],
    ["0x2", "1x2", "2x2", "2x3"],
    ["0x3", "1x3", "2x3", "3x3"],
]

# Track player score
p_score = {
    P1_NAME: 0,
    P2_NAME: 0,
}

p_count = {
    P1_NAME: 8,
    P2_NAME: 8
}

current_player = P1_NAME

def on_enter(event):

    if "!canvas" not in str(event.widget).split(".")[-1] and last_piece_played["key"] != '':
       
        sp_x, sp_y = [int(s) for s in (str(event.widget).split(".")[-1].split(','))]

        if check_valid_place(sp_x, sp_y):
            event.widget.config(bg="blue")
        else:
            event.widget.config(bg="black")
    else:
        event.widget.config(bg="blue")


def on_leave(board, event):
    if board == P1_NAME:
        event.widget.config(bg=P1_COLOR)
    elif board == P2_NAME:
        event.widget.config(bg=P2_COLOR)
    else:
        event.widget.config(bg=B_COLOR)

def on_click_player(key, player, color, piece, message_label, event):

    global last_piece_selected

    win_width = ROOT.winfo_width()
    
    if current_player == player:

        if last_piece_selected["piece"]:
         show_piece(last_piece_selected["key"], last_piece_selected["piece"])

        sp_x = (win_width - P_WIDTH) / 2

        sp_label = Label(ROOT, text = f" {player}'s Selected Piece")
        sp_label.place(x = sp_x, y = 5)

        sp_canvas = Canvas(ROOT, width = P_WIDTH, height  = P_WIDTH, bg=color)
        sp_canvas.place(x = sp_x, y = 25)

        event.widget.delete("all")

        sp_canvas.create_rectangle(0, 0, P_WIDTH, P_WIDTH, width = 3)

        show_piece(key, sp_canvas)

        last_piece_selected["key"] = key
        last_piece_selected["color"] = color
        last_piece_selected["player"] = player
        last_piece_selected["piece"] = piece
        last_piece_selected["placed"] = False

    else:
        message_label.config(text = f"It is {current_player}'s turn.")

def on_click_board(message_label, current_label, p1_label, p2_label, event):

    global current_player
    global last_piece_played
    global last_piece_selected

    w_x = event.widget.winfo_x()
    w_y = event.widget.winfo_y()

    message_label.config(text = '')

    if last_piece_selected["key"] != '':

        if event.widget.cget("bg") == "blue":

            if not last_piece_selected["placed"]:

                last_piece_selected["placed"] = True

                pp_canvas = Canvas(ROOT, width = P_WIDTH, height  = P_WIDTH, bg=last_piece_selected["color"])
                pp_canvas.place(x = w_x, y = w_y)

                event.widget.place_forget()

                show_piece(last_piece_selected["key"], pp_canvas)

                last_piece_played["key"] = last_piece_selected["key"]
                last_piece_played["player"] = last_piece_selected["player"]
                last_piece_played["space"] = str(event.widget).split(".")[-1]

                last_piece_selected["piece"] = ''
                
                record_piece()
                check_score()

                if current_player == P1_NAME and check_valid_any():
                    current_player = P2_NAME
                    current_label.config(text = f"Current Player: {current_player}")
                elif current_player == P2_NAME and check_valid_any():
                    current_player = P1_NAME
                    current_label.config(text = f"Current Player: {current_player}")
                else:
                    last_piece_played["key"] = ''
                    last_piece_played["player"] = ''
                    last_piece_played["space"] = []
                    message_label.config(text = f"No valid placement available. {current_player} goes again.")

        elif event.widget.cget("bg") == "black":
            message_label.config(text = "INVALID PLACEMENT")

        p1_text = p1_label["text"].split(":")
        p2_text = p2_label["text"].split(":")

        p1_label.config(text = f"{p1_text[0]}: {p_score[P1_NAME]}")
        p2_label.config(text = f"{p2_text[0]}: {p_score[P2_NAME]}")

        if p_count[current_player] == 0:
            if p_score[P1_NAME] > p_score[P2_NAME]:
                message_label.config(text = f"Game Over! {P1_NAME} Wins!")
            elif p_score[P2_NAME] > p_score[P1_NAME]:
                message_label.config(text = f"Game Over! {P2_NAME} Wins!")
            else:
                message_label.config(text = "Game Tied!")

    else:
        message_label.config(text = f"{current_player}, please select a piece to play.")

def record_piece(): 
   
    global game_board_state
    global p_count

    coords = last_piece_played["space"].split(',')

    game_board_state[int(coords[0])][int(coords[1])] = last_piece_selected["player"]
    p_count[current_player] -= 1

def check_score():

    global p_score

    sp_x, sp_y = [int(s) for s in (last_piece_played["space"].split(','))]
    

    # check for line with piece as start/end of line horizontal
    if sp_y <= 1:
        if check_connected([sp_x, sp_y], [sp_x, sp_y + 1], [sp_x, sp_y + 2]):
            p_score[last_piece_played["player"]] += 1
    if sp_y >= 2:
        if check_connected([sp_x, sp_y], [sp_x, sp_y - 1], [sp_x, sp_y - 2]):
            p_score[last_piece_played["player"]] += 1

    # check for line with piece as middle of line horizontal
    if sp_y == 1 or sp_y == 2:
        if check_connected([sp_x, sp_y - 1], [sp_x, sp_y], [sp_x, sp_y + 1]):
            p_score[last_piece_played["player"]] += 1

    # check for line with piece as start/end of line vertical
    if sp_x <= 1:
        if check_connected([sp_x, sp_y], [sp_x + 1, sp_y], [sp_x + 2, sp_y]):
            p_score[last_piece_played["player"]] += 1
    if sp_x >= 2:
        if check_connected([sp_x, sp_y], [sp_x - 1, sp_y], [sp_x - 2, sp_y]):
            p_score[last_piece_played["player"]] += 1

    # check for line with piece as middle of line vertical
    if sp_x == 1 or sp_x == 2:
        if check_connected([sp_x - 1, sp_y], [sp_x, sp_y], [sp_x + 1, sp_y]):
            p_score[last_piece_played["player"]] += 1

    # check for line with piece as start/end of line diagonal
    if sp_x <= 1 and sp_y <= 1:
        if check_connected([sp_x, sp_y], [sp_x + 1, sp_y + 1], [sp_x + 2, sp_y + 2]):
            p_score[last_piece_played["player"]] += 1    
    if sp_x <= 1 and sp_y >= 2:
        if check_connected([sp_x, sp_y], [sp_x + 1, sp_y - 1], [sp_x + 2, sp_y - 2]):
            p_score[last_piece_played["player"]] += 1    
    if sp_x >= 2 and sp_y >= 2:
        if check_connected([sp_x, sp_y], [sp_x - 1, sp_y - 1], [sp_x - 2, sp_y - 2]):
            p_score[last_piece_played["player"]] += 1    
    if sp_x >= 2 and sp_y <= 1:
        if check_connected([sp_x, sp_y], [sp_x - 1, sp_y + 1], [sp_x - 2, sp_y + 2]):
            p_score[last_piece_played["player"]] += 1

    # check for line with piece as middle of line diagonal
    if sp_x == 1 or sp_x == 2:
        if (check_connected([sp_x - 1, sp_y - 1], [sp_x, sp_y], [sp_x + 1, sp_y + 1])) or (check_connected([sp_x + 1, sp_y - 1], [sp_x, sp_y], [sp_x - 1, sp_y + 1])):
            print("Scored: 11")
            p_score[last_piece_played["player"]] += 1

def check_connected(space1, space2, space3):
    if ((space1[0] < 0 or space1[0] > 3) or (space1[1] < 0 or space1[1] > 3) or 
        (space2[0] < 0 or space2[0] > 3) or (space2[1] < 0 or space2[1] > 3) or
        (space3[0] < 0 or space3[0] > 3) or (space3[1] < 0 or space3[1] > 3)):
        return False

    if (game_board_state[space1[0]][space1[1]] == last_piece_played["player"] and 
        game_board_state[space2[0]][space2[1]] == last_piece_played["player"] and
        game_board_state[space3[0]][space3[1]] == last_piece_played["player"]
    ):
        return True
    else:
        return False

def check_valid_place(sp_x, sp_y):

    lp_x, lp_y = [int(s) for s in (last_piece_played["space"].split(','))]
    if "xcross" in last_piece_played["key"]:        

        pos_xy = []
        for i in range(1, 4):
            if ((lp_x - i) >= 0) or ((lp_x + i) <= 3) or ((lp_y - i) >= 0) or ((lp_y + i) <= 3):
                pos_xy.append(f"{lp_x + i}, {lp_y + i}")
                pos_xy.append(f"{lp_x + i}, {lp_y - i}")
                pos_xy.append(f"{lp_x - i}, {lp_y + i}")
                pos_xy.append(f"{lp_x - i}, {lp_y - i}")

        if str(f"{sp_x}, {sp_y}") in pos_xy:
            return True
        else:
            return False

    if "cross" in last_piece_played["key"]:
        if (lp_x == sp_x) or (lp_y == sp_y):
            return True
        else:
            return False
        
    if "xcircle" in last_piece_played["key"]:
        if (((sp_x < lp_x -1) or (sp_x > lp_x + 1)) or ((sp_y < lp_y - 1) or (sp_y > lp_y + 1))):
            return True
        else:
            return False
        
    if "circle" in last_piece_played["key"]:
        if (((sp_x == lp_x) or (sp_x == lp_x - 1) or (sp_x == lp_x + 1)) and 
            ((sp_y == lp_y) or (sp_y == lp_y + 1) or (sp_y == lp_y - 1))):

            return True
        else:
            return False
        
def check_valid_any():

    for x in range(4):
        for y in range(4):
            if check_valid_place(x, y):
                if (P1_NAME not in game_board_state[x][y] and P2_NAME not in game_board_state[x][y]):
                    return True

    return False


def show_piece(key, canvas):
    if "xcross" in key:
        for shape in draw_shapes("xcross"):
            canvas.create_polygon(shape)
    elif "cross" in key:
        for shape in draw_shapes("cross"):
            canvas.create_polygon(shape)
    elif "xcircle" in key:
        for shape in draw_shapes("xcircle"):
            if len(shape) == 5:
                canvas.create_oval(shape[:4], fill = shape[4], width = 3)
            else:
                canvas.create_arc(shape[:4], extent = shape[4], start=shape[5], style=ARC, width = 3)
    elif "circle" in key:
        for shape in draw_shapes("circle"):
            if len(shape) == 5:
                canvas.create_oval(shape[:4], fill = "black", width = 3)
            else:
                canvas.create_oval(shape, width = 3)

def draw_shapes(shape):

    if shape == "cross":
        points = [
            [int(P_WIDTH / 2), 1, int(P_WIDTH / 1.66), int(P_WIDTH / 3.125), int(P_WIDTH / 2), int(P_WIDTH / 2.38), int(P_WIDTH / 2.5), int(P_WIDTH / 3.125)],
            [int(P_WIDTH / 1.47),  int(P_WIDTH / 2.5), int(P_WIDTH / 1.02), int(P_WIDTH / 2), int(P_WIDTH / 1.47), int(P_WIDTH / 1.66), int(P_WIDTH / 1.72), int(P_WIDTH / 2)],
            [int(P_WIDTH / 2),  int(P_WIDTH / 1.72), int(P_WIDTH / 1.66), int(P_WIDTH / 1.47), int(P_WIDTH / 2), int(P_WIDTH / 1.02), int(P_WIDTH / 2.5), int(P_WIDTH / 1.47)],
            [int(P_WIDTH / 3.125),  int(P_WIDTH / 2.5), int(P_WIDTH / 2.38), int(P_WIDTH / 2), int(P_WIDTH / 3.125), int(P_WIDTH / 1.66), int(P_WIDTH / P_WIDTH), int(P_WIDTH / 2.0)],
            ]
    elif shape == "xcross":
        points = [
            [int(P_WIDTH / 6.25),  int(P_WIDTH / 6.25), int(P_WIDTH / 2.27), int(P_WIDTH / 3.33), int(P_WIDTH / 2.27), int(P_WIDTH / 2.27), int(P_WIDTH / 3.33), int(P_WIDTH / 2.27)],
            [int(P_WIDTH / 1.78),  int(P_WIDTH / 3.33), int(P_WIDTH / 1.19), int(P_WIDTH / 6.25), int(P_WIDTH / 1.42), int(P_WIDTH / 2.27), int(P_WIDTH / 1.78), int(P_WIDTH / 2.27)],
            [int(P_WIDTH / 1.78),  int(P_WIDTH / 1.78), int(P_WIDTH / 1.42), int(P_WIDTH / 1.78), int(P_WIDTH / 1.19), int(P_WIDTH / 1.19), int(P_WIDTH / 1.78), int(P_WIDTH / 1.43)],
            [int(P_WIDTH / 3.33),  int(P_WIDTH / 1.78), int(P_WIDTH / 2.27), int(P_WIDTH / 1.78), int(P_WIDTH / 2.27), int(P_WIDTH / 1.42), int(P_WIDTH / 6.25), int(P_WIDTH / 1.19)],
            ]
    elif shape == 'circle':
        points = [
            [int(P_WIDTH / 4.16),  int(P_WIDTH / 4.16), int(P_WIDTH / 1.31), int(P_WIDTH / 1.31)],
            [int(P_WIDTH / 2.38),  int(P_WIDTH / 2.38), int(P_WIDTH / 1.72), int(P_WIDTH / 1.72), "black"]
            ]
    elif shape == 'xcircle':
        points = [
            [int(P_WIDTH / 10.0),  int(P_WIDTH / 10.0), int(P_WIDTH / 1.11), int(P_WIDTH / 1.11), 80, 5],
            [int(P_WIDTH / 10.0),  int(P_WIDTH / 10.0), int(P_WIDTH / 1.11), int(P_WIDTH / 1.11), 80, 95],
            [int(P_WIDTH / 10.0),  int(P_WIDTH / 10.0), int(P_WIDTH / 1.11), int(P_WIDTH / 1.11), 80, 185],
            [int(P_WIDTH / 10.0),  int(P_WIDTH / 10.0), int(P_WIDTH / 1.11), int(P_WIDTH / 1.11), 80, 275],
            [int(P_WIDTH / 2.5),  int(P_WIDTH / 2.5), int(P_WIDTH / 1.66), int(P_WIDTH / 1.66), "black"]
            ]

    return points

def player_board(player, p_x, p_y, start, color, message_label):
    # Player 1 Pieces
    player_name = Label(ROOT, text = f"{player}'s pieces")
    player_score = Label(ROOT, text = f"{player}'s score: {p_score[player]}")

    p_canvas = Canvas(ROOT, width = (start * 2) + (INTERVAL * 2), height  = (start * 2) + (INTERVAL * 4), bg="gray")
    p_canvas.place(x = p_x, y = p_y)
    player_name.place(x = p_x, y = p_y - 50)
    player_score.place(x = p_x, y = p_y -25)
    

    p_canvas.create_rectangle(start, start, start + (INTERVAL * 2), start + (INTERVAL * 4), width = 3)
    p_canvas.create_line(start + INTERVAL, start, start + INTERVAL, start + (INTERVAL * 4), width = 3)
    p_canvas.create_line(start, start + INTERVAL, start + (INTERVAL * 2), start + INTERVAL, width = 3)
    p_canvas.create_line(start, start + (INTERVAL * 2), start + (INTERVAL * 2), start + (INTERVAL * 2), width = 3)
    p_canvas.create_line(start, start + (INTERVAL * 3), start + (INTERVAL * 2), start + (INTERVAL * 3), width = 3)

    p_pieces = {
        "cross_1" : Canvas(p_canvas, width = P_WIDTH, height = P_WIDTH, bg=color),
        "cross_2" : Canvas(p_canvas, width = P_WIDTH, height = P_WIDTH, bg=color),
        "xcross_1" : Canvas(p_canvas, width = P_WIDTH, height = P_WIDTH, bg=color),
        "xcross_2" : Canvas(p_canvas, width = P_WIDTH, height = P_WIDTH, bg=color),
        "circle_1" : Canvas(p_canvas, width = P_WIDTH, height = P_WIDTH, bg=color),
        "circle_2" : Canvas(p_canvas, width = P_WIDTH, height = P_WIDTH, bg=color),
        "xcircle_1" : Canvas(p_canvas, width = P_WIDTH, height = P_WIDTH, bg=color),
        "xcircle_2" : Canvas(p_canvas, width = P_WIDTH, height = P_WIDTH, bg=color),
    }

    p_start_x = start + 2
    p_start_y = start + 2
    p_board_x = 0
    p_board_y = 0


    for key in p_pieces:
        p_pieces[key].place(x = p_start_x, y = p_start_y)
        p_pieces[key].place(x = p_start_x + p_board_x, y = p_start_y + p_board_y, width = P_WIDTH, height = P_WIDTH)
        p_pieces[key].bind("<Enter>", on_enter)
        p_pieces[key].bind("<Leave>", partial(on_leave, player))
        p_pieces[key].bind("<Button-1>", partial(on_click_player, key, player, color, p_pieces[key], message_label))

        show_piece(key, p_pieces[key])

        p_board_x += INTERVAL
        if p_board_x > 1 * INTERVAL:
            p_board_y += INTERVAL
            p_board_x = 0

    return player_score

def new_game():
    for widget in ROOT.winfo_children():
        widget.destroy()
    init_game_state()
    ui()

def init_game_state():

    global last_piece_selected
    global last_piece_played
    global game_board_state
    global p_score
    global p_count
    global current_player

    last_piece_selected = {
        "key": '',
        "color": 'gray',
        "player": '',
        "piece": '',
        "placed": False
    }

    # Track last piece played
    last_piece_played = {
        "key": '',
        "player": '',
        "space": [],
    }

    # Track game board state
    game_board_state = [
        ["0x0", "1x0", "2x0", "3x0"],
        ["0x1", "1x1", "2x1", "3x1"],
        ["0x2", "1x2", "2x2", "2x3"],
        ["0x3", "1x3", "2x3", "3x3"],
    ]

    # Track player score
    p_score = {
        P1_NAME: 0,
        P2_NAME: 0,
    }

    p_count = {
        P1_NAME: 8,
        P2_NAME: 8
    }

    current_player = P1_NAME


def ui():

    start = 20
    end = start + 2 + (INTERVAL * 4)

    window_x = (start * 4) + ((P_WIDTH * 5) + 2) + ((INTERVAL * 2) + (start * 2)) * 2   
    window_y = 9 * P_WIDTH

    ROOT.title("Pylieff")
    ROOT.geometry(f"{window_x}x{window_y}")

    menubar = Menu(ROOT)
    ROOT.config(menu = menubar)

    game_menu = Menu(menubar, tearoff = 0)
    config_menu = Menu(menubar, tearoff = 0)
    menubar.add_cascade(label="Game", menu=game_menu)
    menubar.add_cascade(label="Config", menu=config_menu)

    game_menu.add_command(label = "New Game", command = new_game)

    message_label = Label(ROOT, text='')
    message_label.place(x = start, y = 400)

    # Create player pieces

    p1_label = player_board(P1_NAME, P_WIDTH * .4, 100, start, P1_COLOR, message_label)
    p2_label = player_board(P2_NAME, (start * 3) + ((P_WIDTH * 5) + 2) + ((INTERVAL * 2) + (start * 2)), 100, start, P2_COLOR, message_label)

    current_label = Label(ROOT, text = f"Current Player: {current_player}")
    current_label.place(x = start + INTERVAL, y = start)

    # Create Game Board
    game_board = Canvas(ROOT, width = (start * 2) + (INTERVAL * 4), height = (start * 2) + (INTERVAL * 4), bg="gray")
    game_board.place(x = ((start * 4) + (INTERVAL * 2)), y = 100)
    
    game_board.create_rectangle(start, start, start + (INTERVAL * 4), start + (INTERVAL * 4), width = 3)
    

    next_x = start +  INTERVAL
    next_y = start + INTERVAL

    for i in range(4):
        game_board.create_line(next_x, start, next_x, end, width=3)
        game_board.create_line(start, next_y, end, next_y, width=3)

        next_x += INTERVAL
        next_y += INTERVAL

    spaces = []

    for r in range(4):
        for c in range(4):
            spaces.append(Canvas(ROOT, width = P_WIDTH, height = P_WIDTH, bg=B_COLOR, name = f"{str(r)},{str(c)}"))

    start_x = ((start * 4) + (INTERVAL * 2)) + start + 2
    start_y = 102 + start
    board_x = 0
    board_y = 0

    for space in spaces:
        space.place(x = start_x + board_x, y = start_y + board_y, width = P_WIDTH, height = P_WIDTH)
        space.bind("<Enter>", on_enter)
        space.bind("<Leave>", partial(on_leave, "Game Board"))
        space.bind("<Button-1>", partial(on_click_board, message_label, current_label, p1_label, p2_label))
        board_x += INTERVAL
        if board_x > 3 * INTERVAL:
            board_y += INTERVAL
            board_x = 0

    ROOT.mainloop()