import tkinter as tk
import numpy as np
import pickle

model = pickle.load(open("model.pkl", "rb"))

board = [" " for _ in range(9)]

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

def ai_move():
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

    if best_move is not None:
        board[best_move] = "X"
        buttons[best_move]["text"] = "X"

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

root = tk.Tk()
root.title("AI Tic Tac Toe")

buttons = []

for i in range(9):
    btn = tk.Button(root, text=" ", font=("Arial",30), width=5, height=2,
                    command=lambda i=i: click(i))
    btn.grid(row=i//3, column=i%3)
    buttons.append(btn)

status = tk.Label(root, text="You = O | AI = X", font=("Arial",14))
status.grid(row=3, column=0, columnspan=3)

root.mainloop()