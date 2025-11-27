"""
Student Manager Application
A Tkinter-based GUI application for managing student records with animated background.

Features:
- Beautiful sky blue themed interface with animated background
- Floating clouds and interactive particles that respond to mouse movement
- Complete CRUD operations (Create, Read, Update, Delete) for student records
- Sorting functionality by percentage, name, or student code
- File persistence with studentMarks.txt integration
- Decorative borders and cute symbols for enhanced visual appeal
- Professional typography with Georgia font and bold styling
- Compact button layout to fit all functionality without cutoff
- Comprehensive error handling and user feedback

File Structure:
Assessment 1 - Skills Portfolio/
├── student_manager.py              # Main application file
└── A1 - Resources/
    └── studentMarks.txt            # Student database file

"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import os
import random

class AnimatedBackground(tk.Canvas):
    """
    Animated background canvas with floating clouds and interactive particles.
    
    This class creates a dynamic sky blue background with:
    - 6 floating cloud formations that move across the screen
    - 20 interactive particles that respond to mouse movement
    - Smooth animations running at 30fps for optimal performance
    - Mouse tracking for interactive particle behavior
    """
    
    def __init__(self, parent, width=1000, height=700):
        """
        Initialize the animated background.
        
        Args:
            parent: Parent widget for the canvas
            width (int): Canvas width in pixels
            height (int): Canvas height in pixels
        """
        super().__init__(parent, width=width, height=height, highlightthickness=0)
        self.width = width
        self.height = height
        self.clouds = []
        self.particles = []
        self.mouse_x = width // 2
        self.mouse_y = height // 2
        
        # Set sky blue background color
        self.configure(bg='#87CEEB')
        
        # Initialize visual elements
        self.create_initial_clouds()
        self.create_particles()
        
        # Bind mouse movement for interactive particles
        self.bind("<Motion>", self.on_mouse_move)
        
        # Start animation loop
        self.animate()
    
    def create_initial_clouds(self):
        """Create initial cloud formations at random positions."""
        cloud_positions = [
            (100, 80, 200, 120), (400, 150, 550, 190),
            (200, 250, 350, 290), (600, 100, 750, 140),
            (50, 300, 180, 340), (500, 350, 650, 390)
        ]
        
        for x1, y1, x2, y2 in cloud_positions:
            cloud = {
                'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2,
                'dx': random.uniform(0.2, 0.5),  # Cloud movement speed
                'objects': []  # Store cloud visual elements
            }
            self.create_cloud(cloud)
            self.clouds.append(cloud)
    
    def create_cloud(self, cloud):
        """
        Create a fluffy cloud using overlapping circles.
        
        Args:
            cloud (dict): Cloud properties including position and size
        """
        x1, y1, x2, y2 = cloud['x1'], cloud['y1'], cloud['x2'], cloud['y2']
        width = x2 - x1
        height = y2 - y1
        
        # Define circle positions for cloud shape
        circles = [
            (x1 + width * 0.3, y1 + height * 0.5, height * 0.6),
            (x1 + width * 0.5, y1 + height * 0.3, height * 0.5),
            (x1 + width * 0.7, y1 + height * 0.5, height * 0.6),
            (x1 + width * 0.4, y1 + height * 0.7, height * 0.4),
            (x1 + width * 0.6, y1 + height * 0.7, height * 0.4)
        ]
        
        # Create overlapping circles to form cloud
        for cx, cy, r in circles:
            obj = self.create_oval(cx-r, cy-r, cx+r, cy+r, 
                                 fill='white', outline='', tags='cloud')
            cloud['objects'].append(obj)
    
    def create_particles(self):
        """Create floating particles with random properties."""
        for _ in range(20):
            particle = {
                'x': random.randint(0, self.width),
                'y': random.randint(0, self.height),
                'size': random.randint(2, 4),
                'dx': random.uniform(-0.3, 0.3),
                'dy': random.uniform(-0.3, 0.3),
                'object': None
            }
            # Create visual representation of particle
            particle['object'] = self.create_oval(
                particle['x'] - particle['size'],
                particle['y'] - particle['size'],
                particle['x'] + particle['size'],
                particle['y'] + particle['size'],
                fill='#E8F4FF', outline='', tags='particle'
            )
            self.particles.append(particle)
    
    def on_mouse_move(self, event):
        """
        Track mouse position for interactive particles.
        
        Args:
            event: Mouse motion event
        """
        self.mouse_x = event.x
        self.mouse_y = event.y
    
    def animate(self):
        """Main animation loop for clouds and particles."""
        # Animate clouds
        for cloud in self.clouds:
            cloud['x1'] += cloud['dx']
            cloud['x2'] += cloud['dx']
            
            # Reset cloud position when it moves off screen
            if cloud['x1'] > self.width:
                cloud['x1'] = -150
                cloud['x2'] = cloud['x1'] + 150
            
            # Update cloud visual position
            for obj in cloud['objects']:
                self.move(obj, cloud['dx'], 0)
        
        # Animate particles with mouse interaction
        for particle in self.particles:
            # Calculate distance to mouse for interaction
            dx = self.mouse_x - particle['x']
            dy = self.mouse_y - particle['y']
            distance = (dx**2 + dy**2)**0.5
            
            # Add mouse attraction when close
            if distance < 100:
                particle['dx'] += dx * 0.0005
                particle['dy'] += dy * 0.0005
            
            # Limit particle velocity
            particle['dx'] = max(-1, min(1, particle['dx']))
            particle['dy'] = max(-1, min(1, particle['dy']))
            
            # Update particle position
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            
            # Bounce particles off screen edges
            if particle['x'] <= 0 or particle['x'] >= self.width:
                particle['dx'] *= -0.8
            if particle['y'] <= 0 or particle['y'] >= self.height:
                particle['dy'] *= -0.8
            
            # Keep particles within bounds
            particle['x'] = max(0, min(self.width, particle['x']))
            particle['y'] = max(0, min(self.height, particle['y']))
            
            # Update particle visual position
            self.coords(
                particle['object'],
                particle['x'] - particle['size'],
                particle['y'] - particle['size'],
                particle['x'] + particle['size'],
                particle['y'] + particle['size']
            )
        
        # Continue animation loop
        self.after(30, self.animate)

class StudentManager:
    """
    Main student management application class.
    
    Provides comprehensive student record management with:
    - File-based data persistence
    - GUI interface with animated background
    - Complete CRUD operations
    - Sorting and analysis features
    - Professional styling with decorative elements
    - Compact button layout to prevent cutoff
    """
    
    def __init__(self, root):
        """
        Initialize the Student Manager application.
        
        Args:
            root (tk.Tk): The main Tkinter root window
        """
        self.root = root
        self.root.title("Student Manager - Sky Analytics")
        self.root.geometry("1000x700")
        self.root.configure(bg='#87CEEB')
        
        # Initialize student data storage
        self.students = []
        self.filename = "Assessment 1 - Skills Portfolio/A1 - Resources/studentMarks.txt"
        
        # Load existing student data
        self.load_data()
        
        # Setup user interface
        self.setup_gui()
    
    def load_data(self):
        """Load student data from text file with error handling."""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as file:
                    lines = file.readlines()
                    if len(lines) > 0:
                        # Skip first line (student count) and process each student
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
    
    def save_data(self):
        """
        Save student data to text file.
        
        Returns:
            bool: True if save successful, False otherwise
        """
        try:
            with open(self.filename, 'w') as file:
                # Write student count header
                file.write(f"{len(self.students)}\n")
                # Write each student record
                for student in self.students:
                    course_marks = student['course_marks']
                    line = f"{student['code']},{student['name']},{course_marks[0]},{course_marks[1]},{course_marks[2]},{student['exam_mark']}\n"
                    file.write(line)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {str(e)}")
            return False
    
    def calculate_percentage(self, student):
        """
        Calculate overall percentage for a student.
        
        Args:
            student (dict): Student record dictionary
            
        Returns:
            float: Overall percentage (0-100)
        """
        total_coursework = sum(student['course_marks'])
        total_marks = total_coursework + student['exam_mark']
        return (total_marks / 160) * 100
    
    def calculate_grade(self, percentage):
        """
        Calculate letter grade based on percentage.
        
        Args:
            percentage (float): Student's overall percentage
            
        Returns:
            str: Letter grade (A-F)
        """
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
        """Initialize the main application interface."""
        # Create animated background
        self.background = AnimatedBackground(self.root, width=1000, height=700)
        self.background.pack(fill='both', expand=True)
        
        # Create main content container
        self.main_frame = tk.Frame(self.background, bg='white', bd=2, relief='raised')
        self.main_frame.place(relx=0.5, rely=0.5, anchor='center', width=800, height=500)
        
        # Application title with decorative symbols
        title_label = tk.Label(self.main_frame, text="⋆˚✿˖° Student Manager ᯓ★", 
                              font=('Comic Sans MS', 22, 'bold'), fg='#2E86AB', bg='white')
        title_label.pack(pady=15)
        
        # Create interface components
        self.create_menu_buttons()
        self.create_output_area()
    
    def create_menu_buttons(self):
        """Create the main menu button grid with compact layout."""
        button_frame = tk.Frame(self.main_frame, bg='white')
        button_frame.pack(pady=10)
        
        # Define menu buttons with symbols and commands - using shorter text
        buttons = [
            ("⊹ View All", self.view_all_students),
            ("❀ View Student", self.view_individual_student),
            ("ᯓ Highest", self.show_highest_scoring),
            ("✿ Lowest", self.show_lowest_scoring),
            ("✧ Sort", self.sort_students),
            ("♡ Add", self.add_student),
            ("✩ Delete", self.delete_student),
            ("✦ Update", self.update_student)
        ]
        
        # Create buttons in 4-column grid layout with smaller size
        for i, (text, command) in enumerate(buttons):
            btn = tk.Button(button_frame, text=text, command=command,
                          font=('Georgia', 9, 'bold'), bg='#87CEEB', fg='#1E3A5F',
                          activebackground='#5F9EA0', activeforeground='#1E3A5F',
                          relief='raised', bd=2, width=12, height=1)
            btn.grid(row=i//4, column=i%4, padx=3, pady=2)
            self.add_button_hover_effect(btn, '#87CEEB', '#5F9EA0')
    
    def add_button_hover_effect(self, button, normal_color, hover_color):
        """
        Add hover effects to buttons.
        
        Args:
            button: Button widget to enhance
            normal_color (str): Normal state color
            hover_color (str): Hover state color
        """
        def on_enter(e):
            button['background'] = hover_color
            button['cursor'] = 'hand2'
        
        def on_leave(e):
            button['background'] = normal_color
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
    
    def create_output_area(self):
        """Create the results display area."""
        output_frame = tk.Frame(self.main_frame, bg='white')
        output_frame.pack(fill='both', expand=True, padx=15, pady=8)
        
        # Results title with decorative symbol
        tk.Label(output_frame, text="Results: ౨ৎ", font=('Georgia', 12, 'bold'), 
                fg='#2E86AB', bg='white').pack(anchor='w')
        
        # Scrollable text area for output
        self.output_text = scrolledtext.ScrolledText(output_frame, 
                                                   font=('Georgia', 10, 'bold'),
                                                   bg='#F8F9FA', fg='#333333',
                                                   width=70, height=12)
        self.output_text.pack(fill='both', expand=True, pady=4)
    
    def clear_output(self):
        """Clear the output text area."""
        self.output_text.delete(1.0, tk.END)
    
    def display_output(self, text):
        """
        Display text in the output area.
        
        Args:
            text (str): Text to display
        """
        self.clear_output()
        self.output_text.insert(tk.END, text)
    
    def view_all_students(self):
        """Display all student records with decorative formatting."""
        if not self.students:
            self.display_output("No student records found. ❀˖°")
            return
        
        # Create decorative header
        output = "· · ─ · ─ · · ─ ⋆｡˚ ─ · · ─ ·𖥸· ─ · · ─ ·⋆｡˚ ─ · · ─ · ─ · ·\n"
        output += "ALL STUDENT RECORDS ౨ৎ˖ ࣪⊹\n"
        output += "· · ─ · ─ · · ─ ⋆｡˚ ─ · · ─ ·𖥸· ─ · · ─ ·⋆｡˚ ─ · · ─ · ─ · ·\n\n"
        
        total_percentage = 0
        
        # Process each student record
        for student in self.students:
            percentage = self.calculate_percentage(student)
            total_percentage += percentage
            grade = self.calculate_grade(percentage)
            
            # Format student information with decorative elements
            output += f"Name: {student['name']} ⊹˚. ♡\n"
            output += f"Student Code: {student['code']}\n"
            output += f"Coursework Marks: {student['course_marks']}\n"
            output += f"Exam Mark: {student['exam_mark']}\n"
            output += f"Overall Percentage: {percentage:.1f}%\n"
            output += f"Grade: {grade} ❀˖°\n"
            output += "───────୨ৎ───────\n"
        
        # Calculate and display summary
        avg_percentage = total_percentage / len(self.students)
        output += f"\nSUMMARY: ᯓ★\n"
        output += f"Total Students: {len(self.students)}\n"
        output += f"Average Percentage: {avg_percentage:.1f}%\n"
        
        self.display_output(output)
    
    def view_individual_student(self):
        """Display interface for selecting and viewing individual student."""
        if not self.students:
            messagebox.showinfo("Info", "No student records found. ❀˖°")
            return
        
        self.create_student_selection_dialog("Select Student to View ⋆˚✿˖°", self.display_individual_student)
    
    def create_student_selection_dialog(self, title, callback):
        """
        Create dialog for student selection.
        
        Args:
            title (str): Dialog window title
            callback: Function to call with selected student
        """
        select_window = tk.Toplevel(self.root)
        select_window.title(title)
        select_window.geometry("400x300")
        select_window.configure(bg='#87CEEB')
        select_window.transient(self.root)
        select_window.grab_set()
        
        # Dialog title
        tk.Label(select_window, text=title, font=('Georgia', 14, 'bold'), 
                bg='#87CEEB', fg='#1E3A5F').pack(pady=10)
        
        # Listbox frame
        frame = tk.Frame(select_window, bg='#87CEEB')
        frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Student list with scrollbar
        listbox = tk.Listbox(frame, font=('Georgia', 10, 'bold'), bg='white', fg='#333333')
        scrollbar = tk.Scrollbar(frame, orient='vertical')
        
        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)
        
        # Populate listbox with students
        for student in self.students:
            listbox.insert(tk.END, f"{student['code']} - {student['name']}")
        
        listbox.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        def on_select():
            """Handle student selection."""
            selection = listbox.curselection()
            if selection:
                selected_student = self.students[selection[0]]
                select_window.destroy()
                callback(selected_student)
        
        # Selection button with decorative symbol
        tk.Button(select_window, text="Select ⊹", command=on_select,
                 font=('Georgia', 11, 'bold'), bg='#87CEEB', fg='#1E3A5F').pack(pady=10)
    
    def display_individual_student(self, student):
        """
        Display individual student record with decorative formatting.
        
        Args:
            student (dict): Student record to display
        """
        percentage = self.calculate_percentage(student)
        grade = self.calculate_grade(percentage)
        
        # Create decorative header
        output = "· · ─ · ─ · · ─ ⋆｡˚ ─ · · ─ ·𖥸· ─ · · ─ ·⋆｡˚ ─ · · ─ · ─ · ·\n"
        output += f"INDIVIDUAL STUDENT RECORD ౨ৎ˖ ࣪⊹\n"
        output += "· · ─ · ─ · · ─ ⋆｡˚ ─ · · ─ ·𖥸· ─ · · ─ ·⋆｡˚ ─ · · ─ · ─ · ·\n\n"
        
        # Format student information
        output += f"Name: {student['name']} ⊹˚. ♡\n"
        output += f"Student Code: {student['code']}\n"
        output += f"Coursework Marks: {student['course_marks']}\n"
        output += f"Total Coursework: {sum(student['course_marks'])}/60\n"
        output += f"Exam Mark: {student['exam_mark']}/100\n"
        output += f"Overall Percentage: {percentage:.1f}%\n"
        output += f"Grade: {grade} ❀˖°\n"
        
        self.display_output(output)
    
    def show_highest_scoring(self):
        """Display student with highest overall percentage."""
        if not self.students:
            messagebox.showinfo("Info", "No student records found. ❀˖°")
            return
        
        # Find student with highest percentage
        highest_student = max(self.students, key=self.calculate_percentage)
        self.display_individual_student(highest_student)
        
        # Add highlight decoration
        current_text = self.output_text.get(1.0, tk.END)
        highlighted_text = "ᯓ★ HIGHEST SCORING STUDENT ᯓ★\n\n" + current_text
        self.display_output(highlighted_text)
    
    def show_lowest_scoring(self):
        """Display student with lowest overall percentage."""
        if not self.students:
            messagebox.showinfo("Info", "No student records found. ❀˖°")
            return
        
        # Find student with lowest percentage
        lowest_student = min(self.students, key=self.calculate_percentage)
        self.display_individual_student(lowest_student)
        
        # Add highlight decoration
        current_text = self.output_text.get(1.0, tk.END)
        highlighted_text = "⋆˚✿˖° LOWEST SCORING STUDENT ⋆˚✿˖°\n\n" + current_text
        self.display_output(highlighted_text)
    
    def sort_students(self):
        """Display sorting options dialog."""
        if not self.students:
            messagebox.showinfo("Info", "No student records found. ❀˖°")
            return
        
        # Create sorting dialog
        sort_window = tk.Toplevel(self.root)
        sort_window.title("Sort Students")
        sort_window.geometry("300x200")
        sort_window.configure(bg='#87CEEB')
        sort_window.transient(self.root)
        sort_window.grab_set()
        
        # Dialog title
        tk.Label(sort_window, text="Sort Students By:", 
                font=('Georgia', 14, 'bold'), bg='#87CEEB', fg='#1E3A5F').pack(pady=10)
        
        sort_option = tk.StringVar(value="percentage")
        
        # Sorting options
        options = [
            ("Percentage (High to Low)", "percentage_desc"),
            ("Percentage (Low to High)", "percentage_asc"),
            ("Name (A-Z)", "name_asc"),
            ("Name (Z-A)", "name_desc"),
            ("Student Code", "code")
        ]
        
        # Create radio buttons for each option
        for text, value in options:
            tk.Radiobutton(sort_window, text=text, variable=sort_option, 
                          value=value, bg='#87CEEB', font=('Georgia', 10, 'bold')).pack(anchor='w', padx=20)
        
        def perform_sort():
            """Perform sorting based on selected option."""
            option = sort_option.get()
            
            # Apply appropriate sorting
            if option == "percentage_desc":
                self.students.sort(key=self.calculate_percentage, reverse=True)
            elif option == "percentage_asc":
                self.students.sort(key=self.calculate_percentage)
            elif option == "name_asc":
                self.students.sort(key=lambda x: x['name'].lower())
            elif option == "name_desc":
                self.students.sort(key=lambda x: x['name'].lower(), reverse=True)
            elif option == "code":
                self.students.sort(key=lambda x: x['code'])
            
            sort_window.destroy()
            self.view_all_students()
            messagebox.showinfo("Success", "Students sorted successfully! ✧")
        
        # Sort button with decorative symbol
        tk.Button(sort_window, text="Sort ✧", command=perform_sort,
                 font=('Georgia', 12, 'bold'), bg='#87CEEB', fg='#1E3A5F').pack(pady=10)
    
    def add_student(self):
        """Open dialog for adding new student."""
        self.create_student_edit_dialog(None, "Add New Student ♡")
    
    def delete_student(self):
        """Open dialog for deleting student."""
        if not self.students:
            messagebox.showinfo("Info", "No student records found. ❀˖°")
            return
        
        self.create_student_selection_dialog("Select Student to Delete ✩", self.confirm_delete_student)
    
    def confirm_delete_student(self, student):
        """
        Confirm and delete selected student.
        
        Args:
            student (dict): Student record to delete
        """
        result = messagebox.askyesno("Confirm Delete", 
                                   f"Are you sure you want to delete {student['name']}? ✩")
        if result:
            self.students.remove(student)
            if self.save_data():
                messagebox.showinfo("Success", "Student deleted successfully! ✩")
                self.view_all_students()
    
    def update_student(self):
        """Open dialog for updating student."""
        if not self.students:
            messagebox.showinfo("Info", "No student records found. ❀˖°")
            return
        
        self.create_student_selection_dialog("Select Student to Update ✦", 
                                           lambda s: self.create_student_edit_dialog(s, "Update Student ✦"))
    
    def create_student_edit_dialog(self, student, title):
        """
        Create dialog for adding/editing students.
        
        Args:
            student: Student to edit (None for new student)
            title (str): Dialog window title
        """
        edit_window = tk.Toplevel(self.root)
        edit_window.title(title)
        edit_window.geometry("400x500")
        edit_window.configure(bg='#87CEEB')
        edit_window.transient(self.root)
        edit_window.grab_set()
        
        # Dialog title
        tk.Label(edit_window, text=title, font=('Georgia', 16, 'bold'), 
                bg='#87CEEB', fg='#1E3A5F').pack(pady=10)
        
        # Form container
        form_frame = tk.Frame(edit_window, bg='white', bd=2, relief='raised')
        form_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        fields = []
        
        # Student code field
        tk.Label(form_frame, text="Student Code:", font=('Georgia', 10, 'bold'), 
                bg='white').grid(row=0, column=0, sticky='w', padx=10, pady=5)
        code_var = tk.StringVar(value=str(student['code']) if student else "")
        code_entry = tk.Entry(form_frame, textvariable=code_var, font=('Georgia', 10))
        code_entry.grid(row=0, column=1, sticky='ew', padx=10, pady=5)
        fields.append(('code', code_var, code_entry))
        
        # Student name field
        tk.Label(form_frame, text="Student Name:", font=('Georgia', 10, 'bold'), 
                bg='white').grid(row=1, column=0, sticky='w', padx=10, pady=5)
        name_var = tk.StringVar(value=student['name'] if student else "")
        name_entry = tk.Entry(form_frame, textvariable=name_var, font=('Georgia', 10))
        name_entry.grid(row=1, column=1, sticky='ew', padx=10, pady=5)
        fields.append(('name', name_var, name_entry))
        
        # Coursework marks fields
        course_vars = []
        for i in range(3):
            tk.Label(form_frame, text=f"Course Mark {i+1}:", font=('Georgia', 10, 'bold'), 
                    bg='white').grid(row=2+i, column=0, sticky='w', padx=10, pady=5)
            var = tk.StringVar(value=str(student['course_marks'][i]) if student else "0")
            entry = tk.Entry(form_frame, textvariable=var, font=('Georgia', 10))
            entry.grid(row=2+i, column=1, sticky='ew', padx=10, pady=5)
            course_vars.append(var)
        
        # Exam mark field
        tk.Label(form_frame, text="Exam Mark:", font=('Georgia', 10, 'bold'), 
                bg='white').grid(row=5, column=0, sticky='w', padx=10, pady=5)
        exam_var = tk.StringVar(value=str(student['exam_mark']) if student else "0")
        exam_entry = tk.Entry(form_frame, textvariable=exam_var, font=('Georgia', 10))
        exam_entry.grid(row=5, column=1, sticky='ew', padx=10, pady=5)
        
        form_frame.columnconfigure(1, weight=1)
        
        def save_student():
            """Validate and save student data."""
            try:
                # Validate input data
                code = int(code_var.get())
                name = name_var.get().strip()
                course_marks = [int(var.get()) for var in course_vars]
                exam_mark = int(exam_var.get())
                
                # Input validation
                if not name:
                    messagebox.showerror("Error", "Student name is required. ❀˖°")
                    return
                
                if any(mark < 0 or mark > 20 for mark in course_marks):
                    messagebox.showerror("Error", "Course marks must be between 0 and 20. ❀˖°")
                    return
                
                if exam_mark < 0 or exam_mark > 100:
                    messagebox.showerror("Error", "Exam mark must be between 0 and 100. ❀˖°")
                    return
                
                # Check for duplicate code when adding new student
                if not student and any(s['code'] == code for s in self.students):
                    messagebox.showerror("Error", "Student code already exists. ❀˖°")
                    return
                
                # Update or add student
                if student:
                    # Update existing student
                    student['code'] = code
                    student['name'] = name
                    student['course_marks'] = course_marks
                    student['exam_mark'] = exam_mark
                    success_message = "Student updated successfully! ✦"
                else:
                    # Add new student
                    new_student = {
                        'code': code,
                        'name': name,
                        'course_marks': course_marks,
                        'exam_mark': exam_mark
                    }
                    self.students.append(new_student)
                    success_message = "Student added successfully! ♡"
                
                # Save to file and close dialog
                if self.save_data():
                    edit_window.destroy()
                    messagebox.showinfo("Success", success_message)
                    self.view_all_students()
                
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers for marks. ❀˖°")
        
        # Action buttons
        button_frame = tk.Frame(edit_window, bg='#87CEEB')
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Save ✧", command=save_student,
                 font=('Georgia', 12, 'bold'), bg='#87CEEB', fg='#1E3A5F').pack(side='left', padx=5)
        
        tk.Button(button_frame, text="Cancel ❀", command=edit_window.destroy,
                 font=('Georgia', 12, 'bold'), bg='#87CEEB', fg='#1E3A5F').pack(side='left', padx=5)

def main():
    """
    Main application entry point.
    
    Initializes Tkinter and starts the Student Manager application.
    """
    root = tk.Tk()
    app = StudentManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()