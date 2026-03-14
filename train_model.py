import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import pickle

# load dataset
data = pd.read_csv("tic_tac_toe.csv")

# convert text to numbers
mapping = {"x":1, "o":-1, "b":0, "positive":1, "negative":0}
data = data.replace(mapping)

# split features and labels
X = data.iloc[:, :-1]
y = data.iloc[:, -1]

# split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# train model
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# evaluate model
pred = model.predict(X_test)
accuracy = accuracy_score(y_test, pred)

print("Model Accuracy:", accuracy)

# save model
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model saved successfully!")