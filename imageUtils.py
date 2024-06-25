from PIL import Image
from tkinter import filedialog

def importImage():
    try:
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpeg *.jpg *.png")])
        img = Image.open(file_path)
    except:
        return None
    return img

def exportImage(img):
    try:
        file_path =filedialog.askdirectory()
        file_path+= f"/untitled.{(img.format).lower()}" 
        print(file_path)
        img.save(file_path)
    except Exception as error:
        print(error)
        