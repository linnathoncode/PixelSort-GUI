from PIL import Image
from tkinter import filedialog
from customtkinter import *
class ImageHandler:
    def __init__(self):
        self.original_image = None
        self.displayed_image = None
        self.processed_image = None
        self.image_mode = None
        self.image_format = None
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
            #print(error)
            return True
        return True

    def get_image_size(self, img, frame_x, frame_y):
        # Returns the image sizes that fits to the given frame sizes
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

    def process_image(self):
        if self.original_image is not None:
            on_process_img = self.original_image
            on_process_img = self.pixelsort()
        return on_process_img

    def save_changes(self, on_process):
        self.processed_image = on_process

    def display_image(self, img, frame_x, frame_y, image_label):
        # Creates a duplicate image with the adjusted size and displays it 
        resized_img = self.get_image_size(img, frame_x, frame_y)
        self.displayed_image = CTkImage(light_image=resized_img, dark_image=resized_img, size=(resized_img.width, resized_img.height))
        image_label.configure(image=self.displayed_image)
    
    def pixelsort(self):

        self.image_mode = self.original_image.mode
        self.image_format =self.original_image.format

        #convert the image to HSV mode
        on_process_image = self.original_image.convert('HSV')
        
        #get the pixel data
        on_process_image_pixels = list(on_process_image.getdata())

        #sort the pixels by the second value (Saturation) in ascending/descending orden
        #reverse -> false ascending, true descending
        sorted_image_pixels = sorted(on_process_image_pixels, key=lambda x: x[1], reverse=False)

        #create a new image with the same mode and size
        sorted_image = Image.new('HSV', on_process_image.size)
        
        #put the sorted pixel data into the new image
        sorted_image.putdata(sorted_image_pixels)
        
        #convert the image back to its original mode
        final_image = sorted_image.convert(self.image_mode)

        #convert back to original format 
        final_image.format = self.image_format
        
        return final_image
