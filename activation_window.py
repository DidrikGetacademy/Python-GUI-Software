from customtkinter import (
    CTkToplevel,
    CTkButton,
    CTkEntry,
    CTkLabel,
)
from tkinter import StringVar, messagebox
from Logger import logging
from Decryption import load_key



class ActivationWindow(CTkToplevel):
    def __init__(self, parent, on_activation_success):
        super().__init__(parent)
        self.title("Activation Key")
        self.geometry("600x600")
        self.on_activation_success = on_activation_success
        logging.info("Activation window opened.")
        self.activation_key_var = StringVar()

    
        from Validate_key import validate_key
        stored_key = load_key()
        if stored_key:
            if validate_key(stored_key):  
                messagebox.showinfo("Success","Activation successful!")
                self.destroy() 
                if self.on_activation_success:
                    self.on_activation_success() 
                    return
                else:
                    messagebox.showerror("Error", "Invalid or expired activation key.")
                    logging.warning("Invalid or expired activation key.")
                    self.destroy()
            

        self.create_activation_ui()
        
        self.entry.focus_set()
        
        
    def create_activation_ui(self):
                
         self.instructions_label = CTkLabel(
         self, text="Please enter your activation key below: "
          )
         self.instructions_label.pack(pady=20)     
         
                
        #Activation key entry
         self.entry = CTkEntry(self,textvariable=self.activation_key_var,width=400)
         self.entry.pack(pady=10)
         self.entry.insert(0, "Enter Activation Key") 
         self.entry.focus_set()
         
         #Activate Button
         self.activate_button = CTkButton(
         self,text="Activate",command=self.activate_key
         )
         self.activate_button.pack(pady=10)




    def activate_key(self):
        key = self.activation_key_var.get()
        if key:
            from Validate_key import validate_key
            if validate_key(key):  
                messagebox.showinfo("Success", "Activation Key is valid!")
                self.destroy()
                if self.on_activation_success:
                    self.on_activation_success()  
            else:
                messagebox.showerror("Error", "Invalid or used activation key.")
                logging.warning("Error", "Invalid or used activation key.")
        else:
            messagebox.showwarning("Warning", "Please type in your Activation Key")
            logging.warning("Warning", "Please type in your Activation Key")