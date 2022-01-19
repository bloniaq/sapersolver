 # SaperSolver

The application tries to solve expert-sized game of win7-styled 
Minesweeper in full screen mode. 

For now, it doesn't try to take a shot
when it's not sure about mine- and safe field position. It means, that
majority of tries ends near the end. Sometimes try ends early at the
begging. This is due to specifics of minesweeper win7 game - result
depends on luck to some extent. 

Although there are situations, that
application solves whole board.
Here's an example of solved game: https://youtu.be/gsU-hNVL1dM

Reading board and making moves are provided by pyautogui library. Recognizing
fields are quite slow - there is still room for optimization - possibly by
narrowing down region to look at and sampled image to look for.

Model is pure object-oriented python. As said - algorithm needs to be extended
of dealing with situation of randomness. Possibly by a looking for maximum
number of separately subsets of covered fields, which let minimize risk, and
makes shot not-so-blind.

### Installation
Windows users can download proper Minesweeper version from here: 

https://minesweepergame.com/download/windows-7-minesweeper.php

Unfortunatelly I don't know about any Linux nor iOS clone of win7-style 
Minesweper

Package need to be cloned from here, installed by setup with dependecies

### How to use it
Application can be run by `python solver` command in command line when in major 
catalog. At the beggining it starts to look for full-screened window of 
Minesweeper. When it finds it - it starts to solve. Moving mouse or changing 
focus by then, can affect algorithm, so it is advised not to interrupt the process. 

Quitting can be done by either Ctrl+F2 keystroke when focused on console, or by standard
safe-fail mechanism of pyautogui, which is moving cursor to the screen corner.
Also Ctrl-Alt-Delete works, as pyautogui loses screen object and raise an error.

### Configuration
`CLEAR_BOARD` - this constant is in `__main__.py` file, and is responsible for
skip first long part of recognizing all fields if set as True.

`MOVE_DURATION` - this constant is in `controller.py` file, and is responsible for
how long it takes to move cursor before click.

### License
[MIT]