from tkinter import *
from functools import partial

def on_enter(event):
    event.widget.config(bg="blue")

def on_leave(event):
    event.widget.config(bg="gray")

def on_click(event):
    text = event.widget.cget("bg")
    print(event.x)
    if text != "gray":
        print("I dunno")
    else:
        print("Already claimed")

def draw_shapes(shape):

    if shape == "cross":
        points = [
            [24, 0, 29, 15, 24, 20, 19, 15],
            [33, 19, 48, 24, 33, 29, 28, 24],
            [24, 28, 29, 33, 24, 48, 19, 33],
            [15, 19, 20, 24, 15, 29, 0, 24],
            ]
    elif shape == "xcross":
        points = [
            [7, 7, 21, 14, 21, 21, 14, 21],
            [27, 14, 41, 7, 34, 21, 27, 21],
            [27, 27, 34, 27, 41, 41, 27, 34],
            [14, 27, 21, 27, 21, 34, 7, 41],
            ]
    elif shape == 'circle':
        points = [
            [8, 8, 42, 42],
            [20, 20, 30, 30, "black"]
            ]
    elif shape == 'xcircle':
        points = [
            [8, 8, 42, 42, 80, 5],
            [8, 8, 42, 42, 80, 95],
            [8, 8, 42, 42, 80, 185],
            [8, 8, 42, 42, 80, 275],
            [20, 20, 30, 30, "black"]
            ]

    return points

def player_board(player, x, y, start, interval, b_width, root, color):
    # Player 1 Pieces

    player_name = Label(root, text = f"{player}'s pieces")
    p_x = x
    p_y = y
    p_canvas = Canvas(root, width = 100 + (interval * 2), height  = 100 + (interval * 4), bg="white")
    p_canvas.place(x = p_x, y = p_y)
    player_name.place(x = p_x, y = p_y - 50)
    
    p_canvas.bind("<Button-1>", on_click)
    

    p_canvas.create_rectangle(start, start, start + (interval * 2), start + (interval * 4), width = 3)
    p_canvas.create_line(start + interval, start, start + interval, start + (interval * 4), width = 3)
    p_canvas.create_line(start, start + interval, start + (interval * 2), start + interval, width = 3)
    p_canvas.create_line(start, start + (interval * 2), start + (interval * 2), start + (interval * 2), width = 3)
    p_canvas.create_line(start, start + (interval * 3), start + (interval * 2), start + (interval * 3), width = 3)

    p_pieces = {
        "cross_1" : Canvas(root, width = b_width, height = b_width, bg=color),
        "cross_2" : Canvas(root, width = b_width, height = b_width, bg=color),
        "xcross_1" : Canvas(root, width = b_width, height = b_width, bg=color),
        "xcross_2" : Canvas(root, width = b_width, height = b_width, bg=color),
        "circle_1" : Canvas(root, width = b_width, height = b_width, bg=color),
        "circle_2" : Canvas(root, width = b_width, height = b_width, bg=color),
        "xcircle_1" : Canvas(root, width = b_width, height = b_width, bg=color),
        "xcircle_2" : Canvas(root, width = b_width, height = b_width, bg=color),
    }

    p_start_x = p_x + 49
    p_start_y = p_y + 49
    p_board_x = 0
    p_board_y = 0


    for key in p_pieces:
        p_pieces[key].place(x = p_start_x, y = p_start_y)
        p_pieces[key].place(x = p_start_x + p_board_x, y = p_start_y + p_board_y, width = b_width, height = b_width)
        p_pieces[key].bind("<Enter>", on_enter)
        p_pieces[key].bind("<Leave>", on_leave)
        p_pieces[key].bind("<Button-1>", on_click)

        if "xcross" in key:
            for shape in draw_shapes("xcross"):
                p_pieces[key].create_polygon(shape)
        elif "cross" in key:
            for shape in draw_shapes("cross"):
                p_pieces[key].create_polygon(shape)
        elif "xcircle" in key:
            for shape in draw_shapes("xcircle"):
                if len(shape) == 5:
                    p_pieces[key].create_oval(shape[:4], fill = shape[4], width = 3)
                else:
                    p_pieces[key].create_arc(shape[:4], extent = shape[4], start=shape[5], style=ARC, width = 3)
        elif "circle" in key:
            for shape in draw_shapes("circle"):
                if len(shape) == 5:
                    p_pieces[key].create_oval(shape[:4], fill = "black", width = 3)
                else:
                    p_pieces[key].create_oval(shape, width = 3)

        p_board_x += interval
        if p_board_x > 1 * interval:
            p_board_y += interval
            p_board_x = 0


def ui():
    root = Tk()

    root.title("Pylieff")
    root.geometry("800x600")
        
    b_width = 50
    interval = b_width + 3
    start = 47
    end = start + 2 + (interval * 4)

    player_board("Player 1", 20, 100, start, interval, b_width, root, "gray")
    player_board("Player 2", 582, 100, start, interval, b_width, root, "red")


    # Create Game Board
    canvas = Canvas(root, width = 100 + (interval * 4), height = 100 + (interval * 4), bg="white")
    canvas.place(x = 250, y = 100)
    
    canvas.bind("<Button-1>", on_click)

    next_x = start
    next_y = start
    canvas.create_line(start-1, start, start, start, width=3)

    for i in range(5):
        canvas.create_line(next_x, start, next_x, end, width=3)
        canvas.create_line(start, next_y, end, next_y, width=3)

        next_x += interval
        next_y += interval

    space = []

    for i in range(16):
        space.append(Canvas(root, width = b_width, height = b_width, bg="gray"))
        
    start_x = 299
    start_y = 149
    board_x = 0
    board_y = 0

    for i in range(16):
        space[i].place(x = start_x + board_x, y = start_y + board_y, width = b_width, height = b_width)
        space[i].bind("<Enter>", on_enter)
        space[i].bind("<Leave>", on_leave)
        space[i].bind("<Button-1>", on_click)
        board_x += interval
        if board_x > 3 * interval:
            board_y += interval
            board_x = 0

    root.mainloop()