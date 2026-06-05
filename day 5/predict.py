import pickle
import numpy as np

with open("diabetes_model.pkl","rb") as file:
    model=pickle.load(file)

cases=[
    [150,35,45,90],
    [95,22,25,70],
    [180,40,55,100]
]

for case in cases:

    pred=model.predict([case])[0]

    prob=model.predict_proba([case])[0][1]

    print("\nInput:",case)

    print(
        "Prediction:",
        "Diabetic" if pred==1 else "Not Diabetic"
    )

    print(
        "Probability:",
        round(prob*100,2),
        "%"
    )