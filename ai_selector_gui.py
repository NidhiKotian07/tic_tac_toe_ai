import tkinter as tk
import numpy as np
import pickle
import math

model = pickle.load(open("model.pkl","rb"))

board = [" " for _ in range(9)]

ai_type = "ML"

def encode_board(b):
    mapping = {"X":1,"O":-1," ":0}
    return [mapping[i] for i in b]

def check_winner(player):

    wins = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]

    for combo in wins:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] == player:
            return True

    return False


# -------- ML AI --------

def ml_move():

    best_move = None
    best_score = -1

    for i in range(9):
        if board[i] == " ":
            board[i] = "X"

            encoded = np.array(encode_board(board)).reshape(1,-1)
            score = model.predict_proba(encoded)[0][1]

            if score > best_score:
                best_score = score
                best_move = i

            board[i] = " "

    return best_move


# -------- Minimax AI --------

def minimax(is_max):

    if check_winner("X"):
        return 1
    if check_winner("O"):
        return -1
    if " " not in board:
        return 0

    if is_max:

        best = -math.inf

        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                score = minimax(False)
                board[i] = " "
                best = max(best,score)

        return best

    else:

        best = math.inf

        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                score = minimax(True)
                board[i] = " "
                best = min(best,score)

        return best


def minimax_move():

    best_score = -math.inf
    best_move = None

    for i in range(9):
        if board[i] == " ":
            board[i] = "X"
            score = minimax(False)
            board[i] = " "

            if score > best_score:
                best_score = score
                best_move = i

    return best_move


# -------- AI move selector --------

def ai_move():

    if ai_type == "ML":
        move = ml_move()
    else:
        move = minimax_move()

    if move is not None:
        board[move] = "X"
        buttons[move]["text"] = "X"


# -------- player click --------

def click(i):

    if board[i] == " ":

        board[i] = "O"
        buttons[i]["text"] = "O"

        if check_winner("O"):
            status.config(text="You Win!")
            return

        ai_move()

        if check_winner("X"):
            status.config(text="AI Wins!")


# -------- reset board --------

def reset():

    global board
    board = [" " for _ in range(9)]

    for b in buttons:
        b["text"] = " "

    status.config(text="Game Reset")


# -------- AI selector --------

def set_ai(choice):

    global ai_type
    ai_type = choice

    status.config(text="AI Mode: " + choice)


# -------- GUI --------

root = tk.Tk()
root.title("AI Tic Tac Toe")

buttons = []

for i in range(9):

    btn = tk.Button(root,text=" ",font=("Arial",30),
                    width=5,height=2,
                    command=lambda i=i: click(i))

    btn.grid(row=i//3,column=i%3)
    buttons.append(btn)


status = tk.Label(root,text="Select AI Mode",font=("Arial",14))
status.grid(row=3,column=0,columnspan=3)

ml_button = tk.Button(root,text="ML AI",
                      command=lambda: set_ai("ML"))
ml_button.grid(row=4,column=0)

minimax_button = tk.Button(root,text="Minimax AI",
                           command=lambda: set_ai("MINIMAX"))
minimax_button.grid(row=4,column=1)

reset_button = tk.Button(root,text="Reset",
                         command=reset)
reset_button.grid(row=4,column=2)

root.mainloop()