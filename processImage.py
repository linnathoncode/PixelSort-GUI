from PIL import Image
import tkinter as tk
def processImage(image):
    og_format = image.format

    # convert the image to HSV mode
    pre_image = image.convert('HSV')
    
    # get the pixel data
    pre_image_pixels = list(pre_image.getdata())
    
    # sort the pixels by the second value (Saturation) in ascending/descending orden
    # reverse -> false ascending, true descending
    sorted_image_pixels = sorted(pre_image_pixels, key=lambda x: x[1], reverse=False)
    
    # create a new image with the same mode and size
    sorted_image = Image.new('HSV', pre_image.size)
    
    # ut the sorted pixel data into the new image
    sorted_image.putdata(sorted_image_pixels)
    
    # convert the image back to RGBA mode
    final_image = sorted_image.convert('RGB')
    final_image.format = og_format
    return final_image
    

        
image = Image.open('goated.jpeg')
processImage(image)

