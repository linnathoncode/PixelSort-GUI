from customtkinter import *
from imageUtils import importImage, exportImage
from processImage import processImage
import tkinter as tk
from PIL import Image
#theme
set_appearance_mode("system")
set_default_color_theme("red.json")

MAINFRAMEX = 600 
MAINFRAMEY = 300

NEWWINFRAMEX = 900
NEWWINFRAMEY = 645

#setup
root = CTk()
root.geometry("1280x720")
root.title("Pixel Sort")
root.iconbitmap("pixelsortlogo.ico")

original_image = None
displayed_image = None
processed_image = None
#image frame
image_frame = CTkFrame(root, width=MAINFRAMEX, height=MAINFRAMEY)
image_frame.pack(pady=20, padx=20)   


def getImage():
    global original_image
    global displayed_image

    #if there is already an image imported and user calls tries to import again but not import anything
    #img will countinue to be the already imported image 
    if processed_image:
        img = importImage(processed_image)
    else: 
        img = importImage(original_image)

    original_image = img
    img = displayImage(img, MAINFRAMEX, MAINFRAMEY)
    displayed_image = CTkImage(light_image=img, dark_image=img, size=(img.width,img.height))
    image_label.configure(image=displayed_image)   

def displayImage(img, FRAMEX, FRAMEY):
    
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

        # Resize image while maintaining aspect ratio
        img = img.resize((new_width,new_height), Image.LANCZOS)
        return img


def saveImage():
    if processed_image is None and original_image is not None:
        exportImage(original_image)
    elif processed_image is not None:
        exportImage(processed_image)
    else:
        tk.messagebox.showerror("error", "No image is imported!")

def pixelSort():
    if original_image is not None:
        global processed_image
        processed_image = Image.new(original_image.mode, original_image.size)
        processed_image = processImage(original_image)
        displayImage(processed_image)
    else:
        tk.messagebox.showerror("error", "No image is imported!")

def processWindow():

    newWindow = CTkToplevel(root)

    newWindow.title("Process")

    newWindow.geometry("1280x720")

    newWindow.attributes("-topmost", True)

    process_frame = CTkFrame(newWindow,width=NEWWINFRAMEX, height=NEWWINFRAMEY)
    process_frame.pack(padx=20, pady=20, anchor="w")

    process_label = CTkLabel(master=process_frame, text="")
    process_label.pack(pady=10)
    process_label.place(relx=0.5, rely=0.5, anchor=CENTER)
   
    img = Image.open("goated.jpeg")

    img = displayImage(img, NEWWINFRAMEX, NEWWINFRAMEY)
    process_image = CTkImage(light_image=img, dark_image=img, size=(img.width, img.height))
    process_label.configure(image=process_image)   



import_button = CTkButton(root, width=200, height=40, text="Import Image", 
                          command=getImage)
import_button.pack(pady=10)


export_button = CTkButton(root, width=200, height=40, text="Export Image", 
                          command=saveImage)
export_button.pack(pady=0)


process_image_button = CTkButton(root, width=200, height=40, text="Process Image", 
                          command=processWindow)
process_image_button.pack(pady=10)

image_label = CTkLabel(image_frame, text="")
image_label.pack(pady=10)
image_label.place(relx=0.5, rely=0.5, anchor=CENTER)


#main loop
root.mainloop()
