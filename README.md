# Ultimate TicTacToe Playing Bot

#### About
- Ultimate TicTacToe is an extension of the 3x3 TicTacToe, where there are `9 blocks` each having `3x3 cells`.
- Each game is between two teams.
- At the beginning, a coin is flipped to decide the team which will move first (First player).
- The marker for the `first player is ‘x’` and for the `second player is ‘o’`.
- The objective of the game is to win the board by making a legitimate pattern of the blocks.
- A `cell` would refer to any of the `81 smaller squares`.
- A `block` would refer to a `3x3 miniboard` composed of `9 cells`.

#### Rules
1. **[FIRST MOVE]** The very first move of the game is an open move, i.e. `Any cell` on the entire board is valid.
2. **[CORRESPONDENCE RULE]** If the opponent places his/her marker in any of the cells, except for the center cell of a block, then you need to place your marker anywhere in the `two blocks adjacent to the block corresponding to the cell`. For example, for the top left cell, the next player needs to move in center left and top center. Similarly for the right center cell, top right and bottom right blocks are open. Please refer to the code for more clarity.
3. **[CENTER RULE]** If the opponent places his/her marker in the `center cell` of any block, then you need to place your marker in the `center block` only.
4. **[FREE MOVE RULE]** In case the `all of the cells` in the destined blocks obtained from Rule 2 or Rule 3 are `occupied`, then the player may move in `any free cell in the entire board`.
5. **[ABANDON RULE]** Once a block is `won` by a player, it has to be abandoned. That is, you may consider the entire block to be full and `no other player may play` in that block.
6. **[WIN RULE]** The player who wins any three blocks which are either a `row`, `column` or `diagonal` of the board, `wins the game` and the game is over. If all the cells are filled, and `no pattern` has been formed then the `game is
over`.
7. A valid move needs to be returned from the `move` function within `12 seconds`. If the time exceeds 12 seconds for a particular move, then the match will be forfeited and the `opponent wins` by default.

#### Running game : `python evaluator_code.py flag`  
flag :
  - **1** Random player vs AI - Random starts first
  - **2** Human vs. AI
  - **3** Human vs. Human
  - **4** AI vs. Random player - AI starts first
  - **5** AI vs NaiveAI - AI moves first
  - **6** NaiveAI vs AI - NaiveAI moves first
  - **7** AI1 vs AI2 - AI1 moves first
  - **8** AI vs OldAI - OldAI moves first
  - **9** AI vs OldAI - AI moves first
  - **10** 27 vs 64 - 64 moves first
  - **11** 27 vs 64 - 27 moves first


