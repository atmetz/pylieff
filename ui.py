from tkinter import *
from functools import partial

def on_button_click(button, root):
    x_coord = button.winfo_x()
    y_coord = button.winfo_y()
    width = button.winfo_width()
    height = button.winfo_height()
    button.place_forget()

    label_text = Label(root, bg="blue")
    label_text.place(x = x_coord, y = y_coord, width = width, height = height)

def ui():
    root = Tk()

    root.title("Pylieff")
    root.geometry("800x600")

    canvas = Canvas(root, width=300, height=300, bg="white")
    canvas.place(x=250, y=100)

    start = 47
    end = 261
    interval = 53

    next_x = start
    next_y = start
    canvas.create_line(start-1, start, start, start, width=3)

    for i in range(5):
        canvas.create_line(next_x, start, next_x, end, width=3)
        canvas.create_line(start, next_y, end, next_y, width=3)

        next_x += interval
        next_y += interval

    button = []

    for i in range(16):
        button.append(Button(root, activebackground="blue", activeforeground="white"))
        
    start_x = 299
    start_y = 149
    board_x = 0
    board_y = 0
    b_width = 50
    b_height = 50

    for i in range(16):
        button[i].place(x = start_x + board_x, y = start_y + board_y, width = b_width, height = b_height)
        button[i].config(command=partial(on_button_click, button[i], root))
        board_x += interval
        if board_x > 3 * interval:
            board_y += interval
            board_x = 0

    root.mainloop()