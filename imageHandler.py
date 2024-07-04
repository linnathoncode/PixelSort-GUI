from PIL import Image
from tkinter import filedialog
from customtkinter import *
from concurrent.futures import ThreadPoolExecutor

class ImageHandler:
    def __init__(self, main_app):
        self.original_image = None
        self.displayed_image = None
        self.processed_image = None
        self.image_mode = None
        self.image_format = None
        self.main_app = main_app

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
            file_path = filedialog.asksaveasfilename(initialdir="C:\Desktop", filetypes=[("Image files", "*.jpeg *.jpg *.png")])
            file_path = f"{file_path}.{(self.processed_image.format).lower()}"
            self.processed_image.save(file_path)
        except Exception as error:
            #print(error)
            return True
        print(file_path)
        return True

    def get_adjusted_image_size(self, img, frame_x, frame_y):
        # Returns the image sizes that fit to the given frame sizes
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

    def process_image(self, mode_threshold):
        if self.original_image is not None:
            on_process_img = self.original_image
            on_process_img = self.pixelsort(mode_threshold, True, self.main_app.mode_index)
        return on_process_img

    def save_changes(self, on_process):
        self.processed_image = on_process

    def display_image(self, img, frame_x, frame_y, image_label):
        # Creates a duplicate image with the adjusted size and displays it 
        resized_img = self.get_adjusted_image_size(img, frame_x, frame_y)
        self.displayed_image = CTkImage(light_image=resized_img, dark_image=resized_img, size=(resized_img.width, resized_img.height))
        image_label.configure(image=self.displayed_image)
    
    def pixelsort(self, threshold, sort_above_threshold, mode_index):
        self.image_mode = self.original_image.mode
        self.image_format = self.original_image.format

        # Convert the image to given mode
        # ex ("Hue", "HSV", 0, 0) name, mode, position, threshold
        on_process_image = self.original_image.convert(self.main_app.modes_list[mode_index][1])
        
        # Get the pixel data
        on_process_image_pixels = list(on_process_image.getdata())

        # Separate pixels into chunks based on the saturation threshold
        chunk = []
        non_chunk = []
        sorted_image_pixels = []
        index = 0

        # It works in individual chunks now but creates glitchy images because of the use of multithreading
        # it can be implemented as a glitch effect later
        # with ThreadPoolExecutor() as executor:
        #     futures = []
        #     while index < len(on_process_image_pixels):
        #         # Chunk is the chunk of pixels that will be sorted
        #         while index < len(on_process_image_pixels) and ((sort_above_threshold and on_process_image_pixels[index][1] > threshold) or (not sort_above_threshold and on_process_image_pixels[index][1] < threshold)):
        #             chunk.append(on_process_image_pixels[index])
        #             index += 1

        #         if chunk:
        #             # Sort the chunk using a separate thread
        #             futures.append(executor.submit(self.sort_chunk, chunk))
        #             chunk = []

        #         # non_chunk is the pixels that won't be sorted
        #         while index < len(on_process_image_pixels) and ((sort_above_threshold and on_process_image_pixels[index][1] <= threshold) or (not sort_above_threshold and on_process_image_pixels[index][1] >= threshold)):
        #             non_chunk.append(on_process_image_pixels[index])
        #             index += 1

        #         if non_chunk:
        #             sorted_image_pixels.extend(non_chunk)
        #             non_chunk = []

        #     # Append any remaining chunk
        #     if chunk:
        #         futures.append(executor.submit(self.sort_chunk, chunk))

        #     # Wait for all futures to complete and collect results
        #     for future in futures:
        #         sorted_image_pixels.extend(future.result())

        while index < len(on_process_image_pixels):
            # Chunk is the chunk of pixels that will be sorted
            while index < len(on_process_image_pixels) and ((sort_above_threshold and on_process_image_pixels[index][self.main_app.modes_list[mode_index][2]] > threshold) or (not sort_above_threshold and on_process_image_pixels[index][self.main_app.modes_list[mode_index][2]] < threshold)):
                chunk.append(on_process_image_pixels[index])
                index += 1

            if chunk:
                # Sort the chunk using a separate thread
                chunk = self.sort_chunk(chunk)
                for pixel in range(len(chunk)):
                    sorted_image_pixels.append(chunk[pixel])
                chunk = []

            # non_chunk is the pixels that won't be sorted
            while index < len(on_process_image_pixels) and ((sort_above_threshold and on_process_image_pixels[index][self.main_app.modes_list[mode_index][2]] <= threshold) or (not sort_above_threshold and on_process_image_pixels[index][self.main_app.modes_list[mode_index][2]] >= threshold)):
                non_chunk.append(on_process_image_pixels[index])
                index += 1

            if non_chunk:
                for pixel in range(len(non_chunk)):
                    sorted_image_pixels.append(non_chunk[pixel])
                non_chunk = []

        # Append any remaining chunk
        if chunk:
            chunk = self.sort_chunk(chunk)
            for pixel in range(len(chunk)):
                sorted_image_pixels.append(chunk[pixel])
            chunk = []

        # Create a new image with the same mode and size
        sorted_image = Image.new(self.main_app.modes_list[mode_index][1], on_process_image.size)
        
        # Put the sorted pixel data into the new image
        sorted_image.putdata(sorted_image_pixels)
        
        # Convert the image back to its original mode
        final_image = sorted_image.convert(self.image_mode)

        # Convert back to original format
        final_image.format = self.image_format
        
        return final_image

    def sort_chunk(self, chunk):
        return sorted(chunk, key=lambda x: x[1])
