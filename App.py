import customtkinter as ctk
from RegisterAccount_GUI import RegistrationFrame
from LoginAccount_GUI import LoginFrame
from PIL import Image, ImageTk 
from File_path import resource_path
class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1920x1080")
        self.title("Account Management")
        self.resizable(False,False)
        self.maxsize(1400,800)
        self.minsize(1400,800)
        
        


        self.canvas = ctk.CTkCanvas(
            self, 
            width=200, 
            height=200, 
            highlightthickness=0
            )
        
        self.canvas.pack(fill="both", expand=True)
        ImageFront = resource_path("Assets/background1.png")
        self.background_image = Image.open(ImageFront)  
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.canvas.create_image(0, 0, image=self.background_photo, anchor="nw")


       


        self.Register_button = ctk.CTkButton(
            self, 
            text="Register Account", 
            command=self.open_Register_Account,
            bg_color="black",
            fg_color="Black",
            text_color="white"
            )
        self.Register_button.place(relx=0.5, rely=0.5, anchor="center")  

    
        self.login_button = ctk.CTkButton(
            self, 
            text="Login", 
            command=self.open_login_Account,
            bg_color="black",fg_color="Black",
            text_color="white"
            )
        
        self.login_button.place(relx=0.5, rely=0.6, anchor="center")  
        
        
        self.register_frame = RegistrationFrame(
            self, 
            self.open_login_Account
            )
        
        
        self.login_frame = LoginFrame(
            self, 
            self.Connect_User_Account
            )
        self.UserAccount_Frame = None



    def Connect_User_Account(self):
        from UserAccount import UserAccountFrame
        if self.UserAccount_Frame is None:
            self.UserAccount_Frame = UserAccountFrame(self)
        self.hide_frames()
        self.UserAccount_Frame.pack(fill="both", expand=True)



    def open_Register_Account(self):
        self.hide_frames()
        self.register_frame.pack(fill="both", expand=True)


    def open_login_Account(self):     
        self.hide_frames()
        self.login_frame.pack(fill="both", expand=True)



    def hide_frames(self):
        self.Register_button.place_forget()
        self.login_button.place_forget()
        self.register_frame.pack_forget()
        self.login_frame.pack_forget()
        self.canvas.pack_forget()




    def show_mainwindow(self):
        self.canvas.pack(fil="both",expand=True)
        self.canvas.create_image(0, 0, image=self.background_photo, anchor="nw")
        self.Register_button.place(relx=0.5, rely=0.5, anchor="center")
        self.login_button.place(relx=0.5, rely=0.6, anchor="center")


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
