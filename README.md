# Obstruction

Obstruction is a 2D game in which players take turns in marking squares on a grid. The first player unable to move loses (if there are no empty cells).

The application was developed in Python (client side) and C (server side). The players communicate with the server through a ```TCP``` connection.

In the single-player mode, the player can choose between two options for the opponent player (computer): either randomly for a more unpredictable challenge or using a ```Minimax Algorithm``` for a more strategic and competitive gameplay experience.

## Features
- Human versus Computer mode
- Multiplayer mode
- Graphical User Interface built with the ```Pygame``` library


## AI Implementation 

The AI analysis every posible move by using a minimax evaluation function and tries to maximize the score of the move if it's the computer's turn, or minimize if it's the user's turn (it thinks 2 moves in advance, more than that would seriously affect the time performance)

 ## Video sample

 <p align="center">
  <img src="https://github.com/VladutPasare/Obstruction/blob/main/sample.gif" height="500""/>
 </p>
