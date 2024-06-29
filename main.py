from customtkinter import *
from imageUtils import importImage, exportImage
from processImage import processImage
from tkinter import messagebox 
from PIL import Image
#theme
set_appearance_mode("light")
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

image_label = CTkLabel(master=image_frame, text="")
image_label.pack(pady=10)
image_label.place(relx=0.5, rely=0.5, anchor=CENTER)

def getImage():
    global original_image
    global displayed_image
    global processed_image

    #if there is already an image imported and user calls tries to import again but not import anything
    #img will countinue to be the already imported image 
    if processed_image:
        img = importImage(processed_image)
    else: 
        img = importImage(original_image)

    original_image = img
    return img

def displayImage(img):
    displayed_image = getImageSize(img, MAINFRAMEX, MAINFRAMEY)
    displayed_image = CTkImage(light_image=displayed_image, dark_image=displayed_image, size=(displayed_image.width,displayed_image.height))
    image_label.configure(image=displayed_image)   

def getImageSize(img, FRAMEX, FRAMEY):
    
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
        messagebox.showerror("error", "No image is imported!")


    
def processWindow():
    if original_image is not None:
        on_process_image = original_image
        #window setup
        newWindow = CTkToplevel(root)
        newWindow.title("Process")
        newWindow.geometry("1280x720")
        newWindow.attributes("-topmost", True)

        #frame & label setup
        process_frame = CTkFrame(newWindow,width=NEWWINFRAMEX, height=NEWWINFRAMEY)
        process_frame.grid(row=0, column=0, pady=20,padx=20, sticky='w')

        process_label = CTkLabel(master=process_frame, text="")
        process_label.grid(row=0, column=0)
        process_label.place(relx=0.5, rely=0.5, anchor=CENTER)
        processWinDisplay(process_label, original_image)

        def pixelSort():
            on_process_image = Image.new(original_image.mode, original_image.size)
            on_process_image = processImage(original_image)
            processWinDisplay(process_label, on_process_image)

        def saveChanges():
            global processed_image
            #saves the changes made to the image
            processed_image = on_process_image
            #displayes the image on the main menu
            displayImage(processed_image)
           # messagebox.showerror("", "Changes have been saved!")

        #button & sliders frame
        preferences_frame = CTkFrame(newWindow, width=300, height=720)

        #process button
        process_image_button = CTkButton(master=preferences_frame, width=200, height=40, text="Process Image", 
                          command=pixelSort)
        process_image_button.pack(pady=10, padx=20)

        #save changes button
        save_changes_button = CTkButton(master=preferences_frame, width=200, height=40, text="Save Changes", 
                          command=saveChanges)
        save_changes_button.pack(pady=10)

        preferences_frame.grid(pady=20, padx=20,row=0, column=1, sticky="n")

    else:
        messagebox.showerror("error", "No image is imported!")

def processWinDisplay(process_label, img):
    img = getImageSize(img, NEWWINFRAMEX, NEWWINFRAMEY)
    process_image = CTkImage(light_image=img, dark_image=img, size=(img.width, img.height))
    process_label.configure(image=process_image)   




import_button = CTkButton(root, width=200, height=40, text="Import Image", 
                          command=lambda: [displayImage(getImage())])
import_button.pack(pady=10)


export_button = CTkButton(root, width=200, height=40, text="Export Image", 
                          command=saveImage)
export_button.pack(pady=0)


process_image_button = CTkButton(root, width=200, height=40, text="Process Image", 
                          command=processWindow)
process_image_button.pack(pady=10)




#main loop
root.mainloop()
