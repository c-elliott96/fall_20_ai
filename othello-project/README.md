# Othello AI Final Project

## [Project PDF](https://docs.google.com/document/d/152lkKyHSlblsCR52PdDR1xWdkYUvQHvYgHZDk2cu1s0/edit)

## Todo & Notes

* Read othello game rules
* Get plan for building this _right_. 

## Othello rules

* 64 pieces (doesn't really matter). 

* Objective is to have more of your color (black or white) on the board
  at the end of the game. 
  
* Black always moves first.

* Game is usually played on 8x8 board. 
  * However, we need to be able to use an NxN board. 
  
  8x8 sample board, with start plays 
   
   0 1 2 3 4 5 6 7 
  =================
 0| | | | | | | | |
  -----------------
 1| | | | | | | | |
  -----------------
 2| | | | | | | | |
  -----------------
 3| | | |O|@| | | |
  -----------------
 4| | | |@|O| | | |
  -----------------
 5| | | | | | | | |
  -----------------
 6| | | | | | | | |
  -----------------
 7| | | | | | | | |
  -----------------
 8| | | | | | | | |
  =================

* Making an invalid move (when our AI is playing on pythonanywhere) will
  result in forfeiting the game

* Black ALWAYS moves first

* A play can only be made if you can place a piece such that you outflank
  your opponent and can flip pieces
  
* Outflanks can be made horizontally, vertically, or diagonally. 

* If you cannot play during a move, you forfeit your turn. 

* A player cannot forfeit the turn if a move can be made.

* The game ends when neither player can make a move.

============================================================

* The main function we need to run is `get_move()`
  * `get_move(board_size, board_state, turn, time_left, opponent_time_left)` where 
    - `board_size` is N.
    - `board_state` is a 2D array of `'W', 'B', or ' '`.
    - `turn` is the _character whose turn it is_ -> `'B'` or `W`.
    - `time_left` is the remaining time for YOUR AI to make the move. `Milliseconds as int`.
    - `opponent_time_left` is the same as above, but for your opponent.
    
    * `get_move()` should return: 
      1. a list ([]) of the format `[row, col]` where row and col are integers. 
      2. `None` if no move can be made. 
      
* Liow's reccommended todos: 
  * Given a board (state) and a color ('B' or 'W'), compute all actions. 
    Test thoroughly. Should be perfect there. 
    
  * Write a dumb AI that returns a random, _valid_ move from the list of 
    all possible actions

  * Main algorithm (Minimax recursively) along w/ Alpha/Beta pruning. 
  
  * Read up on Othello strategies. 
  
  
<!-- FINISHED RANDOM BOT, NOW LET'S TALK ABOUT MINIMAX --> 

# Binary representation of the board

* Board is N x N values

* We will receive the board as a 2D array (list of lists) of each
  tile's value. 
  
* Those values can be: 'W', 'B', or ' '. The board starts with:
  ``` 
  |W|B|
  |B|W|
  ```
  in the middle. 
  
* To represent 3 values in binary, we need two bits. 
* Let's define them as:
  * ' ' = 00
  * 'W' = 01
  * 'B' = 10
  * Note: This does leave us with a value for 11. Unsure if this is useful
    or not. 
    
* So, the first thing I want to do is figure out how to convert the 2D 
  representation to a binary number of length `N*N*2`. 
  
* The smallest data representation in python 2 appears to be 24 bits. 
  Even sys.getsizeof(0b00) # 00 in binary # is 24. 
  Further, sys.getsizeof(True) is 24. 
