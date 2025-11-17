import tkinter as tk
from tkinter import ttk

class AlexaJokesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Alexa's Joke Corner")
        self.root.geometry("600x500")
        self.root.configure(bg='#f8f4ff')

        # Basic setup
        self.setup_gui()

    def setup_gui(self):
        """SEtup the basic GUI structure."""
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

def main ():
    root = tk.Tk()
    app = AlexaJokesApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()