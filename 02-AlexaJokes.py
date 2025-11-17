import tkinter as tk
from tkinter import ttk
import random
from pathlib import Path

class AlexaJokesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Alexa's Joke Corner")
        self.root.geometry("600x500")
        self.root.configure(bg = '#f8f4ff')
        
        # Joke data
        self.jokes = []
        self.current_joke = None
        self.load_jokes()
        
        self.setup_gui()
        self.show_new_joke()
    
    def load_jokes(self):
        """Load jokes from randomJokes.txt file"""
        try:
            file_path = Path("randomJokes.txt")
            if file_path.exists():
                with open(file_path, 'r', encoding = 'utf-8') as file:
                    lines = [line.strip() for line in file if line.strip()]
                    self.jokes = [line for line in lines if '?' in line]
                    
                if not self.jokes:
                    raise ValueError("No valid jokes found")
                    
            else:
                self.jokes = [
                    "Why did the scarecrow win an award?~He was outstanding in his field!",
                    "What do you call a fake noodle?~An impasta!"
                ]
                
        except Exception as e:
            self.jokes = ["Error loading jokes?~Try again later!"]

    def setup_gui(self):
        """Setup the GUI structure"""
        main_frame = tk.Frame(self.root, bg = '#f8f4ff', padx = 20, pady = 20)
        main_frame.pack(fill = 'both', expand = True)
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text = "Alexa's Joke Corner", 
            font = ("Georgia", 20, "bold"),
            fg = '#4a2c6d',
            bg = '#f8f4ff'
        )
        title_label.pack(pady = 20)
        
        # Joke display frame
        self.joke_frame = tk.Frame(main_frame, bg = '#f0ebff', padx = 20, pady = 20)
        self.joke_frame.pack(fill = 'both', expand = True, pady = 20)
        
        # Setup label
        self.setup_label = tk.Label(
            self.joke_frame,
            text = "",
            font = ("Georgia", 14),
            fg = '#4a2c6d',
            bg = '#f0ebff',
            wraplength = 500,
            justify = 'center'
        )
        self.setup_label.pack(pady=10)
        
        # Punchline label
        self.punchline_label = tk.Label(
            self.joke_frame,
            text = "",
            font = ("Georgia", 12, "italic"),
            fg = '#6a4c9c',
            bg = '#f0ebff',
            wraplength = 500,
            justify = 'center'
        )
        self.punchline_label.pack(pady = 10)
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg = '#f8f4ff')
        button_frame.pack(pady = 10)
        
        # Action buttons
        self.tell_joke_btn = tk.Button(
            button_frame,
            text = "Alexa tell me a Joke",
            command = self.show_new_joke,
            font = ("Verdana", 10),
            bg = '#9370db',
            fg = 'white',
            padx = 15,
            pady = 8
        )
        self.tell_joke_btn.pack(side = 'left', padx = 5)
        
        self.punchline_btn = tk.Button(
            button_frame,
            text = "Show Punchline",
            command = self.show_punchline,
            font = ("Verdana", 10),
            bg = '#9370db',
            fg = 'white',
            padx = 15,
            pady = 8
        )
        self.punchline_btn.pack(side = 'left', padx = 5)
        
        # Quit button
        quit_btn = tk.Button(
            main_frame,
            text = "Quit",
            command = self.root.quit,
            font = ("Verdana", 10),
            bg = '#d27979',
            fg = 'white',
            padx = 15,
            pady = 8
        )
        quit_btn.pack(pady = 10)

    def show_new_joke(self):
        """Display a new random joke"""
        if self.jokes:
            self.current_joke = random.choice(self.jokes)
            if '?' in self.current_joke:
                setup, punchline = self.current_joke.split('?', 1)
                setup = setup.strip() + "?"
                punchline = punchline.strip()
            else:
                setup = self.current_joke
                punchline = "Punchline missing!"
            
            self.current_setup = setup
            self.current_punchline = punchline
            
            self.setup_label.config(text = setup)
            self.punchline_label.config(text = "")
            self.punchline_btn.config(state = 'normal')

    def show_punchline(self):
        """Display the punchline"""
        if hasattr(self, 'current_punchline'):
            self.punchline_label.config(text = self.current_punchline)

def main():
    root = tk.Tk()
    app = AlexaJokesApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()