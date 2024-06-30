from customtkinter import *
from tkinter import messagebox
from imageUtils import ImageHandler
from processImage import processImage
from PIL import Image

# Theme
set_appearance_mode("light")
set_default_color_theme("red.json")

MAINFRAMEX = 600 
MAINFRAMEY = 300

NEWWINFRAMEX = 900
NEWWINFRAMEY = 645

# Setup
root = CTk()
root.geometry("1280x720")
root.title("Pixel Sort")
root.iconbitmap("pixelsortlogo.ico")

# Image handler instance
image_handler = ImageHandler()

# Image frame
image_frame = CTkFrame(root, width=MAINFRAMEX, height=MAINFRAMEY)
image_frame.pack(pady=20, padx=20)   

image_label = CTkLabel(master=image_frame, text="")
image_label.pack(pady=10)
image_label.place(relx=0.5, rely=0.5, anchor=CENTER)

def displayImage(img):
    resized_img = image_handler.get_image_size(img, MAINFRAMEX, MAINFRAMEY)
    displayed_image = CTkImage(light_image=resized_img, dark_image=resized_img, size=(resized_img.width, resized_img.height))
    image_label.configure(image=displayed_image)

def saveImage():
    if not image_handler.export_image():
        messagebox.showerror("error", "No image is imported!")

def processWindow():
    if image_handler.original_image is not None:
        on_process_image = image_handler.original_image
        # Window setup
        newWindow = CTkToplevel(root)
        newWindow.title("Process")
        newWindow.geometry("1280x720")
        newWindow.attributes("-topmost", True)

        # Frame & label setup
        process_frame = CTkFrame(newWindow, width=NEWWINFRAMEX, height=NEWWINFRAMEY)
        process_frame.grid(row=0, column=0, pady=20, padx=20, sticky='w')

        process_label = CTkLabel(master=process_frame, text="")
        process_label.grid(row=0, column=0)
        process_label.place(relx=0.5, rely=0.5, anchor=CENTER)
        processWinDisplay(process_label, image_handler.original_image)

        def pixelSort():
            image_handler.process_image(processImage)
            processWinDisplay(process_label, image_handler.processed_image)

        def saveChanges():
            displayImage(image_handler.processed_image)

        # Button & sliders frame
        preferences_frame = CTkFrame(newWindow, width=300, height=720)

        # Process button
        process_image_button = CTkButton(master=preferences_frame, width=200, height=40, text="Process Image", 
                                         command=pixelSort)
        process_image_button.pack(pady=10, padx=20)

        # Save changes button
        save_changes_button = CTkButton(master=preferences_frame, width=200, height=40, text="Save Changes", 
                                        command=saveChanges)
        save_changes_button.pack(pady=10)

        preferences_frame.grid(pady=20, padx=20, row=0, column=1, sticky="n")

    else:
        messagebox.showerror("error", "No image is imported!")

def processWinDisplay(process_label, img):
    img = image_handler.get_image_size(img, NEWWINFRAMEX, NEWWINFRAMEY)
    process_image = CTkImage(light_image=img, dark_image=img, size=(img.width, img.height))
    process_label.configure(image=process_image)

import_button = CTkButton(root, width=200, height=40, text="Import Image", 
                          command=lambda:(displayImage(image_handler.import_image())))
import_button.pack(pady=10)

export_button = CTkButton(root, width=200, height=40, text="Export Image", 
                          command=saveImage)
export_button.pack(pady=0)

process_image_button = CTkButton(root, width=200, height=40, text="Process Image", 
                                 command=processWindow)
process_image_button.pack(pady=10)

# Main loop
root.mainloop()
