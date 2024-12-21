import tkinter as tk
from PIL import Image, ImageTk
import pygame
import human3

class RotatingImageApp:
    def __init__(self, root, image_path, sound_path):
        self.root = root
        self.root.attributes('-fullscreen', True)
        self.root.config(bg="black")
        
        self.original_image = Image.open(image_path).resize((650, 650), Image.LANCZOS)
        self.angle = 0

        pygame.mixer.init()
        self.sound_path = sound_path

        self.canvas = tk.Canvas(self.root, bg="black", highlightthickness=0)
        self.canvas.pack(expand=True, fill='both')

        self.image_id = None
        self.percentage_text = None
        self.loading_percentage = 0

        self.root.bind('<Return>', self.start_loading)

    def start_loading(self, event=None):
        """Handler to start rotating the image, updating the percentage, and playing the sound."""
        pygame.mixer.music.load(self.sound_path)
        pygame.mixer.music.play(-1) 

        self.update_image()
        self.update_loading_percentage()

    def update_image(self):
        rotated_image = self.original_image.rotate(self.angle)
        self.tk_image = ImageTk.PhotoImage(rotated_image)
        
        if self.image_id is None:
            self.image_id = self.canvas.create_image(self.root.winfo_screenwidth() // 2,
                                                     self.root.winfo_screenheight() // 2,
                                                     image=self.tk_image)
        else:
            self.canvas.itemconfig(self.image_id, image=self.tk_image)

        self.angle += 5  
        self.root.after(5, self.update_image)

    def update_loading_percentage(self):
        if self.loading_percentage <= 100:
            if self.percentage_text is None:
                self.percentage_text = self.canvas.create_text(self.root.winfo_screenwidth() // 2,
                self.root.winfo_screenheight() // 2,
                text=f"{self.loading_percentage}%",
                fill="cyan", font=("Recharge Rg", 40, "bold"))
            else:
                self.canvas.itemconfig(self.percentage_text, text=f"{self.loading_percentage}%")

            self.loading_percentage += 1

            self.root.after(20, self.update_loading_percentage)
        else:
            pygame.mixer.music.stop()

            
            self.root.after(1, self.close_and_launch_human_detection)

    def close_and_launch_human_detection(self):
        """Destroy the loading window and launch human2.py"""
        self.root.destroy()

        new_root = tk.Tk()
        human2_app = human3.HumanDetectionApp(new_root)
        new_root.mainloop()
        
        


def start_app(image_path, sound_path):
    root = tk.Tk()
    app = RotatingImageApp(root, image_path, sound_path)
    root.mainloop()

image_path = "loading.png" 
sound_path = "loading.mp3" 
start_app(image_path, sound_path)
