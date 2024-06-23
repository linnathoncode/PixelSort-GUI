from customtkinter import *
from imageUtils import import_image
import tkinter as tk
from PIL import Image
#theme
set_appearance_mode("light")
set_default_color_theme("red.json")

FRAMEX = 600 
FRAMEY = 300


#setup
root = CTk()
root.geometry("1280x720")

#image frame
image_frame = CTkFrame(root, width=FRAMEX, height=FRAMEY)
image_frame.pack(pady=20, padx=20)   

def display_image():
    img = import_image()
    #this img will be used afterwards

    if img is not None:
        #aspect ratios
        img_ratio = img.width/img.height
        frame_ratio = FRAMEX/FRAMEY

        #image is wider than the frame
        if img_ratio > frame_ratio:

            new_width =FRAMEX
            new_height = int(FRAMEX*img_ratio)
        #image is taller than the frame
        else:
            new_height =FRAMEY
            new_width = int(FRAMEY*img_ratio)
            

    img = img.resize((new_width,new_height), Image.LANCZOS)
    displayed_image= CTkImage(light_image=img, dark_image=img, size=(new_width,new_height))
    image_label.configure(image=displayed_image)
 # Resize image while maintaining aspect ratio


import_button = CTkButton(root, width=200, height=40, text="Import Image", command=display_image)
import_button.pack(pady=100)

image_label = CTkLabel(image_frame, text="")
image_label.pack(pady=10)
image_label.place(relx=0.5, rely=0.5, anchor=CENTER)


#main loop
root.mainloop()
