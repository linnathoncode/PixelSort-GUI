from customtkinter import *
from imageUtils import import_image, export_image
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
root.title("Pixel Sort")
root.iconbitmap("pixelsortlogo.ico")

original_image = None
displayed_image = None

#image frame
image_frame = CTkFrame(root, width=FRAMEX, height=FRAMEY)
image_frame.pack(pady=20, padx=20)   

def display_image():
    global original_image
    global displayed_image
    img = import_image()
    original_image = img

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

def save_image():
    if displayed_image or original_image is not None:
        export_image(original_image)
    else:
        tk.messagebox.showerror("error", "No image is imported!")

def get_pixels():
    #getting the HSV value
    test_image = original_image.convert('HSV')
    image_pixels = list(test_image.getdata())

    #extract only saturation values
    image_pixels_saturation = [t[1] for t in image_pixels]
    print(image_pixels_saturation)


import_button = CTkButton(root, width=200, height=40, text="Import Image", 
                          command=display_image)
import_button.pack(pady=10)


export_button = CTkButton(root, width=200, height=40, text="Export Image", 
                          command=save_image)
export_button.pack(pady=0)


process_image_button = CTkButton(root, width=200, height=40, text="Process Image", 
                          command=get_pixels)
process_image_button.pack(pady=10)

image_label = CTkLabel(image_frame, text="")
image_label.pack(pady=10)
image_label.place(relx=0.5, rely=0.5, anchor=CENTER)


#main loop
root.mainloop()
