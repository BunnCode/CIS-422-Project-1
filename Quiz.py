from tkinter import *
import tkinter as tk
LARGE_FONT = ("Verdana", 12)


class SelfQuiz(tk.Tk):

    def __init__(self, *args, **kwargs):
        """
        Args:
            *args:
            **kwargs:
        """
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=10)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, MakeQuestionsPage, QuestionPage, AnswerPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Self Quiz", font=LARGE_FONT)
        label.pack(pady=50, padx=50)

        button1 = tk.Button(self, text="Create Questions", fg="red", command=lambda: controller.show_frame(MakeQuestionsPage))
        button1.pack()
        button2 = tk.Button(self, text="Quiz Yourself", fg="blue", command=lambda: controller.show_frame(QuestionPage))
        button2.pack()


class MakeQuestionsPage(tk.Frame):
    questions = ["What color is an apple?"]
    answers = ["Red"]

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Create Questions", font=LARGE_FONT)
        label.pack(pady=100, padx=100)

        button1 = tk.Button(self, text="Back to Menu", command=lambda: controller.show_frame(StartPage))
        button1.pack()
        """
        button2 = tk.Button(self, text="Quiz Yourself", fg="blue", command=lambda: controller.show_frame(PageTwo))
        button2.pack()
        """

        def button_command():
            text_1 = entry1.get()
            text_2 = entry2.get()
            MakeQuestionsPage.questions.append(text_1)
            MakeQuestionsPage.answers.append(text_2)
            print(MakeQuestionsPage.questions)
            print(MakeQuestionsPage.answers)
            return None

        entry1 = Entry(label, width=40)
        entry1.pack()
        entry2 = Entry(label, width=40)
        entry2.pack()

        Button(label, text="Enter", command=button_command).pack()


class QuestionPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text=MakeQuestionsPage.questions[AnswerPage.question_num], font=LARGE_FONT)
        label.pack(pady=100, padx=100)
        button1 = tk.Button(self, text="Check", fg="red", command=lambda: controller.show_frame(AnswerPage))
        button1.pack()
        button2 = tk.Button(self, text="Back to Menu", command=lambda: controller.show_frame(StartPage))
        button2.pack()

        """
        def display_prompt():
            label = tk.Label(self, text=PageOne.questions[PageThree.question_num], font=LARGE_FONT)
            label.pack(pady=100, padx=100)
            return None

        while len(PageOne.questions) != 0:
            display_prompt()
        """


class AnswerPage(tk.Frame):
    score = 0
    question_num = 0
    answer_num = 0

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text=MakeQuestionsPage.answers[AnswerPage.answer_num], font=LARGE_FONT)
        label.pack(pady=100, padx=100)

        def correct_score():
            AnswerPage.score += 1
            AnswerPage.question_num += 1
            print(AnswerPage.score)

        def wrong_score():
            AnswerPage.score -= 1
            AnswerPage.question_num += 1
            print(AnswerPage.score)

        def final_score():
            if len(MakeQuestionsPage.questions) + 1 > len(MakeQuestionsPage.questions):
                print("You got " + str(AnswerPage.score) + "/" + str(len(MakeQuestionsPage.questions)) + " correct")

        final_score()

        button1 = tk.Button(self, text="Correct", fg="red", command=correct_score)
        button1.pack()
        button2 = tk.Button(self, text="Wrong", fg="red", command=wrong_score)
        button2.pack()
        button3 = tk.Button(self, text="Next Question", command=lambda: controller.show_frame(QuestionPage))
        button3.pack()
        button4 = tk.Button(self, text="Back to Menu", command=lambda: controller.show_frame(StartPage))
        button4.pack()


app = SelfQuiz()
app.mainloop()
