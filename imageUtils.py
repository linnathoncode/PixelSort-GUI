from PIL import Image
from tkinter import filedialog

def importImage(old_image):
    try:
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpeg *.jpg *.png")])
        print(file_path)
        if Image.open(file_path):
            img = Image.open(file_path)
    except:
        return old_image
    return img

def exportImage(img):
    try:
        file_path =filedialog.askdirectory()
        file_path+= f"/untitled.{(img.format).lower()}" 
        print(file_path)
        img.save(file_path)
    except Exception as error:
        print(error)
        