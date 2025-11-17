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
        self.load_jokes()
        
        self.setup_gui()
    
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
                    
                print(f"Loaded {len(self.jokes)} jokes")
                
            else:
                # Fallback jokes
                self.jokes = [
                    "Why did the scarecrow win an award?~He was outstanding in his field!",
                    "What do you call a fake noodle?~An impasta!"
                ]
                print("Using fallback jokes")
                
        except Exception as e:
            print(f"Error loading jokes: {e}")
            self.jokes = ["Error loading jokes?~Try again later!"]

    def setup_gui(self):
        """Setup the basic GUI structure"""
        main_frame = tk.Frame(self.root, bg = '#f8f4ff', padx=20, pady=20)
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
        
        # Basic quit button
        quit_btn = tk.Button(
            main_frame,
            text = "Quit",
            command = self.root.quit,
            font = ("Verdana", 10),
            bg = '#9370db',
            fg = 'white',
            padx = 15,
            pady = 8
        )
        quit_btn.pack(pady = 20)

def main():
    root = tk.Tk()
    app = AlexaJokesApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()