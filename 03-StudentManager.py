# student_manager.py
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import os
import random

class StudentManager:
    """Main Student Manager application"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Student Manager - Sky Analytics")
        self.root.geometry("1000x700")
        self.root.configure(bg='#87CEEB')
        
        # Initialize data with correct file path
        self.students = []
        self.filename = "Assessment 1 - Skills Portfolio/A1 - Resources/studentMarks.txt"
        
        # Load data
        self.load_data()
        
        # Setup GUI
        self.setup_gui()
    
    def load_data(self):
        """Load student data from file"""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as file:
                    lines = file.readlines()
                    if len(lines) > 0:
                        # Skip first line (student count)
                        for line in lines[1:]:
                            data = line.strip().split(',')
                            if len(data) >= 5:
                                student = {
                                    'code': int(data[0]),
                                    'name': data[1],
                                    'course_marks': [int(data[2]), int(data[3]), int(data[4])],
                                    'exam_mark': int(data[5])
                                }
                                self.students.append(student)
                print(f"Loaded {len(self.students)} students from {self.filename}")
            else:
                # Create sample data if file doesn't exist
                self.create_sample_data()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")
            self.create_sample_data()
    
    def create_sample_data(self):
        """Create sample data for demonstration"""
        sample_students = [
            [8439, "Jake Hobbs", 10, 11, 10, 43],
            [7562, "Emma Wilson", 15, 14, 16, 78],
            [9123, "Michael Brown", 12, 13, 11, 65],
            [6347, "Sarah Johnson", 18, 17, 19, 92],
            [5781, "David Lee", 8, 9, 7, 35]
        ]
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        
        with open(self.filename, 'w') as file:
            file.write(f"{len(sample_students)}\n")
            for student in sample_students:
                file.write(','.join(map(str, student)) + '\n')
        
        self.load_data()
    
    def calculate_percentage(self, student):
        """Calculate overall percentage"""
        total_coursework = sum(student['course_marks'])
        total_marks = total_coursework + student['exam_mark']
        return (total_marks / 160) * 100
    
    def calculate_grade(self, percentage):
        """Calculate grade based on percentage"""
        if percentage >= 70:
            return 'A'
        elif percentage >= 60:
            return 'B'
        elif percentage >= 50:
            return 'C'
        elif percentage >= 40:
            return 'D'
        else:
            return 'F'
    
    def setup_gui(self):
        """Setup the main GUI"""
        # Create main container
        self.main_frame = tk.Frame(self.root, bg='white', bd=2, relief='raised')
        self.main_frame.place(relx=0.5, rely=0.5, anchor='center', width=900, height=600)
        
        # Title
        title_label = tk.Label(self.main_frame, text="🎓 Student Manager", 
                              font=('Arial', 24, 'bold'), fg='#2E86AB', bg='white')
        title_label.pack(pady=20)
        
        # Create menu buttons
        self.create_menu_buttons()
        
        # Create output area
        self.create_output_area()
    
    def create_menu_buttons(self):
        """Create the main menu buttons"""
        button_frame = tk.Frame(self.main_frame, bg='white')
        button_frame.pack(pady=20)
        
        buttons = [
            ("📊 View All Students", self.view_all_students),
            ("👤 View Individual Student", self.view_individual_student),
            ("🏆 Highest Scoring Student", self.show_highest_scoring),
            ("📉 Lowest Scoring Student", self.show_lowest_scoring),
        ]
        
        # Create buttons in two columns
        for i, (text, command) in enumerate(buttons):
            btn = tk.Button(button_frame, text=text, command=command,
                          font=('Arial', 12), bg='#87CEEB', fg='white',
                          activebackground='#5F9EA0', activeforeground='white',
                          relief='raised', bd=3, width=25, height=2)
            btn.grid(row=i//2, column=i%2, padx=10, pady=8)
            
            # Add hover effects
            self.add_button_hover_effect(btn, '#87CEEB', '#5F9EA0')
    
    def add_button_hover_effect(self, button, normal_color, hover_color):
        """Add hover effect to buttons"""
        def on_enter(e):
            button['background'] = hover_color
            button['cursor'] = 'hand2'
        
        def on_leave(e):
            button['background'] = normal_color
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
    
    def create_output_area(self):
        """Create the output text area"""
        output_frame = tk.Frame(self.main_frame, bg='white')
        output_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        tk.Label(output_frame, text="Results:", font=('Arial', 14, 'bold'), 
                fg='#2E86AB', bg='white').pack(anchor='w')
        
        self.output_text = scrolledtext.ScrolledText(output_frame, 
                                                   font=('Consolas', 10),
                                                   bg='#F8F9FA', fg='#333333',
                                                   width=80, height=15)
        self.output_text.pack(fill='both', expand=True, pady=5)
    
    def clear_output(self):
        """Clear the output text area"""
        self.output_text.delete(1.0, tk.END)
    
    def display_output(self, text):
        """Display text in output area"""
        self.clear_output()
        self.output_text.insert(tk.END, text)
    
    def view_all_students(self):
        """Display all student records"""
        if not self.students:
            self.display_output("No student records found.")
            return
        
        output = "ALL STUDENT RECORDS\n"
        output += "=" * 80 + "\n\n"
        
        total_percentage = 0
        
        for student in self.students:
            percentage = self.calculate_percentage(student)
            total_percentage += percentage
            grade = self.calculate_grade(percentage)
            
            output += f"Name: {student['name']}\n"
            output += f"Student Code: {student['code']}\n"
            output += f"Coursework Marks: {student['course_marks']}\n"
            output += f"Exam Mark: {student['exam_mark']}\n"
            output += f"Overall Percentage: {percentage:.1f}%\n"
            output += f"Grade: {grade}\n"
            output += "-" * 40 + "\n"
        
        # Summary
        avg_percentage = total_percentage / len(self.students)
        output += f"\nSUMMARY:\n"
        output += f"Total Students: {len(self.students)}\n"
        output += f"Average Percentage: {avg_percentage:.1f}%\n"
        
        self.display_output(output)
    
    def view_individual_student(self):
        """View individual student record"""
        if not self.students:
            messagebox.showinfo("Info", "No student records found.")
            return
        
        # Create selection dialog
        self.create_student_selection_dialog("Select Student to View", self.display_individual_student)
    
    def create_student_selection_dialog(self, title, callback):
        """Create a dialog for selecting a student"""
        select_window = tk.Toplevel(self.root)
        select_window.title(title)
        select_window.geometry("400x300")
        select_window.configure(bg='#87CEEB')
        select_window.transient(self.root)
        select_window.grab_set()
        
        tk.Label(select_window, text=title, font=('Arial', 16, 'bold'), 
                bg='#87CEEB', fg='white').pack(pady=10)
        
        # Create listbox with scrollbar
        frame = tk.Frame(select_window, bg='#87CEEB')
        frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        listbox = tk.Listbox(frame, font=('Arial', 11), bg='white')
        scrollbar = tk.Scrollbar(frame, orient='vertical')
        
        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)
        
        # Populate listbox
        for student in self.students:
            listbox.insert(tk.END, f"{student['code']} - {student['name']}")
        
        listbox.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        def on_select():
            selection = listbox.curselection()
            if selection:
                selected_student = self.students[selection[0]]
                select_window.destroy()
                callback(selected_student)
        
        tk.Button(select_window, text="Select", command=on_select,
                 font=('Arial', 12), bg='#2E86AB', fg='white').pack(pady=10)
    
    def display_individual_student(self, student):
        """Display individual student record"""
        percentage = self.calculate_percentage(student)
        grade = self.calculate_grade(percentage)
        
        output = f"INDIVIDUAL STUDENT RECORD\n"
        output += "=" * 50 + "\n\n"
        output += f"Name: {student['name']}\n"
        output += f"Student Code: {student['code']}\n"
        output += f"Coursework Marks: {student['course_marks']}\n"
        output += f"Total Coursework: {sum(student['course_marks'])}/60\n"
        output += f"Exam Mark: {student['exam_mark']}/100\n"
        output += f"Overall Percentage: {percentage:.1f}%\n"
        output += f"Grade: {grade}\n"
        
        self.display_output(output)
    
    def show_highest_scoring(self):
        """Show student with highest overall mark"""
        if not self.students:
            messagebox.showinfo("Info", "No student records found.")
            return
        
        highest_student = max(self.students, key=self.calculate_percentage)
        self.display_individual_student(highest_student)
        
        # Add highlight
        current_text = self.output_text.get(1.0, tk.END)
        highlighted_text = "🏆 HIGHEST SCORING STUDENT 🏆\n\n" + current_text
        self.display_output(highlighted_text)
    
    def show_lowest_scoring(self):
        """Show student with lowest overall mark"""
        if not self.students:
            messagebox.showinfo("Info", "No student records found.")
            return
        
        lowest_student = min(self.students, key=self.calculate_percentage)
        self.display_individual_student(lowest_student)
        
        # Add highlight
        current_text = self.output_text.get(1.0, tk.END)
        highlighted_text = "📉 LOWEST SCORING STUDENT 📉\n\n" + current_text
        self.display_output(highlighted_text)

def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = StudentManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()