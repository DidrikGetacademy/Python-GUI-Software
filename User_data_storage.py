import requests
from Logger import logging
import time
#Global userdata
_user_data = {}


    

def set_user_data(data,password = None,RememberMe = False):
    global _user_data
    if not isinstance(data,dict):
        logging.error("Invalid data type. Expected a dictionary.")
        return
    _user_data = data
    if password and RememberMe == True:
        _user_data["password"] = password
        _user_data["last_login"] = time.time() 
    from File_path import ensure_userdata
    ensure_userdata()
    logging.info("User data has been set, and dumped in file.")




def get_user_data():
    return _user_data


#C:\Users\didri\AppData\Roaming\LearnReflect\Userdata.txt


url = "https://learnreflects.com/Server/UpdateUser.php"
def Update_user_data():
    userid = _user_data.get('id')
    email = _user_data.get('email')
    
    if not userid or not email:
         logging.error("Userid and email are required to update user_data")
         return "User ID and  Email are required"
     
     
    payload = {"id": userid ,"email": email}
    
    try:
        headers = {"Content-Type": "application/json"}
        response = requests.post(
            url,
            json=payload,
            headers=headers
        )
        response.raise_for_status()
        
        try:
            data = response.json()
        except ValueError:
            logging.error(f"unexpected response format: {response.text}")
            return "invalid respone from sever",None
        
        if data.get("success",False):
            user = data.get("user",{})
            logging.info(user)
            _user_data['id'] = user.get('id',_user_data.get('id',"Unknown"))
            _user_data['name'] = user.get('name', _user_data.get('name',"Unkown"))
            _user_data['email'] = user.get('email', _user_data.get('email',"Unkown"))
            _user_data['subscription_type'] = user.get('subscription_type', _user_data.get('subscription_type',"Unkown"))
            
            logging.info("User data successfully updated")
            return _user_data
        else:
            error_message = data.get("message","Failed to update user data.")
            logging.error(f"Server error:  {error_message}")
            return error_message,None
    except requests.exceptions.RequestException as e:
        logging.error(f"Request error: {str(e)}")
        return f"Request error: {str(e)}",None       
     
     


def request_password_reset(email):
    url = "https://learnreflects.com/Server/ResetPassword.php"
    payload = {"email": email}
    headers= {"Content-Type": "application/json"}
    try: 
        response = requests.post(url,json=payload,headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}
    
    
         
     
def Reset_password(Token,New_Password):
    url = "https://learnreflects.com/Server/ResetPasswordToken.php"
    payload = {"token": Token, "password": New_Password}
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(
            url,
            json=payload,
            headers=headers
        )
        response.raise_for_status()
        logging.info(f"Response: {response.text}")
        return response.json()
    
    except requests.exceptions.RequestException as e:
        logging.error(f"Request error: {str(e)}")
        return f"Request error: {str(e)}"
            


