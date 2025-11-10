from ui import ui
from config import P1_COLOR, P1_NAME, P2_COLOR, P2_NAME

class Player:
    def __init__(self, name, color, score=0):
        self.name = name
        self.color = color
        self.score = score

def main():
    print("Running Pylieff!")
    player1 = Player(P1_NAME, P1_COLOR)
    player2 = Player(P2_NAME, P2_COLOR)
    ui(player1, player2)

if __name__ == "__main__":
    main()