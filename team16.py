import random
import copy
import collections
import time

class Player16:

    def __init__(self):
        
        self.no_of_moves=0  ## TO hardcode first few moves
        self.block_num=[] ## STORE BLOCKS ALLOWED, TOBE USED BY HEURISTIC
        self.MAX_DEPTH=3
        self.start_time=0

    def move(self, current_board_game, board_stat, move_by_opponent, flag):
        
        self.start_time=time.time()
        temp_board = current_board_game[:]
        temp_block = board_stat[:]
        old_move = move_by_opponent
        own_flag = flag

        self.no_of_moves=self.no_of_moves+1 ## COUNT MOVES

        # HARDCODING FIRST FEW MOVES
        # if(no_of_moves < 5):
        if(move_by_opponent[0]==-1 and move_by_opponent[1]==-1):
             return(4,4)

        if(self.no_of_moves<7):
            self.MAX_DEPTH=2
        elif(self.no_of_moves<15):
            self.MAX_DEPTH=3
        elif(self.no_of_moves<20):
            self.MAX_DEPTH=4
        elif(self.no_of_moves<27):
            self.MAX_DEPTH=5
        elif(self.no_of_moves<33):
            self.MAX_DEPTH=6
        elif(self.no_of_moves<38):
            self.MAX_DEPTH=7
        else :
            self.MAX_DEPTH=8


        print "Max depth is =" ,self.MAX_DEPTH

        
        move = self.alphabeta_search(temp_board, temp_block, old_move, own_flag)
        return move
       

    def alphabeta_search(self, state, block, old_move,own_flag):
        
        def max_value(cell, state, block, given_flag, alpha, beta, depth):
            
            
            v = -100000
            old_move = cell
            new_state = copy.deepcopy(state)
            new_block = block[:]
            # we made the move that EARLIER ONE WAS SUPPOSED TO MAKE
            self.update_lists(new_state, new_block, cell,given_flag)
            
            if (self.cutoff_test(cell,new_state,new_block,depth)==1):
                 return (self.eval_fn_local(cell, new_state,new_block,own_flag) + self.eval_fn_global(cell, new_state,new_block,own_flag))

            list_of_moves = self.get_allowed_moves(new_state, new_block,old_move,self.other_flag(given_flag))


            for a in list_of_moves:
                v = max(v, min_value(a, new_state, new_block, self.other_flag(given_flag),alpha, beta, depth+1))
                if v >= beta:
                    return v
                alpha = max(alpha, v)
            return v            


        def min_value(cell, state, block, given_flag, alpha, beta, depth):
            
            v = 100000
            old_move = cell
            new_state = copy.deepcopy(state)
            new_block = block[:]
            # we made the move that EARLIER ONE WAS SUPPOSED TO MAKE
            self.update_lists(new_state, new_block, cell,given_flag)
            # here , the game board is updated with earliers move
            if (self.cutoff_test(cell,new_state,new_block,depth)==1):
                return (self.eval_fn_local(cell, new_state,new_block,own_flag) + self.eval_fn_global(cell, new_state,new_block,own_flag))

            # NOW BEGIN WITH MIN-Function
            # now which moves this MIN can make
            list_of_moves = self.get_allowed_moves(new_state, new_block,old_move,self.other_flag(given_flag))
            for a in list_of_moves:
                v = min(v, max_value(a, new_state, new_block, self.other_flag(given_flag),alpha, beta, depth+1))
                if v <= alpha:
                    return v
                beta = min(beta, v)
            return v


        list_of_moves = self.get_allowed_moves(state, block, old_move, own_flag)
        # print 'The list of tuples is ::',list_of_moves
        maximum_return_value= -100000 -1
        candidate_tuple=[]
        for i in list_of_moves:
            value=min_value( i , state, block , own_flag,-100000,100000, 0) # pass own flag to MIN
            if value>maximum_return_value:
                maximum_return_value=value
                candidate_tuple=i
            if(time.time()-self.start_time>11):
                break

        return candidate_tuple

    ############################# GIVEN FUNCTIONS ##############
    def get_allowed_moves(self, temp_board, temp_block, purana, flag):
        # return all possible TUPLEs (as a list) that we can make in temp_board
        delta = []
        if purana[0]  ==-1 and purana[1]==-1: ## SUPPOSE WE ARE FIRST TO MOVE
            delta=[4]
        elif purana[0] % 3 == 0 and purana[1] % 3 == 0:
            delta = [1,3]
        elif purana[0] % 3 == 0 and purana[1] % 3 == 2:
            delta = [1,5]
        elif purana[0] % 3 == 2 and purana[1] % 3 == 0:
            delta = [3,7]
        elif purana[0] % 3 == 2 and purana[1] % 3 == 2:
            delta = [5,7]
        elif purana[0] % 3 == 0 and purana[1] % 3 == 1:
            delta = [0,2]
        elif purana[0] % 3 == 1 and purana[1] % 3 == 0:
            delta = [0,6]
        elif purana[0] % 3 == 2 and purana[1] % 3 == 1:
            delta = [6,8]
        elif purana[0] % 3 == 1 and purana[1] % 3 == 2:
            delta = [2,8]
        elif purana[0] % 3 == 1 and purana[1] % 3 == 1:
            delta = [4]

        final_blocks_allowed = []
        for i in delta:
            if temp_block[i] == '-':
                final_blocks_allowed.append(i)
        # We get all the empty cells in allowed blocks. If they're all full, we get all the empty cells in the entire board.
        self.block_num=final_blocks_allowed
        cells = self.get_cells(temp_board, final_blocks_allowed, temp_block,flag)
        return cells

    def get_cells(self, board, allowed, block,flag):

        tuples = []
        # values=[]
        
        for delta in allowed:
            gamma = delta/3
            alpha = delta%3
            for i in range(gamma*3,gamma*3+3):
                for j in range(alpha*3,alpha*3+3):
                    if board[i][j] == '-':
                        tuples.append((i,j))
                        # values.append(self.helper(board,((i,j)),flag))
        # Suppose no move found, then we are free to move any where
        if tuples == []:
            if(block[4]=='-'):
                for i in range(3,6):
                    for j in range (3,6):
                        if (board[i][j] == '-'):
                            tuples.append((i,j))
                if(len(tuples)>0):
                    return tuples
                

            for i in range(9):
                for j in range(9):
                    zeta  = (i/3)*3
                    zeta += (j/3)
                    if board[i][j] == '-' and block[zeta] == '-':
                        tuples.append((i,j))
                        # values.append(self.helper(board,((i,j)),flag) )

        ## Sort tuples by calling 


        # final_tuples=[x for (y,x) in sorted(zip(values,tuples))]
        return tuples

    def update_lists(self, game_board, block_stat, move_ret, fl):
        game_board[move_ret[0]][move_ret[1]] = fl

        block_no = (move_ret[0]/3)*3 + move_ret[1]/3
        id1 = block_no/3
        id2 = block_no%3
        mg = 0
        mflg = 0
        if block_stat[block_no] == '-':
            if game_board[id1*3][id2*3] == game_board[id1*3+1][id2*3+1] and game_board[id1*3+1][id2*3+1] == game_board[id1*3+2][id2*3+2] and game_board[id1*3+1][id2*3+1] != '-':
                mflg=1
            if game_board[id1*3+2][id2*3] == game_board[id1*3+1][id2*3+1] and game_board[id1*3+1][id2*3+1] == game_board[id1*3][id2*3 + 2] and game_board[id1*3+1][id2*3+1] != '-':
                mflg=1
            
            if mflg != 1:
                for i in range(id2*3,id2*3+3):
                    if game_board[id1*3][i]==game_board[id1*3+1][i] and game_board[id1*3+1][i] == game_board[id1*3+2][i] and game_board[id1*3][i] != '-':
                        mflg = 1
                        break

                    ### row-wise
            if mflg != 1:
                for i in range(id1*3,id1*3+3):
                    if game_board[i][id2*3]==game_board[i][id2*3+1] and game_board[i][id2*3+1] == game_board[i][id2*3+2] and game_board[i][id2*3] != '-':
                        mflg = 1
                        break

        
        if mflg == 1:
            block_stat[block_no] = fl
        
        #check for draw on the block.

        id1 = block_no/3
        id2 = block_no%3
        cells = []
        for i in range(id1*3,id1*3+3):
            for j in range(id2*3,id2*3+3):
                if game_board[i][j] == '-':
                    cells.append((i,j))

        if cells == [] and mflg!=1:
            block_stat[block_no] = 'd' #Draw
        
        return

    ########################### CUSTOM FUNCTIONS ###############
    def other_flag(self, flag):
        if flag == 'x':
            return 'o'
        else:
            return 'x'

    def cutoff_test(self,cell,state,block,depth):
        # if (time.time()- self.start_time > 11.5) or depth>MAX_DEPTH:
            # print "CUTTING AT DEPTH = ",depth
        if depth>self.MAX_DEPTH:
            # print 'DEPTH Is ', depth
            return 1
        else:
            return 0

    def eval_fn_local(self,cell, board,block,own_flag):
        ## Determine the block in which the move was made
        

        x=(cell[0]/3)*3
        y=(cell[1]/3)*3
        point=1
        opponent=self.other_flag(own_flag)
        a=[board[x][y],board[x][y+1],board[x][y+2],board[x+1][y],board[x+1][y+1],board[x+1][y+2],board[x+2][y],board[x+2][y+1],board[x+2][y+2]]
        

        ############## SURE WINS ARE CHECKED HERE
        if( a[0] == a[1] and a[1] == a[2] and a[0] == opponent ) or ( a[6] == a[7] and a[7] == a[8] and a[6] == opponent):
                return -100
        elif ( a[0] == a[1] and a[1] == a[2] and a[0] == own_flag ) or ( a[6] == a[7] and a[7] == a[8] and a[6] == own_flag):
               return 100
        if  ( a[3] == a[4] and a[4] == a[5] and a[3] == opponent):
                return -90 
        elif( a[3] == a[4] and a[4] == a[5] and a[3] == own_flag):
                return 90 

        
        if ( a[0] == a[3] and a[3] == a[6] and a[0] == opponent ) or  ( a[2] == a[5] and a[5] == a[8] and a[5] == opponent):
                return -100
        elif ( a[0] == a[3] and a[3] == a[6] and a[0] == own_flag )  or ( a[2] == a[5] and a[5] == a[8] and a[5] == own_flag):
               return 100
        if ( a[1] == a[4] and a[4] == a[7] and a[1] == opponent):
                return -90
        elif  ( a[1] == a[4] and a[4] == a[7] and a[1] == own_flag):
                return 90

        
        if (a[0] == a[4] and a[4] == a[8] and a[0]==opponent) or (a[2] == a[4] and a[4] == a[6] and a[2]==opponent):
            return -90
        elif (a[0] == a[4] and a[4] == a[8] and a[0]==own_flag) or (a[2] == a[4] and a[4] == a[6] and a[2]==own_flag):
            return 90

        ############### PARTIAL WINS ARE CHECKED HERE  eg xx- , x-x , -xx 

        row=a[0]+a[1]+a[2]
        dic=collections.Counter(row)
        if ( dic[own_flag]==2 and dic['-']==1):
            point = point+ 21
        elif( dic[opponent]==2 and dic['-']==1):
            point=point -18
        elif ( dic[own_flag]==1 and dic['-']==2):
            point=point + 15
        elif( dic[opponent]==1 and dic['-']==2):
            point=point -13

        row=a[3]+a[4]+a[5]
        dic=collections.Counter(row)
        if (dic[own_flag]==2 and dic['-']==1):
            point=point+ 18
        elif(dic[opponent]==2 and dic['-']==1):
            point=point -15
        elif(dic[own_flag]==1 and dic['-']==2):
            point=point+ 13
        elif(dic[opponent]==1 and dic['-']==2):
            point=point -10

        row=a[6]+a[7]+a[8]
        dic=collections.Counter(row)
        if (dic[own_flag]==2 and dic['-']==1):
            point=point+ 21
        elif(dic[opponent]==2 and dic['-']==1):
            point=point -18
        elif(dic[own_flag]==1 and dic['-']==2):
            point=point+ 15
        elif(dic[opponent]==1 and dic['-']==2):
            point=point -13

        ## COLOUMN
    
        row=a[0]+a[3]+a[6]
        dic=collections.Counter(row)
        if (dic[own_flag]==2 and dic['-']==1):
            point=point+ 21
        elif(dic[opponent]==2 and dic['-']==1):
            point=point -18
        elif (dic[own_flag]==1 and dic['-']==2):
             point=point+ 15
        elif(dic[opponent]==1 and dic['-']==2):
            point=point -13

        row=a[1]+a[4]+a[7]
        dic=collections.Counter(row)
        if (dic[own_flag]==2 and dic['-']==1):
            point=point+ 18
        elif(dic[opponent]==2 and dic['-']==1):
            point=point -15
        elif(dic[own_flag]==1 and dic['-']==2):
            point=point+ 13
        elif(dic[opponent]==1 and dic['-']==2):
            point=point -10

        row=a[2]+a[5]+a[8]
        dic=collections.Counter(row)
        if (dic[own_flag]==2 and dic['-']==1):
            point=point+ 21
        elif(dic[opponent]==2 and dic['-']==1):
            point=point -18
        elif(dic[own_flag]==1 and dic['-']==2):
             point=point+ 15
        elif(dic[opponent]==1 and dic['-']==2):
            point=point -13

        ## DIAGONAL
    
        row=a[0]+a[4]+a[8]
        dic=collections.Counter(row)
        if (dic[own_flag]==2 and dic['-']==1):
            point=point+ 18
        elif(dic[opponent]==2 and dic['-']==1):
            point=point -15
        elif (dic[own_flag]==1 and dic['-']==2):
            point=point+ 13
        elif(dic[opponent]==1 and dic['-']==2):
            point=point -10

        row=a[2]+a[4]+a[6]
        dic=collections.Counter(row)
        if (dic[own_flag]==2 and dic['-']==1):
            point=point+ 18
        elif(dic[opponent]==2 and dic['-']==1):
            point=point -15
        elif(dic[own_flag]==1 and dic['-']==2):
            point=point+ 13
        elif(dic[opponent]==1 and dic['-']==2):
            point=point -10

        ################## MOVES FOR SINGLE x
        return point



        ##########################CHECK ADVANTAGE IN BLOCK ##################################


    def eval_fn_global(self,cell, board,block,own_flag):
        point=1
        opponent=self.other_flag(own_flag)

        ## CORNER MOVE
        blk = (cell[0]/3)*3 + cell[1]/3


        if( block[0] == block[1] and block[1] == block[2] and block[0] == opponent ) or ( block[6] == block[7] and block[7] == block[8] and block[6] == opponent):
                return -200
        elif ( block[0] == block[1] and block[1] == block[2] and block[0] == own_flag ) or ( block[6] == block[7] and block[7] == block[8] and block[6] == own_flag):
               return 200
        if  ( block[3] == block[4] and block[4] == block[5] and block[3] == opponent):
                return -180 
        elif( block[3] == block[4] and block[4] == block[5] and block[3] == own_flag):
                return 180 

        
        if ( block[0] == block[3] and block[3] == block[6] and block[0] == opponent ) or  ( block[2] == block[5] and block[5] == block[8] and block[5] == opponent):
                return -200
        elif ( block[0] == block[3] and block[3] == block[6] and block[0] == own_flag )  or ( block[2] == block[5] and block[5] == block[8] and block[5] == own_flag):
               return 200
        if ( block[1] == block[4] and block[4] == block[7] and block[1] == opponent):
                return -180
        elif  ( block[1] == block[4] and block[4] == block[7] and block[1] == own_flag):
                return 180

        
        if (block[0] == block[4] and block[4] == block[8] and block[0]==opponent) or (block[2] == block[4] and block[4] == block[6] and block[2]==opponent):
            return 180
        elif (block[0] == block[4] and block[4] == block[8] and block[0]==own_flag) or (block[2] == block[4] and block[4] == block[6] and block[2]==own_flag):
            return -180


        ### PARTIAL WIN

        row=block[0]+block[1]+block[2]
        dic=collections.Counter(row)
        if ( dic[own_flag]==2 and dic['-']==1):
            point=point+ 60
        elif( dic[opponent]==2 and dic['-']==1):
            point=point -50
        elif ( dic[own_flag]==1 and dic['-']==2):
            point=point+ 30                                   ## check this
        elif( dic[opponent]==1 and dic['-']==2):
            point=point -25

        row=block[3]+block[4]+block[5]
        dic=collections.Counter(row)
        if (dic[own_flag]==2 and dic['-']==1):
            point=point+ 80
        elif(dic[opponent]==2 and dic['-']==1):
            point=point -70
        elif ( dic[own_flag]==1 and dic['-']==2):
            point=point+ 50                                   ## check this
        elif( dic[opponent]==1 and dic['-']==2):
            point=point -40

        row=block[6]+block[7]+block[8]
        dic=collections.Counter(row)
        if (dic[own_flag]==2 and dic['-']==1):
            point=point+ 60
        elif(dic[opponent]==2 and dic['-']==1):
            point=point -50
        elif ( dic[own_flag]==1 and dic['-']==2):
            point=point+ 30                                   ## check this
        elif( dic[opponent]==1 and dic['-']==2):
            point=point -25

        ## COLOUMN
    
        row=block[0]+block[3]+block[6]
        dic=collections.Counter(row)
        if (dic[own_flag]==2 and dic['-']==1):
            point=point+ 60
        elif(dic[opponent]==2 and dic['-']==1):
            point=point -50
        elif ( dic[own_flag]==1 and dic['-']==2):
            point=point+ 30                                   ## check this
        elif( dic[opponent]==1 and dic['-']==2):
            point=point -25

        row=block[1]+block[4]+block[7]
        dic=collections.Counter(row)
        if (dic[own_flag]==2 and dic['-']==1):
            point=point+ 80
        elif(dic[opponent]==2 and dic['-']==1):
            point=point -70
        elif ( dic[own_flag]==1 and dic['-']==2):
            point=point+ 50                                  ## check this
        elif( dic[opponent]==1 and dic['-']==2):
            point=point -40

        row=block[2]+block[5]+block[8]
        dic=collections.Counter(row)
        if (dic[own_flag]==2 and dic['-']==1):
            point=point+ 60
        elif(dic[opponent]==2 and dic['-']==1):
            point=point -50
        elif ( dic[own_flag]==1 and dic['-']==2):
            point=point+ 30                                   ## check this
        elif( dic[opponent]==1 and dic['-']==2):
            point=point -25

        ## DIAGONAL
    
        row=block[0]+block[4]+block[8]
        dic=collections.Counter(row)
        if (dic[own_flag]==2 and dic['-']==1):
            point=point+ 80
        elif(dic[opponent]==2 and dic['-']==1):
            point=point -70
        elif ( dic[own_flag]==1 and dic['-']==2):
            point=point+ 50                                   ## check this
        elif( dic[opponent]==1 and dic['-']==2):
            point=point -40

        row=block[2]+block[4]+block[6]
        dic=collections.Counter(row)
        if (dic[own_flag]==2 and dic['-']==1):
            point=point+ 80
        elif(dic[opponent]==2 and dic['-']==1):
            point=point -70
        elif ( dic[own_flag]==1 and dic['-']==2):
            point=point+ 50                                   ## check this
        elif( dic[opponent]==1 and dic['-']==2):
            point=point -40


        return point




    def helper(self,board,tup,flag):
        x=(tup[0]/3)*3
        y=(tup[1]/3)*3
        point=0
        
        if flag=='x':
            opponent='o'
        else:
            opponent='x'

        a=[ [0,0,0],[0,0,0],[0,0,0]]
        a[0][0]=board[x][y]
        a[0][1]=board[x][y+1]
        a[0][2]=board[x][y+2]
        a[1][0]=board[x+1][y]
        a[1][1]=board[x+1][y+1]
        a[1][2]=board[x+1][y+2]
        a[2][0]=board[x+2][y]
        a[2][1]=board[x+2][y+1]
        a[2][2]=board[x+2][y+2]
        
        
        pos_x= tup[0]%3  
        pos_y= tup[1]%3

        row=a[pos_x][0]+a[pos_x][1]+a[pos_x][2]
        coloumn=a[0][pos_y]+a[1][pos_y]+a[2][pos_y]

        dic_row=collections.Counter(row)
        dic_coloumn=collections.Counter(coloumn)
        ## Check row

        if (dic_row[flag]==2 and dic_row['-']==1):
            point+=4
        elif(dic_row[flag]==1 and dic_row['-']==2):
            point+=2

        if (dic_coloumn[flag]==2 and dic_coloumn['-']==1):
            point+=4
        elif(dic_coloumn[flag]==1 and dic_coloumn['-']==2):
            point+=2

        if(pos_x==pos_y):
            row=a[0][0]+a[1][1]+a[2][2]
            dic_row=collections.Counter(row)
            if (dic_row[flag]==2 and dic_row['-']==1):
                point+=4
            elif(dic_row[flag]==1 and dic_row['-']==2):
                point+=2

        return point




##################### THE RANDOM BOT OUTPUT ###################
# prakhar@hp:~/Desktop$ python evaluator_code.py 1
# =========== Game Board ===========
# - - -  - - -  - - -
# - - -  - - -  - - -
# - - -  - - -  - - -

# - - -  - - -  - - -
# - - -  - - -  - - -
# - - -  - - -  - - -

# - - -  - - -  - - -
# - - -  - - -  - - -
# - - -  - - -  - - -
# ==================================
# =========== Block Status =========
# - - -
# - - -
# - - -
# ==================================

# Player 1 made the move: (4, 4) with x
# =========== Game Board ===========
# - - -  - - -  - - -
# - - -  - - -  - - -
# - - -  - - -  - - -

# - - -  - - -  - - -
# - - -  - x -  - - -
# - - -  - - -  - - -

# - - -  - - -  - - -
# - - -  - - -  - - -
# - - -  - - -  - - -
# ==================================
# =========== Block Status =========
# - - -
# - - -
# - - -
# ==================================

# Player 2 made the move: (5, 4) with o
# =========== Game Board ===========
# - - -  - - -  - - -
# - - -  - - -  - - -
# - - -  - - -  - - -

# - - -  - - -  - - -
# - - -  - x -  - - -
# - - -  - o -  - - -

# - - -  - - -  - - -
# - - -  - - -  - - -
# - - -  - - -  - - -
# ==================================
# =========== Block Status =========
# - - -
# - - -
# - - -
# ==================================

# Max depth is = 2
# Player 1 made the move: (6, 0) with x
# =========== Game Board ===========
# - - -  - - -  - - -
# - - -  - - -  - - -
# - - -  - - -  - - -

# - - -  - - -  - - -
# - - -  - x -  - - -
# - - -  - o -  - - -

# x - -  - - -  - - -
# - - -  - - -  - - -
# - - -  - - -  - - -
# ==================================
# =========== Block Status =========
# - - -
# - - -
# - - -
# ==================================

# Player 2 made the move: (5, 1) with o
# =========== Game Board ===========
# - - -  - - -  - - -
# - - -  - - -  - - -
# - - -  - - -  - - -

# - - -  - - -  - - -
# - - -  - x -  - - -
# - o -  - o -  - - -

# x - -  - - -  - - -
# - - -  - - -  - - -
# - - -  - - -  - - -
# ==================================
# =========== Block Status =========
# - - -
# - - -
# - - -
# ==================================

# Max depth is = 2
# Player 1 made the move: (7, 7) with x
# =========== Game Board ===========
# - - -  - - -  - - -
# - - -  - - -  - - -
# - - -  - - -  - - -

# - - -  - - -  - - -
# - - -  - x -  - - -
# - o -  - o -  - - -

# x - -  - - -  - - -
# - - -  - - -  - x -
# - - -  - - -  - - -
# ==================================
# =========== Block Status =========
# - - -
# - - -
# - - -
# ==================================

# Player 2 made the move: (3, 3) with o
# =========== Game Board ===========
# - - -  - - -  - - -
# - - -  - - -  - - -
# - - -  - - -  - - -

# - - -  o - -  - - -
# - - -  - x -  - - -
# - o -  - o -  - - -

# x - -  - - -  - - -
# - - -  - - -  - x -
# - - -  - - -  - - -
# ==================================
# =========== Block Status =========
# - - -
# - - -
# - - -
# ==================================

# Max depth is = 2
# Player 1 made the move: (1, 4) with x
# =========== Game Board ===========
# - - -  - - -  - - -
# - - -  - x -  - - -
# - - -  - - -  - - -

# - - -  o - -  - - -
# - - -  - x -  - - -
# - o -  - o -  - - -

# x - -  - - -  - - -
# - - -  - - -  - x -
# - - -  - - -  - - -
# ==================================
# =========== Block Status =========
# - - -
# - - -
# - - -
# ==================================

# Player 2 made the move: (5, 3) with o
# =========== Game Board ===========
# - - -  - - -  - - -
# - - -  - x -  - - -
# - - -  - - -  - - -

# - - -  o - -  - - -
# - - -  - x -  - - -
# - o -  o o -  - - -

# x - -  - - -  - - -
# - - -  - - -  - x -
# - - -  - - -  - - -
# ==================================
# =========== Block Status =========
# - - -
# - - -
# - - -
# ==================================

# Max depth is = 2
# Player 1 made the move: (3, 0) with x
# =========== Game Board ===========
# - - -  - - -  - - -
# - - -  - x -  - - -
# - - -  - - -  - - -

# x - -  o - -  - - -
# - - -  - x -  - - -
# - o -  o o -  - - -

# x - -  - - -  - - -
# - - -  - - -  - x -
# - - -  - - -  - - -
# ==================================
# =========== Block Status =========
# - - -
# - - -
# - - -
# ==================================

# Player 2 made the move: (0, 4) with o
# =========== Game Board ===========
# - - -  - o -  - - -
# - - -  - x -  - - -
# - - -  - - -  - - -

# x - -  o - -  - - -
# - - -  - x -  - - -
# - o -  o o -  - - -

# x - -  - - -  - - -
# - - -  - - -  - x -
# - - -  - - -  - - -
# ==================================
# =========== Block Status =========
# - - -
# - - -
# - - -
# ==================================

# Max depth is = 2
# Player 1 made the move: (0, 0) with x
# =========== Game Board ===========
# x - -  - o -  - - -
# - - -  - x -  - - -
# - - -  - - -  - - -

# x - -  o - -  - - -
# - - -  - x -  - - -
# - o -  o o -  - - -

# x - -  - - -  - - -
# - - -  - - -  - x -
# - - -  - - -  - - -
# ==================================
# =========== Block Status =========
# - - -
# - - -
# - - -
# ==================================

# Player 2 made the move: (5, 2) with o
# =========== Game Board ===========
# x - -  - o -  - - -
# - - -  - x -  - - -
# - - -  - - -  - - -

# x - -  o - -  - - -
# - - -  - x -  - - -
# - o o  o o -  - - -

# x - -  - - -  - - -
# - - -  - - -  - x -
# - - -  - - -  - - -
# ==================================
# =========== Block Status =========
# - - -
# - - -
# - - -
# ==================================

# Max depth is = 3
# Player 1 made the move: (3, 7) with x
# =========== Game Board ===========
# x - -  - o -  - - -
# - - -  - x -  - - -
# - - -  - - -  - - -

# x - -  o - -  - x -
# - - -  - x -  - - -
# - o o  o o -  - - -

# x - -  - - -  - - -
# - - -  - - -  - x -
# - - -  - - -  - - -
# ==================================
# =========== Block Status =========
# - - -
# - - -
# - - -
# ==================================

# Player 2 made the move: (0, 7) with o
# =========== Game Board ===========
# x - -  - o -  - o -
# - - -  - x -  - - -
# - - -  - - -  - - -

# x - -  o - -  - x -
# - - -  - x -  - - -
# - o o  o o -  - - -

# x - -  - - -  - - -
# - - -  - - -  - x -
# - - -  - - -  - - -
# ==================================
# =========== Block Status =========
# - - -
# - - -
# - - -
# ==================================

# Max depth is = 3
# Player 1 made the move: (0, 1) with x
# =========== Game Board ===========
# x x -  - o -  - o -
# - - -  - x -  - - -
# - - -  - - -  - - -

# x - -  o - -  - x -
# - - -  - x -  - - -
# - o o  o o -  - - -

# x - -  - - -  - - -
# - - -  - - -  - x -
# - - -  - - -  - - -
# ==================================
# =========== Block Status =========
# - - -
# - - -
# - - -
# ==================================

# Player 2 made the move: (1, 6) with o
# =========== Game Board ===========
# x x -  - o -  - o -
# - - -  - x -  o - -
# - - -  - - -  - - -

# x - -  o - -  - x -
# - - -  - x -  - - -
# - o o  o o -  - - -

# x - -  - - -  - - -
# - - -  - - -  - x -
# - - -  - - -  - - -
# ==================================
# =========== Block Status =========
# - - -
# - - -
# - - -
# ==================================

# Max depth is = 3
# Player 1 made the move: (0, 2) with x
# =========== Game Board ===========
# x x x  - o -  - o -
# - - -  - x -  o - -
# - - -  - - -  - - -

# x - -  o - -  - x -
# - - -  - x -  - - -
# - o o  o o -  - - -

# x - -  - - -  - - -
# - - -  - - -  - x -
# - - -  - - -  - - -
# ==================================
# =========== Block Status =========
# x - -
# - - -
# - - -
# ==================================

# Player 2 made the move: (2, 5) with o
# =========== Game Board ===========
# x x x  - o -  - o -
# - - -  - x -  o - -
# - - -  - - o  - - -

# x - -  o - -  - x -
# - - -  - x -  - - -
# - o o  o o -  - - -

# x - -  - - -  - - -
# - - -  - - -  - x -
# - - -  - - -  - - -
# ==================================
# =========== Block Status =========
# x - -
# - - -
# - - -
# ==================================

# Max depth is = 3
# Player 1 made the move: (3, 8) with x
# =========== Game Board ===========
# x x x  - o -  - o -
# - - -  - x -  o - -
# - - -  - - o  - - -

# x - -  o - -  - x x
# - - -  - x -  - - -
# - o o  o o -  - - -

# x - -  - - -  - - -
# - - -  - - -  - x -
# - - -  - - -  - - -
# ==================================
# =========== Block Status =========
# x - -
# - - -
# - - -
# ==================================

# Player 2 made the move: (5, 6) with o
# =========== Game Board ===========
# x x x  - o -  - o -
# - - -  - x -  o - -
# - - -  - - o  - - -

# x - -  o - -  - x x
# - - -  - x -  - - -
# - o o  o o -  o - -

# x - -  - - -  - - -
# - - -  - - -  - x -
# - - -  - - -  - - -
# ==================================
# =========== Block Status =========
# x - -
# - - -
# - - -
# ==================================

# Max depth is = 3
# Player 1 made the move: (3, 1) with x
# =========== Game Board ===========
# x x x  - o -  - o -
# - - -  - x -  o - -
# - - -  - - o  - - -

# x x -  o - -  - x x
# - - -  - x -  - - -
# - o o  o o -  o - -

# x - -  - - -  - - -
# - - -  - - -  - x -
# - - -  - - -  - - -
# ==================================
# =========== Block Status =========
# x - -
# - - -
# - - -
# ==================================

# Player 2 made the move: (2, 7) with o
# =========== Game Board ===========
# x x x  - o -  - o -
# - - -  - x -  o - -
# - - -  - - o  - o -

# x x -  o - -  - x x
# - - -  - x -  - - -
# - o o  o o -  o - -

# x - -  - - -  - - -
# - - -  - - -  - x -
# - - -  - - -  - - -
# ==================================
# =========== Block Status =========
# x - -
# - - -
# - - -
# ==================================

# Max depth is = 3
# Player 1 made the move: (6, 2) with x
# =========== Game Board ===========
# x x x  - o -  - o -
# - - -  - x -  o - -
# - - -  - - o  - o -

# x x -  o - -  - x x
# - - -  - x -  - - -
# - o o  o o -  o - -

# x - x  - - -  - - -
# - - -  - - -  - x -
# - - -  - - -  - - -
# ==================================
# =========== Block Status =========
# x - -
# - - -
# - - -
# ==================================

# Player 2 made the move: (4, 7) with o
# =========== Game Board ===========
# x x x  - o -  - o -
# - - -  - x -  o - -
# - - -  - - o  - o -

# x x -  o - -  - x x
# - - -  - x -  - o -
# - o o  o o -  o - -

# x - x  - - -  - - -
# - - -  - - -  - x -
# - - -  - - -  - - -
# ==================================
# =========== Block Status =========
# x - -
# - - -
# - - -
# ==================================

# Max depth is = 3
# Player 1 made the move: (4, 3) with x
# =========== Game Board ===========
# x x x  - o -  - o -
# - - -  - x -  o - -
# - - -  - - o  - o -

# x x -  o - -  - x x
# - - -  x x -  - o -
# - o o  o o -  o - -

# x - x  - - -  - - -
# - - -  - - -  - x -
# - - -  - - -  - - -
# ==================================
# =========== Block Status =========
# x - -
# - - -
# - - -
# ==================================

# Player 2 made the move: (7, 1) with o
# =========== Game Board ===========
# x x x  - o -  - o -
# - - -  - x -  o - -
# - - -  - - o  - o -

# x x -  o - -  - x x
# - - -  x x -  - o -
# - o o  o o -  o - -

# x - x  - - -  - - -
# - o -  - - -  - x -
# - - -  - - -  - - -
# ==================================
# =========== Block Status =========
# x - -
# - - -
# - - -
# ==================================

# Max depth is = 3
# Player 1 made the move: (4, 5) with x
# =========== Game Board ===========
# x x x  - o -  - o -
# - - -  - x -  o - -
# - - -  - - o  - o -

# x x -  o - -  - x x
# - - -  x x x  - o -
# - o o  o o -  o - -

# x - x  - - -  - - -
# - o -  - - -  - x -
# - - -  - - -  - - -
# ==================================
# =========== Block Status =========
# x - -
# - x -
# - - -
# ==================================

# Player 2 made the move: (0, 6) with o
# =========== Game Board ===========
# x x x  - o -  o o -
# - - -  - x -  o - -
# - - -  - - o  - o -

# x x -  o - -  - x x
# - - -  x x x  - o -
# - o o  o o -  o - -

# x - x  - - -  - - -
# - o -  - - -  - x -
# - - -  - - -  - - -
# ==================================
# =========== Block Status =========
# x - -
# - x -
# - - -
# ==================================

# Max depth is = 4
# Player 1 made the move: (3, 2) with x
# =========== Game Board ===========
# x x x  - o -  o o -
# - - -  - x -  o - -
# - - -  - - o  - o -

# x x x  o - -  - x x
# - - -  x x x  - o -
# - o o  o o -  o - -

# x - x  - - -  - - -
# - o -  - - -  - x -
# - - -  - - -  - - -
# ==================================
# =========== Block Status =========
# x - -
# x x -
# - - -
# ==================================

# Player 2 made the move: (4, 8) with o
# =========== Game Board ===========
# x x x  - o -  o o -
# - - -  - x -  o - -
# - - -  - - o  - o -

# x x x  o - -  - x x
# - - -  x x x  - o o
# - o o  o o -  o - -

# x - x  - - -  - - -
# - o -  - - -  - x -
# - - -  - - -  - - -
# ==================================
# =========== Block Status =========
# x - -
# x x -
# - - -
# ==================================

# Max depth is = 4
# Player 1 made the move: (6, 6) with x
# =========== Game Board ===========
# x x x  - o -  o o -
# - - -  - x -  o - -
# - - -  - - o  - o -

# x x x  o - -  - x x
# - - -  x x x  - o o
# - o o  o o -  o - -

# x - x  - - -  x - -
# - o -  - - -  - x -
# - - -  - - -  - - -
# ==================================
# =========== Block Status =========
# x - -
# x x -
# - - -
# ==================================

# Player 2 made the move: (2, 3) with o
# =========== Game Board ===========
# x x x  - o -  o o -
# - - -  - x -  o - -
# - - -  o - o  - o -

# x x x  o - -  - x x
# - - -  x x x  - o o
# - o o  o o -  o - -

# x - x  - - -  x - -
# - o -  - - -  - x -
# - - -  - - -  - - -
# ==================================
# =========== Block Status =========
# x - -
# x x -
# - - -
# ==================================

# Max depth is = 4
# Player 1 made the move: (8, 3) with x
# =========== Game Board ===========
# x x x  - o -  o o -
# - - -  - x -  o - -
# - - -  o - o  - o -

# x x x  o - -  - x x
# - - -  x x x  - o o
# - o o  o o -  o - -

# x - x  - - -  x - -
# - o -  - - -  - x -
# - - -  x - -  - - -
# ==================================
# =========== Block Status =========
# x - -
# x x -
# - - -
# ==================================

# Player 2 made the move: (8, 5) with o
# =========== Game Board ===========
# x x x  - o -  o o -
# - - -  - x -  o - -
# - - -  o - o  - o -

# x x x  o - -  - x x
# - - -  x x x  - o o
# - o o  o o -  o - -

# x - x  - - -  x - -
# - o -  - - -  - x -
# - - -  x - o  - - -
# ==================================
# =========== Block Status =========
# x - -
# x x -
# - - -
# ==================================

# Max depth is = 4
# Player 1 made the move: (6, 4) with x
# =========== Game Board ===========
# x x x  - o -  o o -
# - - -  - x -  o - -
# - - -  o - o  - o -

# x x x  o - -  - x x
# - - -  x x x  - o o
# - o o  o o -  o - -

# x - x  - x -  x - -
# - o -  - - -  - x -
# - - -  x - o  - - -
# ==================================
# =========== Block Status =========
# x - -
# x x -
# - - -
# ==================================

# Player 2 made the move: (2, 8) with o
# =========== Game Board ===========
# x x x  - o -  o o -
# - - -  - x -  o - -
# - - -  o - o  - o o

# x x x  o - -  - x x
# - - -  x x x  - o o
# - o o  o o -  o - -

# x - x  - x -  x - -
# - o -  - - -  - x -
# - - -  x - o  - - -
# ==================================
# =========== Block Status =========
# x - -
# x x -
# - - -
# ==================================

# Max depth is = 4
# Player 1 made the move: (6, 3) with x
# =========== Game Board ===========
# x x x  - o -  o o -
# - - -  - x -  o - -
# - - -  o - o  - o o

# x x x  o - -  - x x
# - - -  x x x  - o o
# - o o  o o -  o - -

# x - x  x x -  x - -
# - o -  - - -  - x -
# - - -  x - o  - - -
# ==================================
# =========== Block Status =========
# x - -
# x x -
# - - -
# ==================================

# Player 2 made the move: (0, 5) with o
# =========== Game Board ===========
# x x x  - o o  o o -
# - - -  - x -  o - -
# - - -  o - o  - o o

# x x x  o - -  - x x
# - - -  x x x  - o o
# - o o  o o -  o - -

# x - x  x x -  x - -
# - o -  - - -  - x -
# - - -  x - o  - - -
# ==================================
# =========== Block Status =========
# x - -
# x x -
# - - -
# ==================================

# Max depth is = 4
# Player 1 made the move: (1, 5) with x
# =========== Game Board ===========
# x x x  - o o  o o -
# - - -  - x x  o - -
# - - -  o - o  - o o

# x x x  o - -  - x x
# - - -  x x x  - o o
# - o o  o o -  o - -

# x - x  x x -  x - -
# - o -  - - -  - x -
# - - -  x - o  - - -
# ==================================
# =========== Block Status =========
# x - -
# x x -
# - - -
# ==================================

# Player 2 made the move: (1, 8) with o
# =========== Game Board ===========
# x x x  - o o  o o -
# - - -  - x x  o - o
# - - -  o - o  - o o

# x x x  o - -  - x x
# - - -  x x x  - o o
# - o o  o o -  o - -

# x - x  x x -  x - -
# - o -  - - -  - x -
# - - -  x - o  - - -
# ==================================
# =========== Block Status =========
# x - -
# x x -
# - - -
# ==================================

# Max depth is = 4
# Player 1 made the move: (2, 6) with x
# =========== Game Board ===========
# x x x  - o o  o o -
# - - -  - x x  o - o
# - - -  o - o  x o o

# x x x  o - -  - x x
# - - -  x x x  - o o
# - o o  o o -  o - -

# x - x  x x -  x - -
# - o -  - - -  - x -
# - - -  x - o  - - -
# ==================================
# =========== Block Status =========
# x - -
# x x -
# - - -
# ==================================

# Player 2 made the move: (7, 3) with o
# =========== Game Board ===========
# x x x  - o o  o o -
# - - -  - x x  o - o
# - - -  o - o  x o o

# x x x  o - -  - x x
# - - -  x x x  - o o
# - o o  o o -  o - -

# x - x  x x -  x - -
# - o -  o - -  - x -
# - - -  x - o  - - -
# ==================================
# =========== Block Status =========
# x - -
# x x -
# - - -
# ==================================

# Max depth is = 4
# Player 1 made the move: (8, 0) with x
# =========== Game Board ===========
# x x x  - o o  o o -
# - - -  - x x  o - o
# - - -  o - o  x o o

# x x x  o - -  - x x
# - - -  x x x  - o o
# - o o  o o -  o - -

# x - x  x x -  x - -
# - o -  o - -  - x -
# x - -  x - o  - - -
# ==================================
# =========== Block Status =========
# x - -
# x x -
# - - -
# ==================================

# Player 2 made the move: (7, 5) with o
# =========== Game Board ===========
# x x x  - o o  o o -
# - - -  - x x  o - o
# - - -  o - o  x o o

# x x x  o - -  - x x
# - - -  x x x  - o o
# - o o  o o -  o - -

# x - x  x x -  x - -
# - o -  o - o  - x -
# x - -  x - o  - - -
# ==================================
# =========== Block Status =========
# x - -
# x x -
# - - -
# ==================================

# Max depth is = 4
# Player 1 made the move: (8, 6) with x
# =========== Game Board ===========
# x x x  - o o  o o -
# - - -  - x x  o - o
# - - -  o - o  x o o

# x x x  o - -  - x x
# - - -  x x x  - o o
# - o o  o o -  o - -

# x - x  x x -  x - -
# - o -  o - o  - x -
# x - -  x - o  x - -
# ==================================
# =========== Block Status =========
# x - -
# x x -
# - - -
# ==================================

# Player 2 made the move: (6, 5) with o
# =========== Game Board ===========
# x x x  - o o  o o -
# - - -  - x x  o - o
# - - -  o - o  x o o

# x x x  o - -  - x x
# - - -  x x x  - o o
# - o o  o o -  o - -

# x - x  x x o  x - -
# - o -  o - o  - x -
# x - -  x - o  x - -
# ==================================
# =========== Block Status =========
# x - -
# x x -
# - o -
# ==================================

# Max depth is = 5
# Player 1 made the move: (0, 3) with x
# =========== Game Board ===========
# x x x  x o o  o o -
# - - -  - x x  o - o
# - - -  o - o  x o o

# x x x  o - -  - x x
# - - -  x x x  - o o
# - o o  o o -  o - -

# x - x  x x o  x - -
# - o -  o - o  - x -
# x - -  x - o  x - -
# ==================================
# =========== Block Status =========
# x - -
# x x -
# - o -
# ==================================

# Player 2 made the move: (2, 4) with o
# =========== Game Board ===========
# x x x  x o o  o o -
# - - -  - x x  o - o
# - - -  o o o  x o o

# x x x  o - -  - x x
# - - -  x x x  - o o
# - o o  o o -  o - -

# x - x  x x o  x - -
# - o -  o - o  - x -
# x - -  x - o  x - -
# ==================================
# =========== Block Status =========
# x o -
# x x -
# - o -
# ==================================

# Max depth is = 5
# Player 1 made the move: (6, 1) with x
# =========== Game Board ===========
# x x x  x o o  o o -
# - - -  - x x  o - o
# - - -  o o o  x o o

# x x x  o - -  - x x
# - - -  x x x  - o o
# - o o  o o -  o - -

# x x x  x x o  x - -
# - o -  o - o  - x -
# x - -  x - o  x - -
# ==================================
# =========== Block Status =========
# x o -
# x x -
# x o -
# ==================================

# P1
# COMPLETE






















        



