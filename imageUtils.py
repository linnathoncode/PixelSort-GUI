from PIL import Image
from tkinter import filedialog

def import_image():
    try:
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpeg *.jpg *.png")])
        img = Image.open(file_path)
    except:
        return None
    return img

def export_image(img):
    try:
        file_path =filedialog.askdirectory()
        file_path+= f"/untitled.{(img.format).lower()}" 
        #print(file_path)
        img.save(file_path)
    except:
        pass