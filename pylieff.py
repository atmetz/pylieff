from ui import ui
from config import P1_COLOR, P1_NAME, P2_COLOR, P2_NAME

class Player:
    def __init__(self, name, color, piece_count = 8, score = 3, current = False):
        self.name = name
        self.color = color
        self.piece_count = piece_count
        self.score = score
        self.current = current

def main():
    print("Running Pylieff!")
    player1 = Player(P1_NAME, P1_COLOR)
    player2 = Player(P2_NAME, P2_COLOR)
    ui(player1, player2)

if __name__ == "__main__":
    main()