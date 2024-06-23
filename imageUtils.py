from PIL import Image
from tkinter import filedialog

def import_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpeg *.jpg *.png")])
    if file_path:
        img = Image.open(file_path)
        return img

