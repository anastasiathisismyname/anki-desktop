import tkinter as tk
import os
import pandas as pd
import random
from pprint import pprint
import time
import urllib.parse
import chardet
import sys
import os



class AnkiApp(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master, height=500, width=500)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(self, width=400, height=200, relief='raised')
        self.canvas.pack()
        self.thepath = "C:\\Users\\Anastasiia_Pyrih\\deutsch"
        self.font16 = "Century 16"
        self.font14 = "Century 14"
        self.font10 = "Candara 12"
        self.font11 = "Arial 7"
        self.filename = ""
        self.frames = {}
        self.files = self.get_files()

        for F in (StartPage, PageOne):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def get_files(self):

        all_words_df = pd.DataFrame()
        files = []
        for (paths, thedirs, filenames) in os.walk(self.thepath):
            files = files + filenames
            # for csvfile in filenames:
                # print(f"csvfile: {csvfile}")
                # with open(f"{self.thepath}\\{csvfile}", 'rb') as f:
                #     result = chardet.detect(f.read())
                # df = pd.read_csv(f"{self.thepath}\\{csvfile}", encoding=result['encoding'])
                # print(f"df['encoding']: {result['encoding']}")
                # all_words_df = all_words_df.append(df)

        # all_words_df.to_csv(f"{self.thepath}\\all_words.csv", index=False)

        # files = files + ["all_words.csv"]

        return files


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        for file in controller.files:
            controller.filename = file
            self.button = tk.Button(self, text=file, font=controller.font10, fg="IndianRed",
                                    command=lambda: controller.show_frame("PageOne"))
            self.button.pack()


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        self.deutsch_csv = pd.read_csv(f"{controller.thepath}\\{controller.filename}")
        self.question_words = self.deutsch_csv["russ"].tolist()
        self.question = random.choice(self.question_words)
        self.correct_answer = self.deutsch_csv.loc[self.deutsch_csv["russ"] == self.question, "deutsch"].item()

        self.answer_label = tk.Label(self, text="", font=controller.font14)

        self.question_label = tk.Label(self, text=self.question, font=controller.font16)
        self.question_label.pack()

        self.entry = tk.Entry(self)
        self.entry.pack()

        self.hint_label = tk.Label(self, text="Input your answer and press ENTER to submit your answer.",
                                   font=controller.font11)
        self.hint_label.pack()

        controller.master.bind("<Return>", lambda event=None: self.submit())
        controller.master.bind("<Right>", lambda event=None: self.on_next())

        button = tk.Button(self, text="Go to the start page",
                           command=lambda: self.back_to_main_screen())
        button.pack()

    def back_to_main_screen(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)
        self.controller.show_frame("StartPage")

    def on_next(self):
        self.entry.delete(0, 'end')
        self.hint_label["text"] = "Press ENTER to submit your answer."
        self.answer_label['text'] = ""
        self.question = self.get_question()
        self.question_label['text'] = self.question
        self.correct_answer = self.deutsch_csv.loc[self.deutsch_csv["russ"] == self.question, "deutsch"].item()

    def get_question(self):
        return random.choice(self.question_words)

    def submit(self):
        print("submit button clicked")
        answer_input = self.entry.get()
        answer_feedback, color = self.get_answer_text(answer_input)
        self.answer_label['text'] = answer_feedback
        self.answer_label.configure(foreground=color)
        self.answer_label.pack()
        self.hint_label['text'] = "Press 'Move Right' button to the next question"

    def get_answer_text(self, answer):
        if answer.lower() == self.correct_answer.lower():
            print(f"{answer} & {self.correct_answer}")
            try:
                self.question_words.remove(self.question)
                return f"Ja. '{answer}' ist richtig!", "green"
            except IndexError:
                return "Herzlichen Glückwunsch! Du hast alle Wörter gelernt!", "blue"
        else:
            return f"Nein. '{answer}' ist falsh. \nRichtig ist: {self.correct_answer}", "red"


def main():
    root = tk.Tk()
    root.title("My Anki app")
    root.iconbitmap("Spring.ico")
    AnkiApp(root).pack(expand=True, fill='both')
    root.mainloop()


if __name__ == "__main__":
    main()