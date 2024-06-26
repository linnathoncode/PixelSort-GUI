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
        # Image handler instance
        self.image_handler = ImageHandler()

        # Image frame
        self.image_frame = CTkFrame(self.root, width=self.MAINFRAMEX, height=self.MAINFRAMEY)
        self.image_frame.pack(pady=20, padx=20)   

        self.image_label = CTkLabel(master=self.image_frame, text="")
        self.image_label.pack(pady=10)
        self.image_label.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.create_buttons()
        self.root.mainloop()

    def create_buttons(self):
        import_button = CTkButton(self.root,image=self.import_icon, width=200, height=40, text="Import Image", command=self.import_btnf)
        import_button.pack(pady=10)

        export_button = CTkButton(self.root, image=self.export_icon, width=200, height=40, text="Export Image", command=self.export_image_btnf)
        export_button.pack(pady=0)

        pixelsort_image_button = CTkButton(self.root, image=self.pixelsort_icon, width=200, height=40, text="Pixelsort Image", command=self.pixelsort_image_btnf)
        pixelsort_image_button.pack(pady=10)

    def export_image_btnf(self):
        if not self.image_handler.export_image():
            messagebox.showerror("error", "No image is imported!")

    def pixelsort_image_btnf(self):
        ProcessWindow(self.root, self.image_handler, self)

    def import_btnf(self):
        img = self.image_handler.import_image()
        if img is not None:
            self.image_handler.display_image(img, self.MAINFRAMEX, self.MAINFRAMEY, self.image_label)

if __name__ == "__main__":
    main_app = PixelSortApp()
