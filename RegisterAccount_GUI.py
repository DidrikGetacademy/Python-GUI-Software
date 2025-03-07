import customtkinter as ctk
from Registration import register_user
from Logger import logging
from PIL import Image, ImageTk
from File_path import resource_path 
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

        # Dark gray container for registration elements
        self.container = ctk.CTkFrame(
            self, 
            fg_color="#2C3E50",
            corner_radius=15,
            width=400,
            height=500
            )  
        self.container.place(relx=0.5, rely=0.5, anchor="center")

        # Title Label
        self.title_label = ctk.CTkLabel(
            self.container,
            text="Register New Account",
            font=("Arial", 24, "bold"),
            text_color="#FFFFFF"
            ) 
        self.title_label.pack(pady=20)

        # Name Field
        self.name_label = ctk.CTkLabel(self.container, text="Name", text_color="#FFFFFF")  

        self.name_label.pack(pady=(10, 0))
        self.name_entry = ctk.CTkEntry(
            self.container, 
            width=300, 
            fg_color="#FFFFFF",
            text_color="#2C3E50",
            border_color="#2C3E50",
            placeholder_text="Enter your name",
            justify="center"
            )
        self.name_entry.pack(pady=5)

        # Email Field
        self.email_label = ctk.CTkLabel(self.container, text="Email", text_color="#FFFFFF")  # White text
        self.email_label.pack(pady=(10, 0))
        self.email_entry = ctk.CTkEntry(
            self.container,
            width=300,
            fg_color="#FFFFFF",
            text_color="#2C3E50", 
            border_color="#2C3E50", 
            placeholder_text="Enter your email",
            justify="center"
            )
        
        
        self.email_entry.pack(pady=5)

        # Password Field
        self.password_label = ctk.CTkLabel(self.container, text="Password", text_color="#FFFFFF")  # White text
        self.password_label.pack(pady=(10, 0))
        self.password_entry = ctk.CTkEntry(
            self.container,
              width=300,
              show="*",
              fg_color="#FFFFFF",
              text_color="#2C3E50",
              border_color="#2C3E50",
              placeholder_text="Enter your password",
                justify="center"
              )
        self.password_entry.pack(pady=5)

        # Register Button
        self.register_button = ctk.CTkButton(
            self.container, text="Register",
             command=self.Register_new_user,
             fg_color="#34495E", 
             text_color="#FFFFFF",
             hover_color="#1F2A38"
            )  
        self.register_button.pack(pady=20)

        #Goback Button
        self.goback_button = ctk.CTkButton(
            self.container, 
            text="Go back",
            command=self.go_back,
            fg_color="transparent",
            text_color="#FFFFFF",
            hover_color="#1F2A38"
            ) 
        self.goback_button.pack(pady=5)


        # Status Label
        self.status_label = ctk.CTkLabel(
            self.container, text="", text_color="#E74C3C")  
        self.status_label.pack(pady=10)

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
