import customtkinter as ctk
from RegisterAccount_GUI import RegistrationFrame
from LoginAccount_GUI import LoginFrame


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x800")
        self.title("Account Management")
        self.title_label = ctk.CTkLabel(
            self, text="Account Management", font=("Arial", 24)
        )
        self.title_label.pack(pady=20)

        self.Register_button = ctk.CTkButton(
            self, text="Register Account", command=self.open_Register_Account
        )
        self.Register_button.pack(pady=20)

        self.login_button = ctk.CTkButton(
            self, text="Login", command=self.open_login_Account
        )
        self.login_button.pack(pady=20)

        self.register_frame = RegistrationFrame(self, self.open_login_Account)
        self.login_frame = LoginFrame(self, self.Connect_User_Account)
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
        self.title_label.pack_forget()
        self.Register_button.pack_forget()
        self.login_button.pack_forget()
        self.register_frame.pack_forget()
        self.login_frame.pack_forget()

    def show_mainwindow(self):
        self.title_label.pack(pady=20)
        self.Register_button.pack(pady=20)
        self.login_button.pack(pady=20)
    
   
        

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
