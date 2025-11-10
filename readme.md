Computer version of Mijnlieff by Andy Hopwood written in Python.
https://www.xvgames.it/en/mijnlieff/

Game Rules:
Each player begins with an indentical set of 8 pieces.
Play atlernates between the two players.
The first player places a piece anywhere on the board. This piece dictates where the next player can play.
-- Straight: Next piece must be placed in a horizontal or veritcal line.
-- Diagonal: Next piece must be placed in a diagonal line.
-- Pusher: Next piece must be placed so that it is not touching this piece.
-- Puller: Next piece must be placed so that it is touching this piece.
If there is no legal place to play a piece, the player is skipped and the previous player gets to go again.
In this case, there are no restrictions on where the next piece can be played.
Play continues until a player runs out of pieces. Their oppenent gets to play one final piece.
Connect three pieces in a straight line horizontally, vertically or diagonally to score a point.
Connect four pieces to score two points (two lines of three pieces).

Requirements to run:
Python3
Tkinter

Clone the repository:
git clone https://github.com/atmetz/pylieff.git

Run command './pylieff.sh'
