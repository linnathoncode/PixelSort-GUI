from PIL import Image
from tkinter import filedialog

def import_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpeg *.jpg *.png")])
    if file_path:
        img = Image.open(file_path)
        return img

def export_image(img):
    file_path =filedialog.askdirectory()
    file_path+= f"/untitled.{(img.format).lower()}" 
    print(file_path)
    img.save(file_path)
