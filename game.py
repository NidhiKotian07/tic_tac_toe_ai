import numpy as np
import pickle

# load trained model
model = pickle.load(open("model.pkl", "rb"))

board = [" " for _ in range(9)]

def print_board():
    print()
    print(board[0], "|", board[1], "|", board[2])
    print("--+---+--")
    print(board[3], "|", board[4], "|", board[5])
    print("--+---+--")
    print(board[6], "|", board[7], "|", board[8])
    print()

def encode_board(b):
    mapping = {"X":1, "O":-1, " ":0}
    return [mapping[i] for i in b]

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

    board[best_move] = "X"

def check_winner(p):
    wins = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]

    for combo in wins:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] == p:
            return True

    return False

def play():
    print("Tic Tac Toe")
    print("You = O | AI = X")

    while True:
        print_board()

        move = int(input("Enter position (1-9): ")) - 1

        if board[move] != " ":
            print("Invalid move")
            continue

        board[move] = "O"

        if check_winner("O"):
            print_board()
            print("You win!")
            break

        if " " not in board:
            print_board()
            print("Draw!")
            break

        ai_move()

        if check_winner("X"):
            print_board()
            print("AI wins!")
            break

play()