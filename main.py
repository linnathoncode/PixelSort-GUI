from customtkinter import *
from tkinter import messagebox
from imageHandler import ImageHandler
from processWindow import ProcessWindow
from PIL import Image

class PixelSortApp:
    def __init__(self):
        # Theme
        set_appearance_mode("light")
        set_default_color_theme("red.json")

        self.MAINFRAMEX = 900 
        self.MAINFRAMEY = 450

        # Setup
        self.root = CTk()
        self.root.geometry("1280x720")
        self.root.title("PIXELSORT")
        self.root.iconbitmap("icons/pixelsortlogo.ico")

        self.export_icon = CTkImage(Image.open("icons/export.png"))
        self.import_icon = CTkImage(Image.open("icons/import.png"))
        self.pixelsort_icon = CTkImage(Image.open("icons/process.png"))
        self.new_change = False
        
        # name, mode, position, threshold
        self.mode_index = 0
        self.modes_list = [
            ["Hue", "HSV", 0, 0],
            ["Saturation", "HSV", 1, 0],
            ["Value", "HSV", 2, 0]
        ]

        self.positions_list = [
            "Horizontal",
            "Vertical"
            ]
        
        self.sort_position = self.positions_list[0]

        # Image handler instance
        self.image_handler = ImageHandler(self)
        # whether or not there is a new change made


        # Image frame
        self.image_frame = CTkFrame(self.root, width=self.MAINFRAMEX, height=self.MAINFRAMEY)
        self.image_frame.pack(pady=20, padx=20)   

        self.image_label = CTkLabel(master=self.image_frame, text="")
        self.image_label.pack(pady=10)
        self.image_label.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.create_buttons()
        self.create_preferences()
        self.root.mainloop()

    def create_buttons(self):   
        self.button_frame = CTkFrame(self.root, width=900, height=50)
        import_button = CTkButton(self.button_frame,image=self.import_icon, width=200, height=40, text="Import Image", command=self.import_btnf)
        import_button.grid(row= 0, column =0, pady=10, padx= 10)

        export_button = CTkButton(self.button_frame, image=self.export_icon, width=200, height=40, text="Export Image", command=self.export_image_btnf)
        export_button.grid(row= 0, column =1, pady=0, padx= 10)

        pixelsort_image_button = CTkButton(self.button_frame, image=self.pixelsort_icon, width=200, height=40, text="Pixelsort Image", command=self.pixelsort_image_btnf)
        pixelsort_image_button.grid(row= 0, column =2,pady=10, padx= 10)
        self.button_frame.pack(anchor=CENTER)

    def create_preferences(self):
        self.preferences_frame = CTkFrame(self.root, width=900, height=50)
        
        self.modes_option_label = CTkLabel(self.preferences_frame, text="Sort by: ", font=("Arial", 16))
        self.modes_option_label.grid(row=0, column=0, padx=5)

        modes = [mode[0] for mode in self.modes_list]
        self.modes_option = CTkOptionMenu(self.preferences_frame, values=modes, command=self.mode_changed)
        self.modes_option.grid(row=0, column=1, padx=10)

        self.positions_option_label = CTkLabel(self.preferences_frame, text="Position:", font=("Arial", 16))
        self.positions_option_label.grid(row=0, column=2, padx=5)

        self.positions_option = CTkOptionMenu(self.preferences_frame, values=self.positions_list, command=self.position_changed)
        self.positions_option.grid(row=0, column=3, padx= 10)
        self.preferences_frame.pack(pady=10)

    def position_changed(self, value):
        self.sort_position = value

    def mode_changed(self, value):
        index = 0
        for mode in self.modes_list:
            if mode[0] == value:
                self.mode_index = index
                break
            index += 1

    def export_image_btnf(self):
        if not self.image_handler.export_image():
            messagebox.showerror("error", "No image is imported!")

    def pixelsort_image_btnf(self):
        self.new_change = False
        ProcessWindow(self.root, self.image_handler, self)

    def import_btnf(self):
        new_image_handler_instance = ImageHandler(self)
        img = new_image_handler_instance.import_image()
        if img is not None:
            self.image_handler = new_image_handler_instance
            self.image_handler.display_image(img, self.MAINFRAMEX, self.MAINFRAMEY, self.image_label)

if __name__ == "__main__":
    main_app = PixelSortApp()
