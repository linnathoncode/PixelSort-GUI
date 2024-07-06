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
        for mode in self.main_app.modes_list:
            self.main_app.modes_list[mode[2]][3] = 0 
        return img

    def export_image(self):
        if self.processed_image is None:
            return False
        try:
            file_path = filedialog.asksaveasfilename(initialdir="C:\Desktop", filetypes=[("Image files", "*.jpeg *.jpg *.png")], initialfile=f"untitled.{(self.processed_image.format).lower()}")
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

    def process_image(self, mode_threshold, sort_position, sort_above_threshold=True ):
        if self.original_image is not None:
            self.mode_index = self.main_app.mode_index
            self.image_mode = self.original_image.mode
            self.image_format = self.original_image.format

            # Convert the image to given mode
            on_process_image = self.original_image.convert(self.main_app.modes_list[self.mode_index][1])
            opi_pixels = list(on_process_image.getdata())
            width, height = on_process_image.size

            # Sorted array initialization
            sorted_image_pixels = [None] * len(opi_pixels)

            if sort_position == "Horizontal":
                opi_pixels_2d = [opi_pixels[i * width:(i + 1) * width] for i in range(height)]
                for row in range(height):
                    self.pixel_sort(opi_pixels_2d[row], row * width, sorted_image_pixels, mode_threshold, sort_above_threshold, self.mode_index, width, sort_position)
            elif sort_position == "Vertical":
                opi_pixels_2d = [[opi_pixels[row * width + col] for row in range(height)] for col in range(width)]
                for col in range(width):
                    self.pixel_sort(opi_pixels_2d[col], col, sorted_image_pixels, mode_threshold, sort_above_threshold, self.mode_index, width, sort_position)
            else:
                raise ValueError(f"Unknown sort position: {sort_position}")

            # Create a new image with the same mode and size
            sorted_image = Image.new(self.main_app.modes_list[self.mode_index][1], on_process_image.size)
            
            # Put the sorted pixel data into the new image
            sorted_image.putdata(sorted_image_pixels)
            
            # Convert the image back to its original mode
            final_image = sorted_image.convert(self.image_mode)

            # Convert back to original format
            final_image.format = self.image_format
            
            return final_image
                

    def save_changes(self, on_process):
        self.processed_image = on_process

    def display_image(self, img, frame_x, frame_y, image_label):
        # Creates a duplicate image with the adjusted size and displays it 
        resized_img = self.get_adjusted_image_size(img, frame_x, frame_y)
        self.displayed_image = CTkImage(light_image=resized_img, dark_image=resized_img, size=(resized_img.width, resized_img.height))
        image_label.configure(image=self.displayed_image)
    
    def pixel_sort(self, line_pixels, start_index, sorted_image_pixels, threshold, sort_above_threshold, mode_index, width, sort_position):
            chunk = []
            non_chunk = []
            chunk_indices = []
            non_chunk_indices = []

            stride = 1 if sort_position == "Horizontal" else width

            for i, pixel in enumerate(line_pixels):
                index = start_index + (i * stride)

                if (sort_above_threshold and pixel[self.main_app.modes_list[mode_index][2]] > threshold) or (not sort_above_threshold and pixel[self.main_app.modes_list[mode_index][2]] < threshold):
                    chunk.append(pixel)
                    chunk_indices.append(index)
                else:
                    if chunk:
                        sorted_chunk = self.sort_chunk(chunk)
                        for idx, sorted_pixel in zip(chunk_indices, sorted_chunk):
                            sorted_image_pixels[idx] = sorted_pixel
                        chunk = []
                        chunk_indices = []
                    non_chunk.append(pixel)
                    non_chunk_indices.append(index)

            # Handle remaining chunks
            if chunk:
                sorted_chunk = self.sort_chunk(chunk)
                for idx, sorted_pixel in zip(chunk_indices, sorted_chunk):
                    sorted_image_pixels[idx] = sorted_pixel
            if non_chunk:
                for idx, pixel in zip(non_chunk_indices, non_chunk):
                    sorted_image_pixels[idx] = pixel


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


    def sort_chunk(self, chunk):
        return sorted(chunk, key=lambda x: x[1])