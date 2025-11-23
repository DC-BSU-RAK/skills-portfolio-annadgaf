# student_manager.py
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import os
import random

class AnimatedBackground(tk.Canvas):
    """Animated background with floating clouds and interactive elements"""
    
    def __init__(self, parent, width=1000, height=700):
        super().__init__(parent, width=width, height=height, highlightthickness=0)
        self.width = width
        self.height = height
        self.clouds = []
        self.particles = []
        self.mouse_x = width // 2
        self.mouse_y = height // 2
        
        # Create simple sky blue background
        self.configure(bg='#87CEEB')
        
        # Create initial clouds
        self.create_initial_clouds()
        
        # Create floating particles
        self.create_particles()
        
        # Bind mouse movement for interactivity
        self.bind("<Motion>", self.on_mouse_move)
        
        # Start animation
        self.animate()
    
    def create_initial_clouds(self):
        """Create initial cloud formations"""
        cloud_positions = [
            (100, 80, 200, 120), (400, 150, 550, 190),
            (200, 250, 350, 290), (600, 100, 750, 140),
            (50, 300, 180, 340), (500, 350, 650, 390)
        ]
        
        for x1, y1, x2, y2 in cloud_positions:
            cloud = {
                'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2,
                'dx': random.uniform(0.2, 0.5),
                'objects': []
            }
            self.create_cloud(cloud)
            self.clouds.append(cloud)
    
    def create_cloud(self, cloud):
        """Create a fluffy cloud"""
        x1, y1, x2, y2 = cloud['x1'], cloud['y1'], cloud['x2'], cloud['y2']
        width = x2 - x1
        height = y2 - y1
        
        # Create cloud as overlapping circles
        circles = [
            (x1 + width * 0.3, y1 + height * 0.5, height * 0.6),
            (x1 + width * 0.5, y1 + height * 0.3, height * 0.5),
            (x1 + width * 0.7, y1 + height * 0.5, height * 0.6),
            (x1 + width * 0.4, y1 + height * 0.7, height * 0.4),
            (x1 + width * 0.6, y1 + height * 0.7, height * 0.4)
        ]
        
        for cx, cy, r in circles:
            obj = self.create_oval(cx-r, cy-r, cx+r, cy+r, 
                                 fill='white', outline='', tags='cloud')
            cloud['objects'].append(obj)
    
    def create_particles(self):
        """Create floating particles"""
        for _ in range(20):
            particle = {
                'x': random.randint(0, self.width),
                'y': random.randint(0, self.height),
                'size': random.randint(2, 4),
                'dx': random.uniform(-0.3, 0.3),
                'dy': random.uniform(-0.3, 0.3),
                'object': None
            }
            particle['object'] = self.create_oval(
                particle['x'] - particle['size'],
                particle['y'] - particle['size'],
                particle['x'] + particle['size'],
                particle['y'] + particle['size'],
                fill='#E8F4FF', outline='', tags='particle'
            )
            self.particles.append(particle)
    
    def on_mouse_move(self, event):
        """Update mouse position for interactive elements"""
        self.mouse_x = event.x
        self.mouse_y = event.y
    
    def animate(self):
        """Animate background elements"""
        # Move clouds
        for cloud in self.clouds:
            cloud['x1'] += cloud['dx']
            cloud['x2'] += cloud['dx']
            
            # Reset cloud if it goes off screen
            if cloud['x1'] > self.width:
                cloud['x1'] = -150
                cloud['x2'] = cloud['x1'] + 150
            
            # Update cloud position
            for obj in cloud['objects']:
                self.move(obj, cloud['dx'], 0)
        
        # Move particles with mouse influence
        for particle in self.particles:
            # Calculate distance to mouse
            dx = self.mouse_x - particle['x']
            dy = self.mouse_y - particle['y']
            distance = (dx**2 + dy**2)**0.5
            
            # Add slight mouse attraction
            if distance < 100:
                particle['dx'] += dx * 0.0005
                particle['dy'] += dy * 0.0005
            
            # Apply velocity limits
            particle['dx'] = max(-1, min(1, particle['dx']))
            particle['dy'] = max(-1, min(1, particle['dy']))
            
            # Update position
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            
            # Bounce off walls
            if particle['x'] <= 0 or particle['x'] >= self.width:
                particle['dx'] *= -0.8
            if particle['y'] <= 0 or particle['y'] >= self.height:
                particle['dy'] *= -0.8
            
            # Keep particles in bounds
            particle['x'] = max(0, min(self.width, particle['x']))
            particle['y'] = max(0, min(self.height, particle['y']))
            
            # Update visual position
            self.coords(
                particle['object'],
                particle['x'] - particle['size'],
                particle['y'] - particle['size'],
                particle['x'] + particle['size'],
                particle['y'] + particle['size']
            )
        
        # Continue animation
        self.after(30, self.animate)

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
                messagebox.showerror("Error", f"File not found: {self.filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")
    
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
        # Create animated background
        self.background = AnimatedBackground(self.root, width=1000, height=700)
        self.background.pack(fill='both', expand=True)
        
        # Create main container
        self.main_frame = tk.Frame(self.background, bg='white', bd=2, relief='raised')
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
                          font=('Arial', 12), bg='#87CEEB', fg='#1E3A5F',  # Dark blue text
                          activebackground='#5F9EA0', activeforeground='#1E3A5F',
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
        
        # Fixed: Changed select button text to dark blue for visibility
        tk.Button(select_window, text="Select", command=on_select,
                 font=('Arial', 12), bg='#2E86AB', fg='#1E3A5F').pack(pady=10)
    
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