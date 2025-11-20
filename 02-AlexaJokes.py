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
        """Load background images with error handling"""
        try:
            photos_path = Path("Assessment 1 - Skills Portfolio/A1 - Resources/Photos")
            
            if not photos_path.exists():
                self.show_welcome_error("Images folder not found - running without images")
                return
            
            # Load neutral background
            neutral_path = photos_path / "neutral.png"
            if neutral_path.exists():
                image = Image.open(neutral_path)
                image = image.resize((200, 150), Image.LANCZOS)
                self.images['neutral'] = ImageTk.PhotoImage(image)
                print("Loaded neutral.png successfully")
            else:
                print("neutral.png not found in Photos folder")
            
            # Load cry image for punchline
            cry_path = photos_path / "cry.png"
            if cry_path.exists():
                image = Image.open(cry_path)
                image = image.resize((200, 150), Image.LANCZOS)
                self.images['cry'] = ImageTk.PhotoImage(image)
                print("Loaded cry.png successfully")
            else:
                print("cry.png not found in Photos folder")
                
        except Exception as e:
            print(f"Image loading error: {e}")
            self.show_welcome_error("Error loading images - continuing without them")
    
    def show_welcome_error(self, message):
        """Store error message to show after GUI loads"""
        if hasattr(self, 'pending_error'):
            self.pending_error += f" | {message}"
        else:
            self.pending_error = message
    
    def load_sounds(self):
        """Load sound files with comprehensive error handling"""
        try:
            sound_path = Path("Assessment 1 - Skills Portfolio/A1 - Resources/Sounds")
            
            if not sound_path.exists():
                self.show_welcome_error("Sounds folder not found - using fallback sounds")
                self.create_fallback_sounds()
                return
            
            # Define all available sound files
            sound_files = {
                'laughter': "57814__timtube__laughing-9.wav",
                'applause': "324184__kwahmah_02__applause-05.wav",
                'cricket': "352789__vintprox__cricket.ogg",
                'fbi': "656732__paladinvii__fbi-open-up-pvii.mp3",
                'crowd_wow': "581410__audiosea__crowd-wow-sound-effect-1.wav"
            }
            
            loaded_sounds = 0
            missing_sounds = []
            
            for category, filename in sound_files.items():
                file_path = sound_path / filename
                if file_path.exists():
                    try:
                        self.sounds[category] = pygame.mixer.Sound(file_path)
                        loaded_sounds += 1
                        print(f"✓ Loaded {filename}")
                    except Exception as e:
                        print(f"✗ Failed to load {filename}: {e}")
                        missing_sounds.append(filename)
                else:
                    print(f"✗ File not found: {filename}")
                    missing_sounds.append(filename)
            
            if loaded_sounds > 0:
                print(f"Successfully loaded {loaded_sounds} sound files")
            else:
                self.show_welcome_error("No sound files loaded - using fallback sounds")
                self.create_fallback_sounds()
                
            if missing_sounds:
                self.show_welcome_error(f"Missing {len(missing_sounds)} sound files")
                
        except Exception as e:
            print(f"Sound loading error: {e}")
            self.show_welcome_error("Error loading sounds - using fallback")
            self.create_fallback_sounds()
    
    def create_fallback_sounds(self):
        """Create simple fallback sounds"""
        try:
            self.sounds['laughter'] = pygame.mixer.Sound(buffer=bytes([100] * 512))
            self.sounds['applause'] = pygame.mixer.Sound(buffer=bytes([150] * 512))
            self.sounds['crowd_wow'] = pygame.mixer.Sound(buffer=bytes([200] * 512))
            print("Created fallback sounds")
        except:
            print("Failed to create fallback sounds")
            self.sounds['laughter'] = None
            self.sounds['applause'] = None
            self.sounds['crowd_wow'] = None
    
    def load_jokes(self):
        """Load jokes from file with detailed error reporting"""
        try:
            file_path = Path("Assessment 1 - Skills Portfolio/A1 - Resources/randomJokes.txt")
            
            if not file_path.exists():
                self.show_welcome_error("Joke file not found - using backup jokes")
                self.jokes = self.get_fallback_jokes()
                return
            
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = [line.strip() for line in file if line.strip()]
                self.jokes = [line for line in lines if '?' in line]
            
            if not self.jokes:
                self.show_welcome_error("No valid jokes found in file - using backup")
                self.jokes = self.get_fallback_jokes()
            else:
                print(f"✓ Loaded {len(self.jokes)} jokes successfully")
                    
        except Exception as e:
            print(f"Joke loading error: {e}")
            self.show_welcome_error("Error loading jokes - using backup")
            self.jokes = self.get_fallback_jokes()
    
    def get_fallback_jokes(self):
        """Provide fallback jokes when file loading fails"""
        return [
            "Why did the scarecrow win an award?~He was outstanding in his field!",
            "What do you call a fake noodle?~An impasta!",
            "Why don't scientists trust atoms?~Because they make up everything!",
            "What do you call a sleeping bull?~A bulldozer!",
            "Why did the coffee file a police report?~It got mugged!"
        ]
    
    def show_welcome_screen(self):
        """Show welcome screen with start button"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
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
            text="Alexa tell me a Joke",
            command=self.setup_gui,
            font=("Verdana", 14, "bold"),
            bg='#f0ebff',
            fg=self.colors['text'],
            relief='raised',
            padx=25,
            pady=12,
            cursor="hand2",
            borderwidth=2
        )
        start_btn.pack(pady=20)
        
        # Error display area (initially hidden)
        self.welcome_error_label = tk.Label(
            welcome_frame,
            text="",
            font=("Verdana", 9),
            fg='#d27979',
            bg=self.colors['bg'],
            wraplength=500
        )
        self.welcome_error_label.pack(pady=10)
        
        # Show any loading errors
        if hasattr(self, 'pending_error'):
            self.welcome_error_label.config(text=f"Note: {self.pending_error}")
        
        # Add hover effect
        def on_enter(e):
            start_btn['bg'] = self.colors['button']
            start_btn['fg'] = 'white'
        def on_leave(e):
            start_btn['bg'] = '#f0ebff'
            start_btn['fg'] = self.colors['text']
            
        start_btn.bind("<Enter>", on_enter)
        start_btn.bind("<Leave>", on_leave)
    
    def setup_gui(self):
        """Setup the main application GUI"""
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
        
        # Rating frame
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
        
        # Show neutral image if available
        if 'neutral' in self.images:
            self.image_label.config(image=self.images['neutral'])
        else:
            self.image_label.config(text="[Images not available]", fg='#999999')
        
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
            self.root.after(4000, lambda: self.status_label.config(text=""))
    
    def play_punchline_sound(self):
        """Play random punchline sound with error handling"""
        try:
            sound_options = ['laughter', 'cricket', 'fbi']
            available_sounds = [s for s in sound_options if s in self.sounds and self.sounds[s]]
            
            if available_sounds:
                selected_sound = random.choice(available_sounds)
                self.sounds[selected_sound].play()
                
                if selected_sound == 'laughter':
                    self.show_error_message("HAHAHA! That was hilarious!")
                elif selected_sound == 'cricket':
                    self.show_error_message("*cricket sounds* ...tough crowd!")
                elif selected_sound == 'fbi':
                    self.show_error_message("FBI OPEN UP! That joke was criminal!")
            else:
                self.show_error_message("Ba-dum-tss! (Sound effects unavailable)")
                
        except Exception as e:
            self.show_error_message("Audience reaction! (Sound error)")
    
    def play_celebration_sound(self):
        """Play celebration sound for 5-star rating"""
        try:
            if 'crowd_wow' in self.sounds and self.sounds['crowd_wow']:
                self.sounds['crowd_wow'].play()
                self.show_error_message("WOW! The crowd goes wild!")
            elif 'applause' in self.sounds and self.sounds['applause']:
                self.sounds['applause'].play()
                self.show_error_message("Standing ovation!")
            else:
                self.show_error_message("Celebration! (Sound effects unavailable)")
        except Exception as e:
            self.show_error_message("Celebration! (Sound error)")
    
    def show_new_joke(self):
        """Display a new random joke with greedy detection"""
        if self.joke_count > 0 and not self.punchline_shown:
            self.show_error_message("Greedy for jokes huh?? At least let me finish!")
            return
        
        # Reset state
        self.punchline_shown = False
        self.rating_given = False
        self.rating_frame.pack_forget()
        self.rating_response.config(text="")
        
        # Show neutral image if available
        if 'neutral' in self.images:
            self.image_label.config(image=self.images['neutral'])
        
        if not self.jokes:
            self.show_error_message("No jokes available! Check your joke file.")
            self.setup_label.config(text="No jokes loaded. Please check the randomJokes.txt file.")
            self.punchline_btn.config(state='disabled')
            return
        
        self.current_joke = random.choice(self.jokes)
        if '?' in self.current_joke:
            setup, punchline = self.current_joke.split('?', 1)
            setup = setup.strip() + "?"
            punchline = punchline.strip()
        else:
            setup = self.current_joke
            punchline = "Punchline missing! Alexa is having a moment..."
        
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
        """Display the punchline with comprehensive validation"""
        if not hasattr(self, 'current_punchline'):
            self.show_error_message("Error: No joke loaded. Try 'Next Joke' first.")
            return
        
        if self.punchline_shown:
            self.show_error_message("Patience! Already showed you the punchline!")
            return
        
        self.punchline_label.config(text=self.current_punchline)
        self.punchline_shown = True
        self.rate_btn.config(state='normal')
        
        # Play random sound and show cry image if available
        self.play_punchline_sound()
        if 'cry' in self.images:
            self.image_label.config(image=self.images['cry'])
    
    def show_rating(self):
        """Show the rating stars with validation"""
        if not self.punchline_shown:
            self.show_error_message("Can't rate what you haven't seen! Show the punchline first.")
            return
        
        if self.rating_given:
            self.show_error_message("You already rated this masterpiece!")
            return
        
        self.rating_frame.pack(pady=10)
        self.show_error_message("Let me know how I did!")
    
    def rate_joke(self, stars):
        """Handle joke rating with comprehensive feedback"""
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
        
        # Enhanced responses for each rating
        if stars == 1:
            response = "Ouch... you hurt my motherboard.. I need therapy now"
            self.show_error_message("Alexa is crying in the corner...")
        elif stars == 2:
            response = "Well that was... an attempt. Back to joke school I go"
            self.show_error_message("Room for improvement, noted!")
        elif stars == 3:
            response = "Not my best work, but I'll take it! Medium rare comedy"
            self.show_error_message("Decent effort!")
        elif stars == 4:
            response = "Hey, I'm getting good at this! Almost professional"
            self.show_error_message("Getting better every day!")
        else:  # 5 stars
            response = "WOOO I'm basically a stand-up comedian now.. Time for my Netflix special!"
            self.play_celebration_sound()

        self.rating_response.config(text=response)

def main():
    root = tk.Tk()
    app = AlexaJokeApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()