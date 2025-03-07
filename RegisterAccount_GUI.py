import customtkinter as ctk
from Registration import register_user
from Logger import logging
from PIL import Image, ImageTk
from File_path import resource_path 
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")
class RegistrationFrame(ctk.CTkFrame):
    def __init__(self, master, open_login_account):
        super().__init__(master, fg_color="transparent") 

        # Load and set the background image
        image_path = resource_path("Assets/background1.png")
        self.background_image = Image.open(image_path)
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        self.canvas = ctk.CTkCanvas(self, width=1400, height=800, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.background_photo, anchor="nw")

        self.switch_to_login = open_login_account

        # Title Label
        self.title_label = ctk.CTkLabel(self, text="Register new account", font=("Arial", 20), fg_color="transparent")
        self.title_label.place(relx=0.5, rely=0.1, anchor="center")  

        # Name Field
        self.name_label = ctk.CTkLabel(self, text="Name", fg_color="transparent")
        self.name_label.place(relx=0.5, rely=0.2, anchor="center") 
        self.name_entry = ctk.CTkEntry(self, width=300, fg_color="transparent")
        self.name_entry.place(relx=0.5, rely=0.25, anchor="center") 

        # Email Field
        self.email_label = ctk.CTkLabel(self, text="Email", fg_color="transparent")
        self.email_label.place(relx=0.5, rely=0.35, anchor="center") 
        self.email_entry = ctk.CTkEntry(self, width=300, fg_color="transparent")
        self.email_entry.place(relx=0.5, rely=0.4, anchor="center") 

        # Password Field
        self.password_label = ctk.CTkLabel(self, text="Password", fg_color="transparent")
        self.password_label.place(relx=0.5, rely=0.5, anchor="center") 
        self.password_entry = ctk.CTkEntry(self, width=300, show="*", fg_color="transparent")
        self.password_entry.place(relx=0.5, rely=0.55, anchor="center")  

        # Register Button
        self.register_button = ctk.CTkButton(self, text="Register", command=self.Register_new_user, fg_color="transparent")
        self.register_button.place(relx=0.5, rely=0.65, anchor="center") 

        # Go Back Button
        self.goback_button = ctk.CTkButton(self, text="Go back", command=self.go_back, fg_color="transparent")
        self.goback_button.place(relx=0.5, rely=0.75, anchor="center")  

        # Status Label
        self.status_label = ctk.CTkLabel(self, text="", fg_color="transparent")
        self.status_label.place(relx=0.5, rely=0.85, anchor="center")  

        self.lift()  

        
    def Register_new_user(self):
        Email = self.email_entry.get()
        Password = self.password_entry.get()
        Name = self.name_entry.get()
        status_message = register_user(Email, Password, Name)
        self.status_label.configure(text=status_message)

        if "success" in status_message.lower():
            self.switch_to_login()

    def go_back(self):
        logging.info("Going back to main window")
        self.pack_forget()
        self.master.show_mainwindow()
