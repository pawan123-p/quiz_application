import tkinter as tk
from tkinter import messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load questions from CSV
df = pd.read_csv("questions.csv")

# Shuffle the questions using numpy
df = df.sample(frac=1, random_state=np.random.randint(1000))

questions = df.values.tolist()
index = 0
score = 0
user_answers = []


# Load next question

def load_question():
    question, o1, o2, o3, o4, ans = questions[index]

    q_label.config(text=f"Q{index+1}: {question}")
    rb[0].config(text=o1)
    rb[1].config(text=o2)
    rb[2].config(text=o3)
    rb[3].config(text=o4)

    var.set(0)


# Submit current answer

def next_question():
    global index, score

    selected = var.get()
    if selected == 0:
        messagebox.showwarning("Warning", "Please select an option!")
        return

    correct_ans = questions[index][5]

    user_answers.append(selected)

    if selected == correct_ans:
        score += 1

    index += 1

    if index >= len(questions):
        finish_quiz()
    else:
        load_question()


# Show result + matplotlib graph

def finish_quiz():
    root.destroy()

    total = len(questions)
    wrong = total - score

    # Plot result
    plt.figure(figsize=(6,5))
    plt.pie([score, wrong], labels=["Correct", "Wrong"], autopct="%1.1f%%")
    plt.title("Quiz Result")
    plt.show()

    # Save performance in CSV
    result = pd.DataFrame({
        "Total Questions": [total],
        "Correct": [score],
        "Wrong": [wrong]
    })

    result.to_csv("quiz_result.csv", index=False)
    print("Result saved to quiz_result.csv")


# Tkinter Window

root = tk.Tk()
root.title("Quiz Application")
root.geometry("450x350")

var = tk.IntVar()

q_label = tk.Label(root, text="", font=("Arial", 14))
q_label.pack(pady=20)

rb = []
for i in range(4):
    r = tk.Radiobutton(root, text="", variable=var, value=i+1, font=("Arial", 12))
    r.pack(anchor="w", padx=30)
    rb.append(r)

next_btn = tk.Button(root, text="Next", command=next_question, font=("Arial", 12))
next_btn.pack(pady=20)

load_question()

root.mainloop()