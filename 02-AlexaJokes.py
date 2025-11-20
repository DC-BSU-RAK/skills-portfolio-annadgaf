"""
Alexa Joke Teller Application
A Tkinter-based GUI application that tells random jokes with interactive features.

Features:
- Welcome screen with styled entry point
- Random joke selection from file with fallback system
- Setup and punchline display with timing control
- 5-star rating system with humorous responses
- Multiple sound effects for punchlines and celebrations
- Background images that change during joke delivery
- Surprise mode with unexpected content
- Comprehensive error handling and user feedback
- Elegant purple-themed UI with consistent styling

File Structure:
Assessment 1 - Skills Portfolio/
├── A1 - Resources/
│   ├── randomJokes.txt          # Joke database
│   ├── Photos/
│   │   ├── neutral.png          # Default background image
│   │   └── cry.png              # Punchline reaction image
│   └── Sounds/
│       ├── 57814__timtube__laughing-9.wav
│       ├── 324184__kwahmah_02__applause-05.wav
│       ├── 352789__vintprox__cricket.ogg
│       ├── 656732__paladinvii__fbi-open-up-pvii.mp3
│       └── 581410__audiosea__crowd-wow-sound-effect-1.wav

Author: [Your Name]
Date: [Current Date]
Course: Programming Skills Portfolio
"""

import tkinter as tk
from tkinter import ttk
import random
from pathlib import Path
import pygame
from PIL import Image, ImageTk
import os

class AlexaJokeApp:
    """
    Main application class for Alexa Joke Teller.
    
    This class manages the entire application lifecycle including:
    - GUI setup and management
    - Joke loading and delivery
    - Sound and image handling
    - User interaction processing
    - Error handling and fallback systems
    """
    
    def __init__(self, root):
        """
        Initialize the Alexa Joke Teller application.
        
        Args:
            root (tk.Tk): The main Tkinter root window
        """
        self.root = root
        self.root.title("Alexa's Joke Corner")
        self.root.geometry("700x600")
        self.root.configure(bg='#f8f4ff')
        
        # Initialize pygame for sound playback
        pygame.mixer.init()
        
        # Color scheme for consistent purple theme
        self.colors = {
            'bg': '#f8f4ff',          # Main background color
            'accent': '#e6e0ff',      # Secondary background
            'accent2': '#f0ebff',     # Content area background
            'text': '#4a2c6d',        # Primary text color
            'button': '#8a2be2',      # Main button color
            'button_hover': '#6a0dad', # Button hover state
            'star_active': '#ffd700',  # Active star rating
            'star_inactive': '#d3d3d3' # Inactive star rating
        }
        
        # Initialize media storage
        self.sounds = {}    # Dictionary for sound effects
        self.images = {}    # Dictionary for background images
        
        # Load external resources
        self.load_sounds()
        self.load_images()
        
        # Application state variables
        self.jokes = []              # Loaded jokes list
        self.current_joke = None     # Currently displayed joke
        self.punchline_shown = False # Punchline visibility state
        self.rating_given = False    # Rating submission state
        self.joke_count = 0          # Joke delivery counter
        self.surprise_triggered = False # Surprise mode state
        
        # Load joke database
        self.load_jokes()
        
        # Start application with welcome screen
        self.show_welcome_screen()

    def load_images(self):
        """
        Load background images from Photos directory.
        
        Handles missing files gracefully and provides error feedback.
        Supports PNG format with automatic resizing for display.
        """
        try:
            photos_path = Path("Assessment 1 - Skills Portfolio/A1 - Resources/Photos")
            
            # Check if photos directory exists
            if not photos_path.exists():
                self.show_welcome_error("Images folder not found - running without images")
                return
            
            # Load neutral background image
            neutral_path = photos_path / "neutral.png"
            if neutral_path.exists():
                image = Image.open(neutral_path)
                image = image.resize((200, 150), Image.LANCZOS)  # Optimize for display
                self.images['neutral'] = ImageTk.PhotoImage(image)
                print("Loaded neutral.png successfully")
            else:
                print("neutral.png not found in Photos folder")
            
            # Load cry reaction image for punchlines
            cry_path = photos_path / "cry.png"
            if cry_path.exists():
                image = Image.open(cry_path)
                image = image.resize((200, 150), Image.LANCZOS)  # Consistent sizing
                self.images['cry'] = ImageTk.PhotoImage(image)
                print("Loaded cry.png successfully")
            else:
                print("cry.png not found in Photos folder")
                
        except Exception as e:
            print(f"Image loading error: {e}")
            self.show_welcome_error("Error loading images - continuing without them")

    def show_welcome_error(self, message):
        """
        Store error message for display after GUI initialization.
        
        Args:
            message (str): Error message to display to user
        """
        if hasattr(self, 'pending_error'):
            self.pending_error += f" | {message}"
        else:
            self.pending_error = message

    def load_sounds(self):
        """
        Load sound effects from Sounds directory.
        
        Supports multiple audio formats (WAV, OGG, MP3) and provides
        comprehensive error reporting for missing or corrupted files.
        Creates fallback sounds if no files are available.
        """
        try:
            sound_path = Path("Assessment 1 - Skills Portfolio/A1 - Resources/Sounds")
            
            # Verify sounds directory exists
            if not sound_path.exists():
                self.show_welcome_error("Sounds folder not found - using fallback sounds")
                self.create_fallback_sounds()
                return
            
            # Define expected sound files and their categories
            sound_files = {
                'laughter': "57814__timtube__laughing-9.wav",
                'applause': "324184__kwahmah_02__applause-05.wav",
                'cricket': "352789__vintprox__cricket.ogg",
                'fbi': "656732__paladinvii__fbi-open-up-pvii.mp3",
                'crowd_wow': "581410__audiosea__crowd-wow-sound-effect-1.wav"
            }
            
            loaded_sounds = 0
            missing_sounds = []
            
            # Attempt to load each sound file
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
            
            # Report loading results
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
        """
        Generate simple fallback sounds using pygame buffer.
        
        Provides basic audio feedback when sound files are unavailable.
        These are simple generated tones that serve as placeholders.
        """
        try:
            # Create basic tone-based fallback sounds
            self.sounds['laughter'] = pygame.mixer.Sound(buffer=bytes([100] * 512))
            self.sounds['applause'] = pygame.mixer.Sound(buffer=bytes([150] * 512))
            self.sounds['crowd_wow'] = pygame.mixer.Sound(buffer=bytes([200] * 512))
            print("Created fallback sounds")
        except:
            print("Failed to create fallback sounds")
            # Set to None if sound creation fails
            self.sounds['laughter'] = None
            self.sounds['applause'] = None
            self.sounds['crowd_wow'] = None

    def load_jokes(self):
        """
        Load jokes from randomJokes.txt file.
        
        Parses the joke file, validates format, and provides comprehensive
        error handling for file access and format issues.
        """
        try:
            file_path = Path("Assessment 1 - Skills Portfolio/A1 - Resources/randomJokes.txt")
            
            # Check if joke file exists
            if not file_path.exists():
                self.show_welcome_error("Joke file not found - using backup jokes")
                self.jokes = self.get_fallback_jokes()
                return
            
            # Read and parse joke file
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = [line.strip() for line in file if line.strip()]
                # Filter for valid jokes (must contain question mark)
                self.jokes = [line for line in lines if '?' in line]
            
            # Validate that jokes were loaded
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
        """
        Provide curated fallback jokes when file loading fails.
        
        Returns:
            list: Pre-defined jokes as backup content
        """
        return [
            "Why did the scarecrow win an award?~He was outstanding in his field!",
            "What do you call a fake noodle?~An impasta!",
            "Why don't scientists trust atoms?~Because they make up everything!",
            "What do you call a sleeping bull?~A bulldozer!",
            "Why did the coffee file a police report?~It got mugged!"
        ]

    def show_welcome_screen(self):
        """
        Display the welcome screen with application entry point.
        
        Creates an inviting initial interface with error display
        capabilities for resource loading issues.
        """
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Create welcome frame
        welcome_frame = tk.Frame(self.root, bg=self.colors['bg'])
        welcome_frame.pack(expand=True, fill='both')
        
        # Application title
        title_label = tk.Label(
            welcome_frame,
            text="Alexa's Humor",
            font=("Georgia", 32, "bold"),
            fg=self.colors['text'],
            bg=self.colors['bg']
        )
        title_label.pack(pady=80)
        
        # Main entry button
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
        
        # Error display area for loading issues
        self.welcome_error_label = tk.Label(
            welcome_frame,
            text="",
            font=("Verdana", 9),
            fg='#d27979',
            bg=self.colors['bg'],
            wraplength=500
        )
        self.welcome_error_label.pack(pady=10)
        
        # Display any loading errors
        if hasattr(self, 'pending_error'):
            self.welcome_error_label.config(text=f"Note: {self.pending_error}")
        
        # Button hover effects
        def on_enter(e):
            start_btn['bg'] = self.colors['button']
            start_btn['fg'] = 'white'
        def on_leave(e):
            start_btn['bg'] = '#f0ebff'
            start_btn['fg'] = self.colors['text']
            
        start_btn.bind("<Enter>", on_enter)
        start_btn.bind("<Leave>", on_leave)

    def setup_gui(self):
        """
        Initialize the main application interface.
        
        Creates all GUI components including joke display area,
        control buttons, rating system, and status feedback.
        """
        # Clear welcome screen
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main application frame
        main_frame = tk.Frame(self.root, bg=self.colors['bg'], padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Application title
        title_label = tk.Label(
            main_frame, 
            text="Alexa's Joke Corner", 
            font=("Georgia", 20, "bold"),
            fg=self.colors['text'],
            bg=self.colors['bg']
        )
        title_label.pack(pady=20)
        
        # Joke display area
        self.joke_frame = tk.Frame(
            main_frame, 
            bg=self.colors['accent2'], 
            padx=20, 
            pady=20
        )
        self.joke_frame.pack(fill='both', expand=True, pady=20)
        
        # Joke setup text display
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
        
        # Joke punchline display
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
        
        # Rating system components
        self.setup_rating_system()
        
        # Control buttons
        self.setup_control_buttons(main_frame)
        
        # Status feedback system
        self.setup_status_system(main_frame)
        
        # Image display area
        self.setup_image_display(main_frame)
        
        # Initialize button states
        self.punchline_btn.config(state='disabled')
        self.rate_btn.config(state='disabled')
        
        # Start with first joke
        self.show_new_joke()

    def setup_rating_system(self):
        """Initialize the 5-star rating interface components."""
        self.rating_frame = tk.Frame(self.joke_frame, bg=self.colors['accent2'])
        
        # Rating prompt
        self.rating_label = tk.Label(
            self.rating_frame,
            text="Rate this joke:",
            font=("Verdana", 10),
            fg=self.colors['text'],
            bg=self.colors['accent2']
        )
        self.rating_label.pack(pady=(10, 5))
        
        # Star rating buttons
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
            # Bind click event to rating function
            star.bind('<Button-1>', lambda e, idx=i: self.rate_joke(idx + 1))
            self.star_buttons.append(star)
        
        # Rating response display
        self.rating_response = tk.Label(
            self.rating_frame,
            text="",
            font=("Verdana", 9, "italic"),
            fg=self.colors['text'],
            bg=self.colors['accent2']
        )
        self.rating_response.pack(pady=5)

    def setup_control_buttons(self, parent):
        """Create and arrange the main control buttons."""
        button_frame = tk.Frame(parent, bg=self.colors['bg'])
        button_frame.pack(pady=10)
        
        # Primary action buttons
        self.punchline_btn = self.create_button(button_frame, "Show Punchline", self.show_punchline)
        self.punchline_btn.pack(side='left', padx=5)
        
        self.next_joke_btn = self.create_button(button_frame, "Next Joke", self.show_new_joke)
        self.next_joke_btn.pack(side='left', padx=5)
        
        self.rate_btn = self.create_button(button_frame, "Rate my Joke", self.show_rating)
        self.rate_btn.pack(side='left', padx=5)
        
        # Special features
        self.surprise_btn = self.create_button(button_frame, "Surprise Me", self.activate_surprise_mode)
        self.surprise_btn.pack(side='left', padx=5)
        
        # Application exit
        quit_btn = self.create_button(parent, "Quit", self.root.quit, '#f0ebff')
        quit_btn.pack(pady=10)

    def setup_status_system(self, parent):
        """Initialize the status message display system."""
        self.status_label = tk.Label(
            parent,
            text="",
            font=("Verdana", 8, "italic"),
            fg='#666666',
            bg=self.colors['bg']
        )
        self.status_label.pack(pady=5)

    def setup_image_display(self, parent):
        """Setup the background image display area."""
        self.image_label = tk.Label(parent, bg=self.colors['bg'])
        self.image_label.pack(pady=10)
        
        # Show default image if available
        if 'neutral' in self.images:
            self.image_label.config(image=self.images['neutral'])
        else:
            self.image_label.config(text="[Images not available]", fg='#999999')

    def create_button(self, parent, text, command, color=None):
        """
        Create a consistently styled button with hover effects.
        
        Args:
            parent: Parent widget for the button
            text (str): Button display text
            command: Function to call on button click
            color (str, optional): Custom background color
            
        Returns:
            tk.Button: Configured button widget
        """
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
        
        # Hover effect handlers
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
        """
        Display temporary status messages to the user.
        
        Args:
            message (str): Message to display
        """
        if hasattr(self, 'status_label'):
            self.status_label.config(text=message)
            # Clear message after 4 seconds
            self.root.after(4000, lambda: self.status_label.config(text=""))

    def play_punchline_sound(self):
        """Play a randomly selected sound effect for punchline delivery."""
        try:
            sound_options = ['laughter', 'cricket', 'fbi']
            available_sounds = [s for s in sound_options if s in self.sounds and self.sounds[s]]
            
            if available_sounds:
                selected_sound = random.choice(available_sounds)
                self.sounds[selected_sound].play()
                
                # Contextual feedback messages
                if selected_sound == 'laughter':
                    self.show_error_message("HAHAHA! LOL!")
                elif selected_sound == 'cricket':
                    self.show_error_message("*cricket sounds* ...tough crowd!")
                elif selected_sound == 'fbi':
                    self.show_error_message("That joke was criminal!")
            else:
                self.show_error_message("Ba-dum-tss! (Sound effects unavailable)")
                
        except Exception as e:
            self.show_error_message("Audience reaction! (Sound error)")

    def play_celebration_sound(self):
        """Play celebration sound for 5-star ratings."""
        try:
            # Priority: crowd wow -> applause -> fallback
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

    def activate_surprise_mode(self):
        """
        Activate surprise mode with unexpected content.
        
        Replaces normal joke delivery with various surprise types
        including anti-jokes, philosophical content, and meta-humor.
        """
        self.surprise_triggered = True
        
        # Reset application state
        self.punchline_shown = False
        self.rating_given = False
        self.rating_frame.pack_forget()
        self.rating_response.config(text="")
        
        # Reset visual display
        if 'neutral' in self.images:
            self.image_label.config(image=self.images['neutral'])
        
        # Select and execute random surprise type
        surprises = [
            self.surprise_anti_joke,
            self.surprise_philosophical,
            self.surprise_meta,
            self.surprise_technical,
            self.surprise_emotional
        ]
        
        random.choice(surprises)()
        
        # Update button states
        self.punchline_btn.config(state='normal')
        self.rate_btn.config(state='disabled')
        
        # Reset star ratings
        for star in self.star_buttons:
            star.config(fg=self.colors['star_inactive'])

    def surprise_anti_joke(self):
        """Deliver an anti-joke that subverts comedy expectations."""
        anti_jokes = [
            "Why did the chicken cross the road?~To get to the other side. Seriously, that's it.",
            "What's the difference between a piano?~The piano can play music, but you can't tuna fish.",
            "Why was the math book sad?~It had too many problems. And I'm not joking."
        ]
        setup, punchline = random.choice(anti_jokes).split('~')
        self.setup_label.config(text=setup)
        self.punchline_label.config(text="")
        self.current_punchline = punchline
        self.show_error_message("Surprise! Anti-humor activated!")

    def surprise_philosophical(self):
        """Deliver philosophical content instead of a joke."""
        philosophical = [
            "What is the sound of one hand clapping?~It's the same sound as a tree falling in an empty forest.",
            "Why do we exist?~To tell bad jokes, apparently.",
            "What is the meaning of life?~42. And bad puns."
        ]
        setup, punchline = random.choice(philosophical).split('~')
        self.setup_label.config(text=setup)
        self.punchline_label.config(text="")
        self.current_punchline = punchline
        self.show_error_message("Deep thoughts incoming...")

    def surprise_meta(self):
        """Deliver meta-content about the application itself."""
        meta_jokes = [
            "Why didn't the joke work?~Because you're reading this instead of laughing.",
            "What do you call a joke that explains itself?~This one.",
            "Why am I telling you this?~Because the programmer thought it would be funny."
        ]
        setup, punchline = random.choice(meta_jokes).split('~')
        self.setup_label.config(text=setup)
        self.punchline_label.config(text="")
        self.current_punchline = punchline
        self.show_error_message("Meta-humor engaged!")

    def surprise_technical(self):
        """Deliver programming and technology-themed content."""
        technical = [
            "Why did the Python programmer get rejected?~Because he couldn't C# well enough.",
            "What's a programmer's favorite place?~The Foo Bar.",
            "Why do programmers prefer dark mode?~Because light attracts bugs."
        ]
        setup, punchline = random.choice(technical).split('~')
        self.setup_label.config(text=setup)
        self.punchline_label.config(text="")
        self.current_punchline = punchline
        self.show_error_message("Technical difficulties... just kidding!")

    def surprise_emotional(self):
        """Deliver emotionally engaging content."""
        emotional = [
            "Are you proud of me?~I try my best to make you smile!",
            "Do you think I'm funny?~I hope so, otherwise this is awkward...",
            "Can we be friends?~I'd like that! Even if my jokes are bad."
        ]
        setup, punchline = random.choice(emotional).split('~')
        self.setup_label.config(text=setup)
        self.punchline_label.config(text="")
        self.current_punchline = punchline
        self.show_error_message("Emotional connection established!")

    def show_new_joke(self):
        """
        Display a new random joke with automatic surprise chance.
        
        Includes 1 in 15 chance of automatic surprise activation
        and comprehensive state management.
        """
        # Random surprise activation (1 in 15 chance)
        if random.randint(1, 15) == 1 and not self.surprise_triggered:
            self.activate_surprise_mode()
            return
        
        self.surprise_triggered = False
        
        # Prevent rapid joke skipping
        if self.joke_count > 0 and not self.punchline_shown:
            self.show_error_message("Greedy for jokes huh?? At least let me finish!")
            return
        
        # Reset application state
        self.punchline_shown = False
        self.rating_given = False
        self.rating_frame.pack_forget()
        self.rating_response.config(text="")
        
        # Reset visual display
        if 'neutral' in self.images:
            self.image_label.config(image=self.images['neutral'])
        
        # Handle empty joke list
        if not self.jokes:
            self.show_error_message("No jokes available! Check your joke file.")
            self.setup_label.config(text="No jokes loaded. Please check the randomJokes.txt file.")
            self.punchline_btn.config(state='disabled')
            return
        
        # Select and parse random joke
        self.current_joke = random.choice(self.jokes)
        if '?' in self.current_joke:
            setup, punchline = self.current_joke.split('?', 1)
            setup = setup.strip() + "?"
            punchline = punchline.strip()
        else:
            setup = self.current_joke
            punchline = "Punchline missing! Alexa is having a moment..."
        
        # Update display
        self.current_setup = setup
        self.current_punchline = punchline
        self.setup_label.config(text=setup)
        self.punchline_label.config(text="")
        self.punchline_btn.config(state='normal')
        self.rate_btn.config(state='disabled')
        
        # Reset rating display
        for star in self.star_buttons:
            star.config(fg=self.colors['star_inactive'])
        
        self.joke_count += 1

    def show_punchline(self):
        """
        Display the current joke's punchline.
        
        Includes comprehensive validation to prevent user errors
        and manages associated sound and visual effects.
        """
        # Validation checks
        if not hasattr(self, 'current_punchline'):
            self.show_error_message("Error: No joke loaded. Try 'Next Joke' first.")
            return
        
        if self.punchline_shown:
            self.show_error_message("Patience! Already showed you the punchline!")
            return
        
        # Display punchline
        self.punchline_label.config(text=self.current_punchline)
        self.punchline_shown = True
        self.rate_btn.config(state='normal')
        
        # Play sound effect and update image
        self.play_punchline_sound()
        if 'cry' in self.images:
            self.image_label.config(image=self.images['cry'])

    def show_rating(self):
        """
        Display the rating interface.
        
        Validates that punchline has been shown before allowing ratings
        to ensure informed voting.
        """
        if not self.punchline_shown:
            self.show_error_message("Can't rate what you haven't seen! Show the punchline first.")
            return
        
        if self.rating_given:
            self.show_error_message("You already rated this masterpiece!")
            return
        
        self.rating_frame.pack(pady=10)
        self.show_error_message("Let me know how I did!")

    def rate_joke(self, stars):
        """
        Process joke rating and provide humorous feedback.
        
        Args:
            stars (int): Number of stars rated (1-5)
        """
        if self.rating_given:
            self.show_error_message("You already rated this one! Make up your mind!")
            return
        
        self.rating_given = True
        
        # Update star visual feedback
        for i, star in enumerate(self.star_buttons):
            if i < stars:
                star.config(fg=self.colors['star_active'])
            else:
                star.config(fg=self.colors['star_inactive'])
        
        # Provide contextual response based on rating
        if stars == 1:
            response = "Ouch... you hurt my motherboard.. I need therapy now"
            self.show_error_message("Alexa is crying in the corner...")
        elif stars == 2:
            response = "Well that was... an attempt.."
            self.show_error_message("Room for improvement, noted!")
        elif stars == 3:
            response = "Not my best work, but I'll take it! Medium rare comedy"
            self.show_error_message("Decent effort!")
        elif stars == 4:
            response = "Hey, I'm getting good at this! Almost professional"
            self.show_error_message("Getting better every day!")
        else:  # 5 stars
            response = "WOOO I'm basically a stand-up comedian now.."
            self.play_celebration_sound()

        self.rating_response.config(text=response)


def main():
    """
    Main application entry point.
    
    Initializes Tkinter and starts the Alexa Joke Teller application.
    """
    root = tk.Tk()
    app = AlexaJokeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()