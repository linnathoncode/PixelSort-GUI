from PIL import Image
from tkinter import filedialog
class ImageHandler:
    def __init__(self):
        self.original_image = None
        self.displayed_image = None
        self.processed_image = None

    def import_image(self):
        if self.processed_image is None:
            self.processed_image = self.original_image
        try:
            file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpeg *.jpg *.png")])
            print(file_path)
            if Image.open(file_path):
                img = Image.open(file_path)
        except:
            return self.processed_image
        self.original_image = img
        self.processed_image =img
        return img

    def export_image(self):
        if self.processed_image is None:
            return False
        try:
            file_path = filedialog.askdirectory()
            file_path += f"/untitled.{self.processed_image.format.lower()}"
            print(file_path)
            self.processed_image.save(file_path)
        except Exception as error:
            print(error)
            return True
        return True

    def get_image_size(self, img, frame_x, frame_y):
        if img is not None:
            img_ratio = img.width / img.height
            frame_ratio = frame_x / frame_y

            if img_ratio > frame_ratio:
                new_width = frame_x
                new_height = int(frame_x / img_ratio)
            else:
                new_height = frame_y
                new_width = int(frame_y * img_ratio)

            resized_img = img.resize((new_width, new_height), Image.LANCZOS)
            return resized_img
        return None

    def process_image(self, process_function):
        if self.original_image is not None:
            self.processed_image = process_function(self.original_image)
        return self.processed_image
