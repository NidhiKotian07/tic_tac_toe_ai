import pandas as pd
import random

def check_x_win(board):
    win_positions = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]
    
    for pos in win_positions:
        if board[pos[0]] == board[pos[1]] == board[pos[2]] == "x":
            return True
    return False

values = ["x", "o", "b"]

data = []

for _ in range(5000):
    board = [random.choice(values) for _ in range(9)]

    if check_x_win(board):
        label = "positive"
    else:
        label = "negative"

    board.append(label)
    data.append(board)

columns = [
"top-left","top-middle","top-right",
"middle-left","middle-middle","middle-right",
"bottom-left","bottom-middle","bottom-right",
"class"
]

df = pd.DataFrame(data, columns=columns)

df.to_csv("tic_tac_toe.csv", index=False)

print("Dataset generated successfully!")