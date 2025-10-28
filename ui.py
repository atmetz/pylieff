from tkinter import *
from functools import partial

from config import P1_COLOR, P2_COLOR, B_COLOR, P_WIDTH, INTERVAL, ROOT

last_piece = {
    "key": '',
    "color": '',
    "player": '',
    "placed": False
}

def on_enter(event):
    event.widget.config(bg="blue")

def on_leave(board, event):
    if board == "Player 1":
        event.widget.config(bg=P1_COLOR)
    elif board == "Player 2":
        event.widget.config(bg=P2_COLOR)
    else:
        event.widget.config(bg=B_COLOR)

def on_click_player(key, player, color, event):

    global last_piece

    win_width = ROOT.winfo_width()

    sp_x = (win_width - P_WIDTH) / 2

    sp_label = Label(ROOT, text = f" {player}'s Selected Piece")
    #spl_x = (win_width - sp_label.winfo_width()) / 2
    sp_label.place(x = sp_x, y = 5)

    sp_canvas = Canvas(ROOT, width = P_WIDTH, height  = P_WIDTH, bg=color)
    sp_canvas.place(x = sp_x, y = 25)

    event.widget.place_forget()

    sp_canvas.create_rectangle(1, 1, P_WIDTH, P_WIDTH, width = 1)

    show_piece(key, sp_canvas)

    last_piece["key"] = key
    last_piece["color"] = color
    last_piece["player"] = player
    last_piece["placed"] = False

def on_click_board(event):

    w_x = event.widget.winfo_x()
    w_y = event.widget.winfo_y()

    if not last_piece["placed"]:

        last_piece["placed"] = True

        pp_canvas = Canvas(ROOT, width = P_WIDTH, height  = P_WIDTH, bg=last_piece["color"])
        pp_canvas.place(x = w_x, y = w_y)

        event.widget.place_forget()

        show_piece(last_piece["key"], pp_canvas)

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

def player_board(player, p_x, p_y, start, color):
    # Player 1 Pieces

    player_name = Label(ROOT, text = f"{player}'s pieces")
    p_canvas = Canvas(ROOT, width = (start * 2) + (INTERVAL * 2), height  = (start * 2) + (INTERVAL * 4), bg="white")
    p_canvas.place(x = p_x, y = p_y)
    player_name.place(x = p_x, y = p_y - 50)
    

    p_canvas.create_rectangle(start, start, start + (INTERVAL * 2), start + (INTERVAL * 4), width = 3)
    p_canvas.create_line(start + INTERVAL, start, start + INTERVAL, start + (INTERVAL * 4), width = 3)
    p_canvas.create_line(start, start + INTERVAL, start + (INTERVAL * 2), start + INTERVAL, width = 3)
    p_canvas.create_line(start, start + (INTERVAL * 2), start + (INTERVAL * 2), start + (INTERVAL * 2), width = 3)
    p_canvas.create_line(start, start + (INTERVAL * 3), start + (INTERVAL * 2), start + (INTERVAL * 3), width = 3)

    p_pieces = {
        "cross_1" : Canvas(ROOT, width = P_WIDTH, height = P_WIDTH, bg=color),
        "cross_2" : Canvas(ROOT, width = P_WIDTH, height = P_WIDTH, bg=color),
        "xcross_1" : Canvas(ROOT, width = P_WIDTH, height = P_WIDTH, bg=color),
        "xcross_2" : Canvas(ROOT, width = P_WIDTH, height = P_WIDTH, bg=color),
        "circle_1" : Canvas(ROOT, width = P_WIDTH, height = P_WIDTH, bg=color),
        "circle_2" : Canvas(ROOT, width = P_WIDTH, height = P_WIDTH, bg=color),
        "xcircle_1" : Canvas(ROOT, width = P_WIDTH, height = P_WIDTH, bg=color),
        "xcircle_2" : Canvas(ROOT, width = P_WIDTH, height = P_WIDTH, bg=color),
    }

    p_start_x = p_x + start + 2
    p_start_y = p_y + start + 2
    p_board_x = 0
    p_board_y = 0


    for key in p_pieces:
        p_pieces[key].place(x = p_start_x, y = p_start_y)
        p_pieces[key].place(x = p_start_x + p_board_x, y = p_start_y + p_board_y, width = P_WIDTH, height = P_WIDTH)
        p_pieces[key].bind("<Enter>", on_enter)
        p_pieces[key].bind("<Leave>", partial(on_leave, player))
        p_pieces[key].bind("<Button-1>", partial(on_click_player, key, player, color))

        show_piece(key, p_pieces[key])

        p_board_x += INTERVAL
        if p_board_x > 1 * INTERVAL:
            p_board_y += INTERVAL
            p_board_x = 0


def ui():

    start = 20
    end = start + 2 + (INTERVAL * 4)

    window_x = (start * 4) + ((P_WIDTH * 5) + 2) + ((INTERVAL * 2) + (start * 2)) * 2   
    window_y = 9 * P_WIDTH

    ROOT.title("Pylieff")
    ROOT.geometry(f"{window_x}x{window_y}")

    # Create player pieces

    player_board("Player 1", P_WIDTH * .4, 100, start, P1_COLOR)
    player_board("Player 2", (start * 3) + ((P_WIDTH * 5) + 2) + ((INTERVAL * 2) + (start * 2)), 100, start, P2_COLOR)


    # Create Game Board
    game_board = Canvas(ROOT, width = (start * 2) + (INTERVAL * 4), height = (start * 2) + (INTERVAL * 4), bg="white")
    game_board.place(x = ((start * 4) + (INTERVAL * 2)), y = 100)
    
    game_board.create_rectangle(start, start, start + (INTERVAL * 4), start + (INTERVAL * 4), width = 3)
    

    next_x = start +  INTERVAL
    next_y = start + INTERVAL

    for i in range(4):
        game_board.create_line(next_x, start, next_x, end, width=3)
        game_board.create_line(start, next_y, end, next_y, width=3)

        next_x += INTERVAL
        next_y += INTERVAL

    space = []

    for i in range(16):
        space.append(Canvas(ROOT, width = P_WIDTH, height = P_WIDTH, bg=B_COLOR))

    start_x = ((start * 4) + (INTERVAL * 2)) + start + 2
    start_y = 102 + start
    board_x = 0
    board_y = 0

    for i in range(16):
        space[i].place(x = start_x + board_x, y = start_y + board_y, width = P_WIDTH, height = P_WIDTH)
        space[i].bind("<Enter>", on_enter)
        space[i].bind("<Leave>", partial(on_leave, "Game Board"))
        space[i].bind("<Button-1>", partial(on_click_board))
        board_x += INTERVAL
        if board_x > 3 * INTERVAL:
            board_y += INTERVAL
            board_x = 0

    ROOT.mainloop()