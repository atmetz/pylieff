from tkinter import *
from functools import partial

from config import P1_COLOR, P1_NAME, P2_COLOR, P2_NAME, B_COLOR, P_WIDTH, INTERVAL, ROOT

class Board:
    def __init__(self, player, b_x, b_y, start, message_label):
        self.player = player
        self.b_x = b_x
        self.b_y = b_y
        self.start = start
        self.message_label = message_label

    def create_board(self):
        raise NotImplementedError("create_board method not implemented")
    
    def on_click(self):
        raise NotImplementedError("on_click method not implemented")
    
    def show_piece(self, key, canvas):
        if "xcross" in key:
            for shape in self.draw_shapes("xcross"):
                canvas.create_polygon(shape)
        elif "cross" in key:
            for shape in self.draw_shapes("cross"):
                canvas.create_polygon(shape)
        elif "xcircle" in key:
            for shape in self.draw_shapes("xcircle"):
                if len(shape) == 5:
                    canvas.create_oval(shape[:4], fill = shape[4], width = 3)
                else:
                    canvas.create_arc(shape[:4], extent = shape[4], start=shape[5], style=ARC, width = 3)
        elif "circle" in key:
            for shape in self.draw_shapes("circle"):
                if len(shape) == 5:
                    canvas.create_oval(shape[:4], fill = "black", width = 3)
                else:
                    canvas.create_oval(shape, width = 3)

    def draw_shapes(self, shape):

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
    
class PlayerBoard(Board):
        
    def __init__(self, player, b_x, b_y, start, message_label):
        super().__init__(player, b_x, b_y, start, message_label)

    def create_board(self):
        # Player Pieces
        player_name = Label(ROOT, text = f"{self.player.name}'s pieces")
        player_score = Label(ROOT, text = f"{self.player.name}'s score: {self.player.score}")

        p_canvas = Canvas(ROOT, width = (self.start * 2) + (INTERVAL * 2), height  = (self.start * 2) + (INTERVAL * 4), bg="gray")
        p_canvas.place(x = self.b_x, y = self.b_y)
        player_name.place(x = self.b_x, y = self.b_y - 50)
        player_score.place(x = self.b_x, y = self.b_y -25)
        

        p_canvas.create_rectangle(self.start, self.start, self.start + (INTERVAL * 2), self.start + (INTERVAL * 4), width = 3)
        p_canvas.create_line(self.start + INTERVAL, self.start, self.start + INTERVAL, self.start + (INTERVAL * 4), width = 3)
        p_canvas.create_line(self.start, self.start + INTERVAL, self.start + (INTERVAL * 2), self.start + INTERVAL, width = 3)
        p_canvas.create_line(self.start, self.start + (INTERVAL * 2), self.start + (INTERVAL * 2), self.start + (INTERVAL * 2), width = 3)
        p_canvas.create_line(self.start, self.start + (INTERVAL * 3), self.start + (INTERVAL * 2), self.start + (INTERVAL * 3), width = 3)

        p_pieces = {
            "cross_1" : Canvas(p_canvas, width = P_WIDTH, height = P_WIDTH, bg=self.player.color),
            "cross_2" : Canvas(p_canvas, width = P_WIDTH, height = P_WIDTH, bg=self.player.color),
            "xcross_1" : Canvas(p_canvas, width = P_WIDTH, height = P_WIDTH, bg=self.player.color),
            "xcross_2" : Canvas(p_canvas, width = P_WIDTH, height = P_WIDTH, bg=self.player.color),
            "circle_1" : Canvas(p_canvas, width = P_WIDTH, height = P_WIDTH, bg=self.player.color),
            "circle_2" : Canvas(p_canvas, width = P_WIDTH, height = P_WIDTH, bg=self.player.color),
            "xcircle_1" : Canvas(p_canvas, width = P_WIDTH, height = P_WIDTH, bg=self.player.color),
            "xcircle_2" : Canvas(p_canvas, width = P_WIDTH, height = P_WIDTH, bg=self.player.color),
        }

        p_start_x = self.start + 2
        p_start_y = self.start + 2
        p_board_x = 0
        p_board_y = 0


        for key in p_pieces:
            p_pieces[key].place(x = p_start_x, y = p_start_y)
            p_pieces[key].place(x = p_start_x + p_board_x, y = p_start_y + p_board_y, width = P_WIDTH, height = P_WIDTH)
            p_pieces[key].bind("<Enter>", on_enter)
            p_pieces[key].bind("<Leave>", partial(on_leave, self.player.name))
            p_pieces[key].bind("<Button-1>", partial(self.on_click, key, self.player, p_pieces[key], self.message_label))

            self.show_piece(key, p_pieces[key])

            p_board_x += INTERVAL
            if p_board_x > 1 * INTERVAL:
                p_board_y += INTERVAL
                p_board_x = 0

        return player_score
    
    def on_click(self, key, player, piece, message_label, event):

        global last_piece_selected

        win_width = ROOT.winfo_width()
        
        if player.current:

            if last_piece_selected["piece"]:
                self.show_piece(last_piece_selected["key"], last_piece_selected["piece"])

            sp_x = (win_width - P_WIDTH) / 2

            sp_label = Label(ROOT, text = f" {player.name}'s Selected Piece")
            sp_label.place(x = sp_x, y = 5)

            sp_canvas = Canvas(ROOT, width = P_WIDTH, height  = P_WIDTH, bg=player.color)
            sp_canvas.place(x = sp_x, y = 25)

            event.widget.delete("all")

            sp_canvas.create_rectangle(0, 0, P_WIDTH, P_WIDTH, width = 3)

            self.show_piece(key, sp_canvas)

            last_piece_selected["key"] = key
            last_piece_selected["color"] = player.color
            last_piece_selected["player"] = player.name
            last_piece_selected["piece"] = piece
            last_piece_selected["placed"] = False

        else:
            message_label.config(text = f"It is the other player's turn.")
    
class GameBoard(Board):
        
    def __init__(self, b_x, b_y, start, message_label):
        self.game_board_state = [
            ["0x0", "1x0", "2x0", "3x0"],
            ["0x1", "1x1", "2x1", "3x1"],
            ["0x2", "1x2", "2x2", "2x3"],
            ["0x3", "1x3", "2x3", "3x3"],
        ]
        super().__init__(None, b_x, b_y, start, message_label)

    
    def create_board(self, current_label, p1_label, p2_label, player1, player2):
        # Create Game Board
        end = self.start + 2 + (INTERVAL * 4)

        game_board = Canvas(ROOT, width = (self.start * 2) + (INTERVAL * 4), height = (self.start * 2) + (INTERVAL * 4), bg="gray")
        game_board.place(x = self.b_x, y = self.b_y)
        
        game_board.create_rectangle(self.start, self.start, self.start + (INTERVAL * 4), self.start + (INTERVAL * 4), width = 3)
        

        next_x = self.start +  INTERVAL
        next_y = self.start + INTERVAL

        for i in range(4):
            game_board.create_line(next_x, self.start, next_x, end, width=3)
            game_board.create_line(self.start, next_y, end, next_y, width=3)

            next_x += INTERVAL
            next_y += INTERVAL

        spaces = []

        for r in range(4):
            for c in range(4):
                spaces.append(Canvas(ROOT, width = P_WIDTH, height = P_WIDTH, bg=B_COLOR, name = f"{str(r)},{str(c)}"))

        start_x = self.b_x + 22
        start_y = self.b_y + 22
        board_x = 0
        board_y = 0

        for space in spaces:
            space.place(x = start_x + board_x, y = start_y + board_y, width = P_WIDTH, height = P_WIDTH)
            space.bind("<Enter>", on_enter)
            space.bind("<Leave>", partial(on_leave, "Game Board"))
            space.bind("<Button-1>", partial(self.on_click, self.message_label, current_label, p1_label, p2_label, player1, player2))
            board_x += INTERVAL
            if board_x > 3 * INTERVAL:
                board_y += INTERVAL
                board_x = 0

    def on_click(self, message_label, current_label, p1_label, p2_label, player1, player2, event):

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

                    self.show_piece(last_piece_selected["key"], pp_canvas)

                    last_piece_played["key"] = last_piece_selected["key"]
                    last_piece_played["player"] = last_piece_selected["player"]
                    last_piece_played["space"] = str(event.widget).split(".")[-1]

                    last_piece_selected["piece"] = ''
                    
                    if player1.current:
                        self.record_piece(player1)
                        check_score(player1, self.game_board_state)
                    else:
                        self.record_piece(player2)
                        check_score(player2, self.game_board_state)

                    if player1.current and check_valid_any():
                        player1.current = False
                        player2.current = True
                        current_label.config(text = f"Current Player: {player2.name}")
                    elif player2.current and check_valid_any():
                        player2.current = False
                        player1.current = True
                        current_label.config(text = f"Current Player: {player1.name}")
                    else:
                        last_piece_played["key"] = ''
                        last_piece_played["player"] = ''
                        last_piece_played["space"] = []
                        message_label.config(text = f"No valid placement available. Current player goes again.")

            elif event.widget.cget("bg") == "black":
                message_label.config(text = "INVALID PLACEMENT")

            p1_text = p1_label["text"].split(":")
            p2_text = p2_label["text"].split(":")

            p1_label.config(text = f"{p1_text[0]}: {player1.score}")
            p2_label.config(text = f"{p2_text[0]}: {player2.score}")

            if ((player1.current and player1.piece_count < 1) or 
                (player2.current and player2.piece_count < 1)):
                if player1.score > player2.score:
                    message_label.config(text = f"Game Over! {player1.name} Wins!")
                elif player2.score > player1.score:
                    message_label.config(text = f"Game Over! {player2.name} Wins!")
                else:
                    message_label.config(text = "Game Tied!")

        else:
            message_label.config(text = f"Please select a piece to play.")
    

    def record_piece(self, player): 

        coords = last_piece_played["space"].split(',')

        self.game_board_state[int(coords[0])][int(coords[1])] = last_piece_selected["player"]
        player.piece_count -= 1

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

'''def record_piece(player): 
   
    global game_board_state

    coords = last_piece_played["space"].split(',')

    game_board_state[int(coords[0])][int(coords[1])] = last_piece_selected["player"]
    player.piece_count -= 1'''

def check_score(player, game_board_state):

    sp_x, sp_y = [int(s) for s in (last_piece_played["space"].split(','))]    

    # check for line with piece as start/end of line horizontal
    if sp_y <= 1:
        if check_connected([sp_x, sp_y], [sp_x, sp_y + 1], [sp_x, sp_y + 2], game_board_state):
            player.score += 1
    if sp_y >= 2:
        if check_connected([sp_x, sp_y], [sp_x, sp_y - 1], [sp_x, sp_y - 2], game_board_state):
            player.score += 1

    # check for line with piece as middle of line horizontal
    if sp_y == 1 or sp_y == 2:
        if check_connected([sp_x, sp_y - 1], [sp_x, sp_y], [sp_x, sp_y + 1], game_board_state):
            player.score += 1

    # check for line with piece as start/end of line vertical
    if sp_x <= 1:
        if check_connected([sp_x, sp_y], [sp_x + 1, sp_y], [sp_x + 2, sp_y], game_board_state):
            player.score += 1
    if sp_x >= 2:
        if check_connected([sp_x, sp_y], [sp_x - 1, sp_y], [sp_x - 2, sp_y], game_board_state):
            player.score += 1

    # check for line with piece as middle of line vertical
    if sp_x == 1 or sp_x == 2:
        if check_connected([sp_x - 1, sp_y], [sp_x, sp_y], [sp_x + 1, sp_y], game_board_state):
            player.score += 1

    # check for line with piece as start/end of line diagonal
    if sp_x <= 1 and sp_y <= 1:
        if check_connected([sp_x, sp_y], [sp_x + 1, sp_y + 1], [sp_x + 2, sp_y + 2], game_board_state):
            player.score += 1    
    if sp_x <= 1 and sp_y >= 2:
        if check_connected([sp_x, sp_y], [sp_x + 1, sp_y - 1], [sp_x + 2, sp_y - 2], game_board_state):
            player.score += 1    
    if sp_x >= 2 and sp_y >= 2:
        if check_connected([sp_x, sp_y], [sp_x - 1, sp_y - 1], [sp_x - 2, sp_y - 2], game_board_state):
            player.score += 1    
    if sp_x >= 2 and sp_y <= 1:
        if check_connected([sp_x, sp_y], [sp_x - 1, sp_y + 1], [sp_x - 2, sp_y + 2], game_board_state):
            player.score += 1

    # check for line with piece as middle of line diagonal
    if sp_x == 1 or sp_x == 2:
        if ((check_connected([sp_x - 1, sp_y - 1], [sp_x, sp_y], [sp_x + 1, sp_y + 1], game_board_state)) or 
        (check_connected([sp_x + 1, sp_y - 1], [sp_x, sp_y], [sp_x - 1, sp_y + 1], game_board_state))):
            player.score += 1

def check_connected(space1, space2, space3, game_board_state):
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

def new_game():
    pass
    '''for widget in ROOT.winfo_children():
        widget.destroy()
    ui()'''

def init_game_state(player1, player2):

    global last_piece_selected
    global last_piece_played
    global game_board_state

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

    # Reset piece count and score
    player1.piece_count = 8
    player1.score = 0
    player2.piece_count = 8
    player2.score = 0
    
    player1.current = True
    player2.current = False

def change_settings():

    x = ROOT.winfo_x()
    y = ROOT.winfo_y()
    config = Toplevel(ROOT)
    config.title("Settings")
    config.geometry(f"200x200+{x}+{y}")

    p1_label = Label(config, text = "Player 1:")    
    p2_label = Label(config, text = "Player 2:")
    p1_entry = Entry(config, width = 10)
    p2_entry = Entry(config, width = 10)
    p1_entry.insert(END, P1_NAME)
    p2_entry.insert(END, P2_NAME)

    p1_label.place(x = 10, y = 10)
    p2_label.place(x = 10, y = 40)

    p1_entry.place(x = 75, y = 10)
    p2_entry.place(x = 75, y = 40)

    size_option = IntVar(config, 50)

    Label(config, text = "Size:").place(x = 10, y = 70)
    Radiobutton(config, text = "Small", variable=size_option, value=50).place(x = 75, y = 70)
    Radiobutton(config, text = "Medium", variable=size_option, value=100).place(x = 75, y = 90)
    Radiobutton(config, text = "Large", variable=size_option, value=150).place(x = 75, y = 110)

    Button(config, text = "Save", command = lambda: save_settings(p1_entry.get(), p2_entry.get(), size_option.get(), config)).place(x = 10, y = 165)

    Button(config, text= "Reset", command = lambda: save_settings("Player 1", "Player 2", 50, config)).place(x = 10, y = 130)

    Button(config, text = "Cancel", command = config.destroy).place(x = 75, y = 165)


    
def save_settings(p1, p2, size, config):
    global P1_NAME
    global P2_NAME
    global P_WIDTH
    global INTERVAL

    P1_NAME = p1
    P2_NAME = p2

    P_WIDTH = size
    INTERVAL = P_WIDTH + 3

    cf = open("config.py", "w")
    cf.write('from tkinter import Tk\n\n')
    cf.write('P1_COLOR = "gray"\n')
    cf.write(f'P1_NAME = "{P1_NAME}"\n')
    cf.write('P2_COLOR = "red"\n')
    cf.write(f'P2_NAME = "{P2_NAME}"\n')
    cf.write('B_COLOR = "gray"\n\n')
    cf.write(f'P_WIDTH = {P_WIDTH}\n')
    cf.write(f'INTERVAL = {P_WIDTH} + 3\n\n')
    cf.write('ROOT = Tk()')
    cf.close()
    
    config.destroy()

    new_game()


def ui(player1, player2):

    init_game_state(player1, player2)

    start = 20

    if P_WIDTH == 50:
        p1_x = 20
        p2_x = 458
        gb_x = 186
        st_y = 100
        message_y = 400
        window_x = 624
        window_y = 450
    elif P_WIDTH == 100:
        p1_x = 40
        p2_x = 778
        gb_x = 306
        st_y = 150
        message_y = 650  
        window_x = 1074
        window_y = 775 
    elif P_WIDTH == 150:
        p1_x = 60
        p2_x = 1098
        gb_x = 426
        st_y = 200
        message_y = 900
        window_x = 1524
        window_y = 1153

    ROOT.title("Pylieff")
    ROOT.geometry(f"{window_x}x{window_y}")

    menubar = Menu(ROOT)
    ROOT.config(menu = menubar)

    game_menu = Menu(menubar, tearoff = 0)
    menubar.add_cascade(label="Game", menu=game_menu)

    game_menu.add_command(label = "New Game", command = new_game)
    game_menu.add_command(label = "Settings", command = change_settings)

    message_label = Label(ROOT, text='')
    message_label.place(x = start, y = message_y)

    # Create player pieces
    player1_board = PlayerBoard(player1, p1_x, st_y, start, message_label)
    player2_board = PlayerBoard(player2, p2_x, st_y, start, message_label)

    p1_label = player1_board.create_board()
    p2_label = player2_board.create_board()

    current_label = Label(ROOT, text = f"Current Player: {player1.name}")
    current_label.place(x = start + INTERVAL, y = start)

    # Create Game Board
    game_board = GameBoard(gb_x, st_y, start, message_label)
    game_board.create_board(current_label, p1_label, p2_label, player1, player2)

    ROOT.mainloop()