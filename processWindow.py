from customtkinter import *
from tkinter import messagebox
from sys import platform
from PIL import Image
NEWWINFRAMEX = 900
NEWWINFRAMEY = 645

class ProcessWindow:
    def __init__(self, root, image_handler, main_app):
        self.root = root
        self.main_app = main_app
        self.image_handler = image_handler
        self.temp_mode_threshold =self.main_app.modes_list[self.main_app.mode_index][3]

        if self.image_handler.original_image is not None:
            self.on_process_img = self.image_handler.processed_image
            self.new_window = CTkToplevel(self.root)
            self.new_window.title(f"Pixel Sort by {self.main_app.modes_list[self.main_app.mode_index][0]}")
            self.new_window.geometry("1280x720")
            self.new_window.attributes("-topmost", True)
            self.new_window.iconbitmap("icons/pixelsortlogo.ico")
            self.save_icon = CTkImage(Image.open("icons/save.png"))
            self.process_icon = CTkImage(Image.open("icons/process.png"))

            # Because CTkToplevel currently is bugged on windows
            # and doesn't check if a user specified icon is set
            # we need to set the icon again after 200ms
            if platform.startswith("win"):
              self.new_window.after(200, lambda: self.new_window.iconbitmap("icons/pixelsortlogo.ico"))

            # Frame & label setup
            self.process_frame = CTkFrame(self.new_window, width=NEWWINFRAMEX, height=NEWWINFRAMEY)
            self.process_frame.grid(row=0, column=0, pady=20, padx=20, sticky='w')
            self.process_label = CTkLabel(master=self.process_frame, text="")
            self.process_label.grid(row=0, column=0)
            self.process_label.place(relx=0.5, rely=0.5, anchor=CENTER)
            self.process_win_display(self.on_process_img)

            # Button & sliders frame
            self.preferences_frame = CTkFrame(self.new_window, width=300, height=720)

            self.mode_threshold_label = CTkLabel(master=self.preferences_frame, text=self.temp_mode_threshold)
            self.mode_threshold_label.pack(pady=5)

            self.create_buttons_sliders()
            


            self.preferences_frame.grid(pady=20, padx=20, row=0, column=1, sticky="n")
            
            #self.pre_process()
        else:
            messagebox.showerror("error", "No image is imported!")

    def pre_process(self):
        self.on_process_img = self.image_handler.process_image(self.temp_mode_threshold)
        self.process_win_display(self.on_process_img)
        return

    def create_buttons_sliders(self):

        self.slider = CTkSlider(self.preferences_frame, from_=0, to=255,command=self.sliderf)
        self.slider.set(self.temp_mode_threshold)
        self.slider.pack(pady=5, padx=20)

        # Process button
        self.process_image_button = CTkButton(master=self.preferences_frame, image=self.process_icon, width=200, height=40, text="Process Image",
                                                command=lambda: self.process_image_btnf())
        self.process_image_button.pack(pady=10, padx=20)

        # Save changes button
        self.save_changes_button = CTkButton(master=self.preferences_frame, image=self.save_icon, width=200, height=40, text="Save Changes",
                                                command=self.save_changes_btnf)
        self.save_changes_button.pack(pady=10, padx=20)


    def sliderf(self,value):
        self.temp_mode_threshold = int(value)
        self.mode_threshold_label.configure(text=int(value))

    def process_image_btnf(self):
        # Passes processImage function as a parameter
        self.main_app.new_change = True
        self.on_process_img = self.image_handler.process_image(self.temp_mode_threshold, self.main_app.sort_position)
        self.process_win_display(self.on_process_img)

    def process_win_display(self, img):
        # Creates a replica image with the adjusted size for the frame and displays it
        img = self.image_handler.get_adjusted_image_size(img, NEWWINFRAMEX, NEWWINFRAMEY)  # Returns Image
        processed_image = CTkImage(light_image=img, dark_image=img, size=(img.width, img.height))
        self.process_label.configure(image=processed_image)

    def save_changes_btnf(self):
        # Saves the changes made in the pixelsort windows and displays the changed image on the main frame
        if self.main_app.new_change:
            self.main_app.modes_list[self.main_app.mode_index][3] =  self.temp_mode_threshold
            self.image_handler.save_changes(self.on_process_img)
            self.image_handler.display_image(self.image_handler.processed_image, self.main_app.MAINFRAMEX, self.main_app.MAINFRAMEY, self.main_app.image_label)