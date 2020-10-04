import tkinter as tk
import os
import pandas as pd
import random
from pprint import pprint
import time


class StartPage(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master, height=500, width=500)

        self.font16 = "Century 16"
        self.font14 = "Century 14"
        self.font10 = "Candara 12"
        self.font11 = "Arial 7"

        self.thepath = "C:\\Users\\Anastasiia_Pyrih\\deutsch"
        self.files = self.get_files()

        self.canvas = tk.Canvas(self, width=400, height=600, relief='raised')
        self.canvas.pack()

        self.answer_label = tk.Label(self, text="", font=self.font14)

        self.filename = ""
        self.correct_answer = ""

        master.bind("<Return>", lambda event=None: self.submit())
        master.bind("<Right>", lambda event=None: self.on_next())

        self.deutsch_csv = ""
        self.question_words = []
        self.question = ""
        self.answer = ""

        self.file_buttons = []
        move = 0
        for file in self.files:
            self.button = tk.Button(self, text=file, font=self.font10, fg="IndianRed",
                                    command=lambda: self.start_training(file))
            self.button.pack()

            self.canvas.create_window(200, 90 + move, window=self.button)
            move += 40
            self.file_buttons.append(self.button)

    def get_question(self, filename):
        if filename != "all_words.csv":
            print(f"C:\\Users\\Anastasiia_Pyrih\\deutsch\\{filename}")
            deutsch_csv = pd.read_csv(f"C:\\Users\\Anastasiia_Pyrih\\deutsch\\{filename}")
            question_words = deutsch_csv["russ"].tolist()
            question = random.choice(question_words)
            correct_answer = deutsch_csv.loc[deutsch_csv["russ"] == question, "deutsch"].item()
            return question, correct_answer
        else:
            return None, None


    def start_training(self, filename):
        for button in self.file_buttons:
            button.lower()

        self.filename = filename

        question, correct_answer = self.get_question(filename)

        self.question_label = tk.Label(self, text=question, font=self.font16)

        self.question_label.pack()

        self.entry = tk.Entry(self).pack()

        self.canvas.create_window(200, 200, window=self.entry)

        self.hint_label = tk.Label(self, text="Input your answer and press ENTER to submit your answer.",
                                   font=self.font11)
        self.hint_label.pack()

        self.canvas.create_window(200, 350, window=self.hint_label)
        self.canvas.create_window(200, 150, window=self.question_label)

    def get_files(self):
        files = []
        for (paths, thedirs, filenames) in os.walk(self.thepath):
            files = files + filenames
        files = files + ["all_words.csv"]
        return files
    #
    # def on_next(self):
    #     self.entry.delete(0, 'end')
    #     self.hint_label["text"] = "Press ENTER to submit your answer."
    #     self.answer_label['text'] = ""
    #     self.question = self.get_question(self.filename)
    #     self.question_label['text'] = self.question
    #     self.correct_answer = self.deutsch_csv.loc[self.deutsch_csv["russ"] == self.question, "deutsch"].item()
    #
    # def submit(self):
    #     print("submit button clicked")
    #     self.answer = self.entry.get()
    #     answer, color = self.get_answer_text(self.answer)
    #     self.answer_label['text'] = answer
    #     self.answer_label.configure(foreground=color)
    #     self.answer_label.pack()
    #     self.canvas.create_window(200, 250, window=self.answer_label)
    #     self.hint_label['text'] = "Press 'Move Right' button to the next question"
    #
    # def get_answer_text(self, answer):
    #     if answer.lower() == self.correct_answer.lower():
    #         print(f"{answer} & {self.correct_answer}")
    #         try:
    #             self.question_words.remove(self.question)
    #             return f"Ja. '{answer}' ist richtig!", "green"
    #         except IndexError:
    #             return "Herzlichen Glückwunsch! Du hast alle Wörter gelernt!", "blue"
    #     else:
    #         return f"Nein. '{answer}' ist falsh. \nRichtig ist: {self.correct_answer}", "red"
    #

def main():
    root = tk.Tk()
    root.title("My Anki app")
    root.iconbitmap("Spring.ico")
    StartPage(root).pack(expand=True, fill='both')
    root.mainloop()


if __name__ == "__main__":
    main()