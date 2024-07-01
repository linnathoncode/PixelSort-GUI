from customtkinter import *
from tkinter import messagebox

NEWWINFRAMEX = 900
NEWWINFRAMEY = 645

class ProcessWindow:
    def __init__(self, root, image_handler, main_app):
        self.root = root
        self.image_handler = image_handler
        self.main_app = main_app
        self.saturation_threshold = 0

        if self.image_handler.original_image is not None:
            self.on_process_img = self.image_handler.processed_image
            self.new_window = CTkToplevel(self.root)
            self.new_window.title("Process")
            self.new_window.geometry("1280x720")
            self.new_window.attributes("-topmost", True)

            # Frame & label setup
            self.process_frame = CTkFrame(self.new_window, width=NEWWINFRAMEX, height=NEWWINFRAMEY)
            self.process_frame.grid(row=0, column=0, pady=20, padx=20, sticky='w')

            self.process_label = CTkLabel(master=self.process_frame, text="")
            self.process_label.grid(row=0, column=0)
            self.process_label.place(relx=0.5, rely=0.5, anchor=CENTER)
            self.process_win_display(self.on_process_img)

            # Button & sliders frame
            self.preferences_frame = CTkFrame(self.new_window, width=300, height=720)

            self.create_buttons_sliders()
            
            self.saturation_threshold_label = CTkLabel(master=self.preferences_frame, text="0")
            self.saturation_threshold_label.pack()

            self.preferences_frame.grid(pady=20, padx=20, row=0, column=1, sticky="n")
            

        else:
            messagebox.showerror("error", "No image is imported!")


    def create_buttons_sliders(self):
            # Process button
            self.process_image_button = CTkButton(master=self.preferences_frame, width=200, height=40, text="Process Image",
                                                  command=lambda: self.process_image_btnf())
            self.process_image_button.pack(pady=10, padx=20)

            # Save changes button
            self.save_changes_button = CTkButton(master=self.preferences_frame, width=200, height=40, text="Save Changes",
                                                 command=self.save_changes_btnf)
            self.save_changes_button.pack(pady=10)

            self.slider = CTkSlider(self.preferences_frame, from_=0, to=255,command=self.sliderf)
            self.slider.set(0)
            self.slider.pack(pady=10, padx=20)

    def sliderf(self,value):
        self.saturation_threshold = value
        self.saturation_threshold_label.configure(text=int(value))

    def process_image_btnf(self):
        # Passes processImage function as a parameter
        self.on_process_img = self.image_handler.process_image(self.saturation_threshold)
        self.process_win_display(self.on_process_img)

    def process_win_display(self, img):
        # Creates a replica image with the adjusted size for the frame and displays it
        img = self.image_handler.get_image_size(img, NEWWINFRAMEX, NEWWINFRAMEY)  # Returns Image
        processed_image = CTkImage(light_image=img, dark_image=img, size=(img.width, img.height))
        self.process_label.configure(image=processed_image)

    def save_changes_btnf(self):
        # Saves the changes made in the pixelsort windows and displays the changed image on the main frame
        self.image_handler.save_changes(self.on_process_img)
        self.image_handler.display_image(self.image_handler.processed_image, self.main_app.MAINFRAMEX, self.main_app.MAINFRAMEY, self.main_app.image_label)