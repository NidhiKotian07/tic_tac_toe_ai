import tkinter as tk
from tkinter import messagebox
import numpy as np
import pickle
import math

# load ML model
model = pickle.load(open("model.pkl","rb"))

board = [" " for _ in range(9)]
ai_mode = "ML"

player_score = 0
ai_score = 0

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


# -------- ML MOVE --------

def ml_move():

    best_move = None
    best_score = -1

    for i in range(9):

        if board[i] == " ":

            board[i] = "X"

            encoded = np.array(encode_board(board)).reshape(1,-1)
            score = model.predict_proba(encoded)[0][1]

            board[i] = " "

            if score > best_score:
                best_score = score
                best_move = i

    return best_move


# -------- MINIMAX --------

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


# -------- AI MOVE --------

def ai_move():

    if ai_mode == "ML":
        move = ml_move()
    else:
        move = minimax_move()

    if move is not None:

        board[move] = "X"
        buttons[move]["text"] = "X"
        buttons[move]["fg"] = "#ff4d4d"

        if check_winner("X"):

            global ai_score
            ai_score += 1
            update_score()

            messagebox.showinfo("Game Over","AI Wins!")
            reset()


# -------- PLAYER CLICK --------

def click(i):

    if board[i] == " ":

        board[i] = "O"

        buttons[i]["text"] = "O"
        buttons[i]["fg"] = "#4dff88"

        if check_winner("O"):

            global player_score
            player_score += 1
            update_score()

            messagebox.showinfo("Game Over","You Win!")
            reset()

            return

        root.after(400, ai_move)


# -------- RESET --------

def reset():

    global board
    board = [" " for _ in range(9)]

    for b in buttons:
        b["text"] = " "
        b["fg"] = "white"


# -------- SCORE UPDATE --------

def update_score():

    score_label.config(
        text=f"Player: {player_score}    AI: {ai_score}"
    )


# -------- AI MODE --------

def set_ai(mode):

    global ai_mode
    ai_mode = mode

    status.config(text="AI Mode: "+mode)


# -------- GUI --------

root = tk.Tk()
root.title("AI Tic Tac Toe")
root.geometry("420x520")
root.configure(bg="#1a1a1a")

title = tk.Label(
    root,
    text="AI Tic Tac Toe",
    font=("Arial",22,"bold"),
    fg="white",
    bg="#1a1a1a"
)

title.pack(pady=10)

frame = tk.Frame(root,bg="#1a1a1a")
frame.pack()

buttons = []

for i in range(9):

    btn = tk.Button(
        frame,
        text=" ",
        font=("Arial",28,"bold"),
        width=4,
        height=2,
        bg="#2c3e50",
        fg="white",
        command=lambda i=i: click(i)
    )

    btn.grid(row=i//3,column=i%3,padx=5,pady=5)

    buttons.append(btn)


score_label = tk.Label(
    root,
    text="Player: 0    AI: 0",
    font=("Arial",14),
    fg="white",
    bg="#1a1a1a"
)

score_label.pack(pady=10)


status = tk.Label(
    root,
    text="Select AI Mode",
    font=("Arial",12),
    fg="white",
    bg="#1a1a1a"
)

status.pack()


control_frame = tk.Frame(root,bg="#1a1a1a")
control_frame.pack(pady=10)


ml_btn = tk.Button(
    control_frame,
    text="ML AI",
    width=10,
    command=lambda:set_ai("ML")
)

ml_btn.grid(row=0,column=0,padx=5)


minimax_btn = tk.Button(
    control_frame,
    text="Minimax AI",
    width=10,
    command=lambda:set_ai("MINIMAX")
)

minimax_btn.grid(row=0,column=1,padx=5)


reset_btn = tk.Button(
    control_frame,
    text="Reset",
    width=10,
    command=reset
)

reset_btn.grid(row=0,column=2,padx=5)


root.mainloop()