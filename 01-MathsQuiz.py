import tkinter as tk
from tkinter import messagebox
import random

class MathsQuiz:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Maths Quiz")
        self.window.configure(bg = '#ffe6f2')
        self.window.geometry("500x400")

        # Styling
        self.title_font = ("Comic Sans MS", 16, "bold")
        self.normal_font = ("Arial", 12)
        self.button_font = ("Arial", 10, "bold")

        self.score = 0
        self.current_question = 0
        self.total_questions = 10
        self.difficulty = None
        self.attemps = 0

        self.setup_widgets()
        self.displayMenu()

    def setup_widgets(self):
        # Main frame
        self.main_frame = tk.Frame(
            self.window, 
            bg = '#ffe6f2'
            )
        self.main_frame.pack(
            expand = True, 
            fill = 'both', 
            padx = 20, 
            pady = 20
            )

        # Title label
        self.title_label = tk.Label(
            self.main_frame, 
            text = "⊹ ࣪ ˖ Math Quiz ⊹ ࣪ ˖", 
            font = self.title_font, 
            bg = '#ffb6e1', 
            fg = '#8b008b', 
            padx = 20, 
            pady = 10
            )
        self.title_label.pack(fill = 'x', pady = (0, 20))

        # Question label
        self.question_label = tk.Label(
            self.main_frame, 
            text = "", 
            font = self.normal_font, 
            bg = '#ffe6f2', 
            fg = '#c71585'
            )
        self.question_label.pack(pady = 10)

        # Answer entry
        self.answer_entry = tk.Entry(
            self.main_frame, 
            font = self.normal_font, 
            bg = '#fff0f5', 
            fg = '#8b008b', 
            width = 20
            )
        self.answer_entry.pack(pady = 10)

        # Submit button
        self.submit_btn = tk.Button(
            self.main_frame, 
            text = "Submit Answer", 
            font = self.button_font, 
            bg = '#ff69b4', 
            fg = '#c71585', 
            activebackground = '#ff1493',
            command = self.check_answer
            )
        self.submit_btn.pack(pady = 10)

        # Score label
        self.score_label = tk.Label(
            self.main_frame, 
            text = "Score: 0", 
            font = self.normal_font, 
            bg = '#ffe6f2', 
            fg = '#c71585'
            )
        self.score_label.pack(pady = 10)

        # Difficulty buttons frame
        self.diff_frame = tk.Frame(
            self.main_frame, 
            bg = '#ffe6f2'
            )
        
    def displayMenu(self):
        self.question_label.config(text = "DIFFICULTY LEVEL")

        # Remove existing widgets from diff_frame
        for widget in self.diff_frame.winfo_children():
            widget.destroy()

        self.diff_frame.pack(pady = 20)

        # Difficulty buttons
        easy_btn = tk.Button(
            self.diff_frame, 
            text = "₊˚⊹ 1. Easy", 
            font = self.button_font, 
            bg = '#ffb6c1', 
            fg = '#8b008b', 
            command = lambda: self.set_difficulty("easy")
            )
        easy_btn.pack(pady = 5, fill = 'x')

        moderate_btn = tk.Button(
            self.diff_frame, 
            text = "⋆˚࿔ 2. Moderate", 
            font = self.button_font, 
            bg = '#ff69b4', 
            fg = '#8b008b', 
            command = lambda: self.set_difficulty("moderate")
            )
        moderate_btn.pack(pady = 5, fill = 'x')

        advanced_btn = tk.Button(
            self.diff_frame, 
            text = "ᰔ 3. Advanced", 
            font = self.button_font, 
            bg = '#ff6b95', 
            fg = '#8b008b', 
            command = lambda: self.set_difficulty("advanced")
            )
        advanced_btn.pack(pady = 5, fill = 'x')

        # Hide submit button and entry in menu
        self.answer_entry.pack_forget()
        self.submit_btn.pack_forget()
        self.score_label.pack_forget()

    def set_difficulty(self, level):
        self.difficulty = level
        self.diff_frame.pack_forget()
        self.answer_entry.pack(pady = 10)
        self.submit_btn.pack(pady = 10)
        self.score_label.pack(pady = 10)
        self.next_question()

    def randomInt(self):
        if self.difficulty == "easy":
            return random.randint(0, 9)
        elif self.difficulty == "moderate":
            return random.randint(10, 99)
        else:  # advanced
            return random.randint(1000, 9999)

    def decideOperation(self):
        return '+' if random.randint(0, 1) == 0 else '-'

    def displayProblem(self):
        self.num1 = self.randomInt()
        self.num2 = self.randomInt()
        self.operation = self.decideOperation()

        # Make sure we don't get negative results for subtraction
        if self.operation == '-' and self.num1 < self.num2:
            self.num1, self.num2 = self.num2, self.num1

        question_text = f"Question {self.current_question + 1}: {self.num1} {self.operation} {self.num2} = ?"
        self.question_label.config(text = question_text)
        self.answer_entry.delete(0, tk.END)
        self.attemps = 0

    def isCorrect(self, user_answer):
        try:
            if self.operation == '+':
                correct_answer = self.num1 + self.num2
            else:
                correct_answer = self.num1 - self.num2
            return int(user_answer) == correct_answer
        except ValueError:
            return False

    def check_answer(self):
        user_answer = self.answer_entry.get()

        if self.isCorrect(user_answer):
            if self.attemps == 0:
                self.score += 10
                messagebox.showinfo("Correct! 𑣲", "Well done! +10 points")
            else: 
                self.score += 5
                messagebox.showinfo("Good! ⋆˚࿔", "Correct on second try! +5 points")
            self.next_question()
        else:
            self.attempts += 1
            if self.attempts == 1:
                messagebox.showwarning("Try again ₊˚⊹", "That's not quite right. One more attempt!")    
                self.answer_entry.delete(0, tk.END)
            else:
                if self.operation == '+':
                    correct_answer = self.num1 + self.num2
                else:
                    correct_answer = self.num1 - self.num2
                messagebox.showerror("Incorrect ૮ ․ ․ ྀིა", f"The correct answer was {correct_answer}")
                self.next_question()

    def next_question(self):
        self.current_question += 1
        self.score_label.config(text = f"Score: {self.score}")

        if self.current_question < self.total_questions:
            self.displayProblem()
        else:
            self.displayResults()

    def displayResults(self):
        grade = ""
        if self.score >= 90:
            grade = "A+ ⊹ ࣪ ˖ Excellent!"
        elif self.score >= 80:
            grade = "A ⋆˚࿔ Very Good!" 
        elif self.score >= 70:
            grade = "B 𑣲 Good Job!" 
        elif self.score >= 60:
            grade = "C ₊˚⊹ Okay!"
        else:
            grade = "D ᰔ Keep Practicing!" 

        result_text = f"Final Score: {self.score}/100\nGrade: {grade}"

        messagebox.showinfo("Quiz Completed ૮ ․ ․ ྀིა", result_text)

        play_again = messagebox.askyesno("Play Again?", "Would you like to play again?")
        if play_again:
            self.score = 0
            self.current_question = 0
            self.displayMenu()
        else:
            self.window.quit()

    def run(self):
        self.window.mainloop()

# Start the quiz
if __name__ == "__main__":
    quiz = MathsQuiz()
    quiz.run()