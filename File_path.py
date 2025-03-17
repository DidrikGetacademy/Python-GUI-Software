import json
import logging
import sys
from Logger import logging
from cryptography.fernet import Fernet
from pathlib import Path
import os


def load_userdata():
     if User_data_Path.exists():
         try: 
             with open(User_data_Path,'r') as file:
                 return json.load(file) 
         except (json.JSONDecodeError, IOError) as e:
             logging.error(f"Error loading user data: {e}")
             return {}
         else:
             logging.warning("Userdata file does not exsist.")
             return {}





def get_userdata_from_appdata():
    try:
         if User_data_Path.exists():
             with open(User_data_Path, 'r',encoding='utf-8') as user_file:
                 userdata = json.load(user_file)
                 logging.info(f"Loaded user data:  {userdata}")
                 return userdata
         else: 
            logging.warning(f"Userdata does not exsist on the path {User_data_Path}")
            return None
    except Exception as e:
        logging.error(f"could not read userdata.txt")
        return None
    
    


def ensure_userdata():
        from User_data_storage import get_user_data
        UserData = get_user_data()
        if UserData:
            with open(User_data_Path,"w", encoding="utf-8") as user: 
                  json.dump(UserData,user,indent=4)
                  logging.info("User data successfully written to file.")
        logging.info("no user data too write")




def ensure_directories():
    if not app_data_path.exists():
        logging.info("App_data_path did not exist, creating it now")
        app_data_path.mkdir(parents=True, exist_ok=True)  
        
    if not secret_key_path.exists():
        logging.info("Secret_key_path did not exist, Creating a key with Fernet")
        key = Fernet.generate_key()
        with open(secret_key_path, "wb") as key_file:
            key_file.write(key)
        logging.info(f"Generated new encryption key {key} and saved to secret.key at {secret_key_path}")
    
    if not secret_key_path.exists() or secret_key_path.stat().st_size == 0:
        logging.error("Failed to generate or save the encryption key.")
        raise ValueError("Encryption key could not be s aved or laded correctly")   
    
    if not activation_key_path.exists():
        with open(activation_key_path, "w") as key_file:
            json.dump({},key_file) 
        logging.info("Generated empty activation_key.json")
    
    try: 
         from Validate_key import load_key
         if not load_key():
           logging.info("No valid activation key found")
           return None
    except ImportError as e:
        logging.error(f"Error importing load_key: {e}")
        raise



def get_app_data_path():
    if sys.platform == "win32":
        return Path(os.getenv("APPDATA")) / "LearnReflect"
    elif sys.platform == "darwin":  # macOS
        return Path.home() / "Library" / "Application Support" / "LearnReflect"
    else:  # Linux and others
        return Path.home() / ".config" / "LearnReflect" #linux


def resource_path(relative_path):
    if getattr(sys, 'frozen',False):
        base_path = sys._MEIPASS
    else: 
        base_path = os.path.abspath(os.path.dirname(__file__))
    logging.info(f"Base Path for bundled files {base_path}")
    logging.info(f"Bundled files and folders: {os.listdir(base_path)}")
    full_path = os.path.join(base_path,relative_path)
    return full_path

app_data_path = get_app_data_path()
secret_key_path = app_data_path / 'secret.key'
activation_key_path = app_data_path / 'activation_key.json'
User_data_Path = app_data_path / 'Userdata.txt'