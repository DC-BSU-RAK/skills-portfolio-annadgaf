import tkinter as tk
from tkinter import ttk
import random
from pathlib import Path
import pygame

class AlexaJokeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Alexa's Joke Corner")
        self.root.geometry("650x550")
        self.root.configure(bg='#f8f4ff')
        
        # Initialize pygame for sound
        pygame.mixer.init()
        
        # Enhanced color scheme with better button colors
        self.colors = {
            'bg': '#f8f4ff',
            'accent': '#e6e0ff',
            'accent2': '#f0ebff',
            'text': '#4a2c6d',
            'button': '#8a2be2',      # Brighter purple
            'button_hover': '#6a0dad', # Darker purple for hover
            'star_active': '#ffd700',
            'star_inactive': '#d3d3d3'
        }
        
        # Joke data and state
        self.jokes = []
        self.current_joke = None
        self.punchline_shown = False
        self.rating_given = False
        self.joke_count = 0
        self.load_jokes()
        
        self.setup_gui()
        self.show_new_joke()
    
    def load_jokes(self):
        """Load jokes from A1 - Resources/randomJokes.txt file"""
        try:
            file_path = Path("A1 - Resources/randomJokes.txt")
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as file:
                    lines = [line.strip() for line in file if line.strip()]
                    self.jokes = [line for line in lines if '?' in line]
                    
                if not self.jokes:
                    raise ValueError("No valid jokes found")
                    
            else:
                self.jokes = [
                    "Why did the scarecrow win an award?~He was outstanding in his field!",
                    "What do you call a fake noodle?~An impasta!"
                ]
                self.show_error_message("Error 404: Humor not found. Using backup jokes!")
                
        except Exception as e:
            self.jokes = ["Error loading jokes?~Try again later!"]
            self.show_error_message("Alexa forgot the jokes, please be patient")

    def show_error_message(self, message):
        """Show temporary error messages in status label"""
        self.status_label.config(text=message)
        self.root.after(3000, lambda: self.status_label.config(text=""))

    def play_punchline_sound(self):
        """Play audience laughter sound effect"""
        try:
            # Create a laughter-like sound using multiple tones
            for i in range(3):
                # Varying frequencies to simulate laughter
                freq = 300 + (i * 50)
                pygame.mixer.Sound(buffer=bytes([freq] * 3000)).play()
                pygame.time.delay(150)
        except Exception as e:
            print(f"Sound error: {e} - Continuing without audio")

    def play_celebration_sound(self):
        """Play applause and celebration sound effect"""
        try:
            # Create applause-like sound with multiple tones
            for i in range(5):
                # Random frequencies to simulate clapping
                freq = random.randint(200, 400)
                pygame.mixer.Sound(buffer=bytes([freq] * 1000)).play()
                pygame.time.delay(80)
        except Exception as e:
            print(f"Sound error: {e} - Continuing without audio")

    def create_button(self, parent, text, command, color=None):
        """Create a styled button with hover effects"""
        btn_color = color or self.colors['button']
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=("Verdana", 10, "bold"),
            bg=btn_color,
            fg='white',
            relief='raised',
            padx=15,
            pady=8,
            cursor="hand2"
        )
        
        # Add hover effect
        def on_enter(e):
            btn['bg'] = self.colors['button_hover']
        def on_leave(e):
            btn['bg'] = btn_color
            
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn

    def setup_gui(self):
        """Setup the GUI structure with improved button styling"""
        main_frame = tk.Frame(self.root, bg=self.colors['bg'], padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="Alexa's Joke Corner", 
            font=("Georgia", 20, "bold"),
            fg=self.colors['text'],
            bg=self.colors['bg']
        )
        title_label.pack(pady=20)
        
        # Joke display frame
        self.joke_frame = tk.Frame(main_frame, bg=self.colors['accent2'], padx=20, pady=20)
        self.joke_frame.pack(fill='both', expand=True, pady=20)
        
        # Setup label
        self.setup_label = tk.Label(
            self.joke_frame,
            text="",
            font=("Georgia", 14),
            fg=self.colors['text'],
            bg=self.colors['accent2'],
            wraplength=500,
            justify='center'
        )
        self.setup_label.pack(pady=10)
        
        # Punchline label
        self.punchline_label = tk.Label(
            self.joke_frame,
            text="",
            font=("Georgia", 12, "italic"),
            fg='#6a4c9c',
            bg=self.colors['accent2'],
            wraplength=500,
            justify='center'
        )
        self.punchline_label.pack(pady=10)
        
        # Rating frame (initially hidden)
        self.rating_frame = tk.Frame(self.joke_frame, bg=self.colors['accent2'])
        self.rating_label = tk.Label(
            self.rating_frame,
            text="Rate this joke:",
            font=("Verdana", 10),
            fg=self.colors['text'],
            bg=self.colors['accent2']
        )
        self.rating_label.pack(pady=(10, 5))
        
        self.stars_frame = tk.Frame(self.rating_frame, bg=self.colors['accent2'])
        self.stars_frame.pack()
        
        self.star_buttons = []
        for i in range(5):
            star = tk.Label(
                self.stars_frame,
                text="★",
                font=("Arial", 20),
                fg=self.colors['star_inactive'],
                bg=self.colors['accent2'],
                cursor="hand2"
            )
            star.pack(side='left')
            star.bind('<Button-1>', lambda e, idx=i: self.rate_joke(idx + 1))
            self.star_buttons.append(star)
        
        self.rating_response = tk.Label(
            self.rating_frame,
            text="",
            font=("Verdana", 9, "italic"),
            fg=self.colors['text'],
            bg=self.colors['accent2']
        )
        self.rating_response.pack(pady=5)
        
        # Button frame with improved styling
        button_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        button_frame.pack(pady=10)
        
        # Action buttons with new purple styling
        self.tell_joke_btn = self.create_button(button_frame, "Alexa tell me a Joke", self.show_new_joke)
        self.tell_joke_btn.pack(side='left', padx=5)
        
        self.punchline_btn = self.create_button(button_frame, "Show Punchline", self.show_punchline)
        self.punchline_btn.pack(side='left', padx=5)
        
        self.next_joke_btn = self.create_button(button_frame, "Next Joke", self.show_new_joke)
        self.next_joke_btn.pack(side='left', padx=5)
        
        self.rate_btn = self.create_button(button_frame, "Rate my Joke", self.show_rating)
        self.rate_btn.pack(side='left', padx=5)
        
        # Quit button
        quit_btn = self.create_button(main_frame, "Quit", self.root.quit, '#d27979')
        quit_btn.pack(pady=10)
        
        # Status label for error messages
        self.status_label = tk.Label(
            main_frame,
            text="",
            font=("Verdana", 8, "italic"),
            fg='#666666',
            bg=self.colors['bg']
        )
        self.status_label.pack(pady=5)
        
        # Initially disable some buttons
        self.punchline_btn.config(state='disabled')
        self.rate_btn.config(state='disabled')

    def show_new_joke(self):
        """Display a new random joke with greedy detection"""
        # Check for greedy behavior
        if self.joke_count > 0 and not self.punchline_shown:
            self.show_error_message("Greedy for jokes huh?? At least let me finish!")
        
        # Reset state
        self.punchline_shown = False
        self.rating_given = False
        self.rating_frame.pack_forget()
        self.rating_response.config(text="")
        
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
            
            self.setup_label.config(text=setup)
            self.punchline_label.config(text="")
            self.punchline_btn.config(state='normal')
            self.rate_btn.config(state='disabled')
            
            # Reset stars
            for star in self.star_buttons:
                star.config(fg=self.colors['star_inactive'])
            
            self.joke_count += 1

    def show_punchline(self):
        """Display the punchline with spam detection"""
        if not hasattr(self, 'current_punchline'):
            self.show_error_message("Bro you don't even KNOW the joke yet...")
            return
        
        if self.punchline_shown:
            self.show_error_message("Already showed you the punchline! Memory issues?")
            return
        
        self.punchline_label.config(text=self.current_punchline)
        self.punchline_shown = True
        self.rate_btn.config(state='normal')
        self.play_punchline_sound()
        self.show_error_message("Audience laughter! Ba-dum-tss!")

    def show_rating(self):
        """Show the rating stars with validation"""
        if not self.punchline_shown:
            self.show_error_message("Can't rate what you haven't seen! Show the punchline first.")
            return
        
        self.rating_frame.pack(pady=10)

    def rate_joke(self, stars):
        """Handle joke rating with duplicate detection"""
        if self.rating_given:
            self.show_error_message("You already rated this one! Make up your mind!")
            return
        
        self.rating_given = True
        
        # Update star colors
        for i, star in enumerate(self.star_buttons):
            if i < stars:
                star.config(fg=self.colors['star_active'])
            else:
                star.config(fg=self.colors['star_inactive'])
        
        # Show response based on rating
        if stars == 1:
            response = "Ouch... you hurt my motherboard.."
        elif stars == 5:
            response = "WOOO I'm basically a stand-up comedian now.."
            self.play_celebration_sound()
            self.show_error_message("Standing ovation!")
        else:
            response = f"Thanks for the {stars} star rating!"

        self.rating_response.config(text=response)

def main():
    root = tk.Tk()
    app = AlexaJokeApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()