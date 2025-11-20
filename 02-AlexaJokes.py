import tkinter as tk
from tkinter import ttk
import random
from pathlib import Path
import pygame
from PIL import Image, ImageTk
import os

class AlexaJokeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Alexa's Joke Corner")
        self.root.geometry("700x600")
        self.root.configure(bg='#f8f4ff')
        
        # Initialize pygame for sound
        pygame.mixer.init()
        
        # Enhanced color scheme
        self.colors = {
            'bg': '#f8f4ff',
            'accent': '#e6e0ff',
            'accent2': '#f0ebff',
            'text': '#4a2c6d',
            'button': '#8a2be2',
            'button_hover': '#6a0dad',
            'star_active': '#ffd700',
            'star_inactive': '#d3d3d3'
        }
        
        # Sound files and images
        self.sounds = {}
        self.images = {}
        self.load_sounds()
        self.load_images()
        
        # Joke data and state
        self.jokes = []
        self.current_joke = None
        self.punchline_shown = False
        self.rating_given = False
        self.joke_count = 0
        self.load_jokes()
        
        # Start with welcome screen
        self.show_welcome_screen()
    
    def load_images(self):
        """Load background images"""
        try:
            photos_path = Path("Assessment 1 - Skills Portfolio/A1 - Resources/Photos")
            
            # Load neutral background
            neutral_path = photos_path / "neutral.png"
            if neutral_path.exists():
                image = Image.open(neutral_path)
                image = image.resize((200, 150), Image.LANCZOS)  # Smaller size
                self.images['neutral'] = ImageTk.PhotoImage(image)
            
            # Load cry image for punchline
            cry_path = photos_path / "cry.png"
            if cry_path.exists():
                image = Image.open(cry_path)
                image = image.resize((200, 150), Image.LANCZOS)  # Smaller size
                self.images['cry'] = ImageTk.PhotoImage(image)
                
        except Exception as e:
            print(f"Image loading error: {e}")
    
    def load_sounds(self):
        """Load sound files in multiple formats"""
        try:
            sound_path = Path("Assessment 1 - Skills Portfolio/A1 - Resources/Sounds")
            
            if sound_path.exists():
                # Define all available sound files
                self.available_sounds = {
                    'laughter': [
                        sound_path / "57814__timtube__laughing-9.wav"
                    ],
                    'applause': [
                        sound_path / "324184__kwahmah_02__applause-05.wav"
                    ],
                    'cricket': [
                        sound_path / "352789__vintprox__cricket.ogg"
                    ],
                    'fbi': [
                        sound_path / "656732__paladinvii__fbi-open-up-pvii.mp3"
                    ],
                    'crowd_wow': [
                        sound_path / "581410__audiosea__crowd-wow-sound-effect-1.wav"
                    ]
                }
                
                # Load sounds that exist
                for category, files in self.available_sounds.items():
                    for file_path in files:
                        if file_path.exists():
                            self.sounds[category] = pygame.mixer.Sound(file_path)
                            print(f"Loaded {category} sound: {file_path.name}")
                            break
                        else:
                            print(f"Sound file not found: {file_path}")
                
                print("Sound files loaded successfully!")
                
            else:
                print("Sounds folder not found - using fallback")
                self.create_fallback_sounds()
                
        except Exception as e:
            print(f"Sound loading error: {e} - Using fallback sounds")
            self.create_fallback_sounds()
    
    def create_fallback_sounds(self):
        """Create simple fallback sounds"""
        try:
            # Create basic fallback sounds
            self.sounds['laughter'] = pygame.mixer.Sound(buffer=bytes([100] * 512))
            self.sounds['applause'] = pygame.mixer.Sound(buffer=bytes([150] * 512))
            self.sounds['crowd_wow'] = pygame.mixer.Sound(buffer=bytes([200] * 512))
        except:
            self.sounds['laughter'] = None
            self.sounds['applause'] = None
            self.sounds['crowd_wow'] = None
    
    def load_jokes(self):
        """Load jokes from file"""
        try:
            file_path = Path("Assessment 1 - Skills Portfolio/A1 - Resources/randomJokes.txt")
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as file:
                    lines = [line.strip() for line in file if line.strip()]
                    self.jokes = [line for line in lines if '?' in line]
                    
                if not self.jokes:
                    raise ValueError("No valid jokes found")
                print(f"Successfully loaded {len(self.jokes)} jokes!")
                    
            else:
                self.jokes = [
                    "Why did the scarecrow win an award?~He was outstanding in his field!",
                    "What do you call a fake noodle?~An impasta!"
                ]
                
        except Exception as e:
            self.jokes = ["Error loading jokes?~Try again later!"]
    
    def show_welcome_screen(self):
        """Show welcome screen with start button"""
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Welcome frame
        welcome_frame = tk.Frame(self.root, bg=self.colors['bg'])
        welcome_frame.pack(expand=True, fill='both')
        
        # Title
        title_label = tk.Label(
            welcome_frame,
            text="Alexa's Humor",
            font=("Georgia", 32, "bold"),
            fg=self.colors['text'],
            bg=self.colors['bg']
        )
        title_label.pack(pady=80)
        
        # Start button
        start_btn = tk.Button(
            welcome_frame,
            text="Start",
            command=self.setup_gui,
            font=("Verdana", 16, "bold"),
            bg=self.colors['button'],
            fg='white',
            relief='raised',
            padx=30,
            pady=15,
            cursor="hand2"
        )
        start_btn.pack(pady=20)
        
        # Add hover effect to start button
        def on_enter(e):
            start_btn['bg'] = self.colors['button_hover']
        def on_leave(e):
            start_btn['bg'] = self.colors['button']
        start_btn.bind("<Enter>", on_enter)
        start_btn.bind("<Leave>", on_leave)
    
    def setup_gui(self):
        """Setup the main application GUI"""
        # Clear welcome screen
        for widget in self.root.winfo_children():
            widget.destroy()
        
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
        self.joke_frame = tk.Frame(
            main_frame, 
            bg=self.colors['accent2'], 
            padx=20, 
            pady=20
        )
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
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        button_frame.pack(pady=10)
        
        # Action buttons
        self.tell_joke_btn = self.create_button(button_frame, "Alexa tell me a Joke", self.show_new_joke)
        self.tell_joke_btn.pack(side='left', padx=5)
        
        self.punchline_btn = self.create_button(button_frame, "Show Punchline", self.show_punchline)
        self.punchline_btn.pack(side='left', padx=5)
        
        self.next_joke_btn = self.create_button(button_frame, "Next Joke", self.show_new_joke)
        self.next_joke_btn.pack(side='left', padx=5)
        
        self.rate_btn = self.create_button(button_frame, "Rate my Joke", self.show_rating)
        self.rate_btn.pack(side='left', padx=5)
        
        # Quit button
        quit_btn = self.create_button(main_frame, "Quit", self.root.quit, '#f0ebff')
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
        
        # Image display at bottom center
        self.image_label = tk.Label(main_frame, bg=self.colors['bg'])
        self.image_label.pack(pady=10)
        
        # Show neutral image initially
        if 'neutral' in self.images:
            self.image_label.config(image=self.images['neutral'])
        
        # Initially disable some buttons
        self.punchline_btn.config(state='disabled')
        self.rate_btn.config(state='disabled')
        
        # Show first joke
        self.show_new_joke()
    
    def create_button(self, parent, text, command, color=None):
        """Create a styled button"""
        btn_color = color or self.colors['button']
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=("Verdana", 10, "bold"),
            bg='#f0ebff',
            fg=self.colors['text'],
            relief='raised',
            padx=15,
            pady=8,
            cursor="hand2",
            borderwidth=2
        )
        
        def on_enter(e):
            btn['bg'] = self.colors['button']
            btn['fg'] = 'white'
        def on_leave(e):
            btn['bg'] = '#f0ebff'
            btn['fg'] = self.colors['text']
            
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn
    
    def show_error_message(self, message):
        """Show temporary error messages"""
        if hasattr(self, 'status_label'):
            self.status_label.config(text=message)
            self.root.after(3000, lambda: self.status_label.config(text=""))
    
    def play_punchline_sound(self):
        """Play random punchline sound"""
        try:
            # Randomly select a sound to play
            sound_options = ['laughter', 'cricket', 'fbi']
            available_sounds = [s for s in sound_options if s in self.sounds and self.sounds[s]]
            
            if available_sounds:
                selected_sound = random.choice(available_sounds)
                self.sounds[selected_sound].play()
                
                # Show appropriate message
                if selected_sound == 'laughter':
                    self.show_error_message("HAHAHA! That was hilarious!")
                elif selected_sound == 'cricket':
                    self.show_error_message("*cricket sounds* ...tough crowd!")
                elif selected_sound == 'fbi':
                    self.show_error_message("FBI OPEN UP! That joke was criminal!")
            else:
                self.show_error_message("Ba-dum-tss!")
                
        except Exception as e:
            self.show_error_message("Audience reaction!")
    
    def play_celebration_sound(self):
        """Play celebration sound for 5-star rating"""
        try:
            # Try to play crowd wow sound first, then applause as fallback
            if 'crowd_wow' in self.sounds and self.sounds['crowd_wow']:
                self.sounds['crowd_wow'].play()
                self.show_error_message("WOW! The crowd goes wild!")
            elif 'applause' in self.sounds and self.sounds['applause']:
                self.sounds['applause'].play()
                self.show_error_message("Standing ovation!")
            else:
                self.show_error_message("Celebration!")
        except Exception as e:
            self.show_error_message("Celebration!")
    
    def show_new_joke(self):
        """Display a new random joke"""
        if self.joke_count > 0 and not self.punchline_shown:
            self.show_error_message("Greedy for jokes huh?? At least let me finish!")
        
        # Reset state
        self.punchline_shown = False
        self.rating_given = False
        self.rating_frame.pack_forget()
        self.rating_response.config(text="")
        
        # Show neutral image
        if 'neutral' in self.images:
            self.image_label.config(image=self.images['neutral'])
        
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
        """Display the punchline"""
        if not hasattr(self, 'current_punchline'):
            self.show_error_message("Bro you don't even KNOW the joke yet...")
            return
        
        if self.punchline_shown:
            self.show_error_message("Already showed you the punchline! Memory issues?")
            return
        
        self.punchline_label.config(text=self.current_punchline)
        self.punchline_shown = True
        self.rate_btn.config(state='normal')
        
        # Play random sound and show cry image
        self.play_punchline_sound()
        if 'cry' in self.images:
            self.image_label.config(image=self.images['cry'])
    
    def show_rating(self):
        """Show the rating stars"""
        if not self.punchline_shown:
            self.show_error_message("Can't rate what you haven't seen! Show the punchline first.")
            return
        
        self.rating_frame.pack(pady=10)
    
    def rate_joke(self, stars):
        """Handle joke rating"""
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
        else:
            response = f"Thanks for the {stars} star rating!"

        self.rating_response.config(text=response)

def main():
    root = tk.Tk()
    app = AlexaJokeApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()