import logging
import requests
from Logger import logging
from Decryption import load_key
from encryption import save_key,encrypt_key
from User_data_storage import get_user_data



def validate_key_with_Server(key_code):
    try:
        user_data = get_user_data()
        user_id = user_data.get("id",None)
        
        if not user_id:
            logging.error("User ID not found. cannot validate key.")
            return False
        
        headers = {"Content-Type": "application/json"}
        response = requests.post(
            "https://learnreflects.com/Server/Validate_privatekey.php",
            json={"key_code": key_code, "user_id": user_id},
            headers=headers
        )
        response.raise_for_status()
        data = response.json()
        if data.get("success"):
            subscription_type = data.get("subscription_type","unknown")
            subscription_end = data.get("subscription_end",None)
            
            logging.info(f"Program activated successfully! Subscription type: {subscription_type}")
            if subscription_end:
                logging.info(f"subscription ends at: {subscription_end}")
            encrypted_key = encrypt_key(key_code)
            save_key(encrypted_key)
            logging.info("Program activated successfully!")
            return True
        else:
            logging.error(f"Activation failed: {data.get('error', 'Unknown error')}")
            return False
    except requests.exceptions.RequestException as e:
        logging.error(f"Error during key validation: {e}")
        return False


# def validate_subscription_status(user_id):
#     try:
#         user_data = get_user_data()
#         print(f"userdata:",user_data)
        
#         headers = {
#             "Content-Type": "application/json",
#             "Authorization": f"Bearer {user_data.get('token', '')}"
#         }
        
#         response = requests.post(
#             "https://learnreflects.com/Server/validate_subscription.php",
#             json={"user_id": user_id},
#             headers=headers
#         )
#         response.raise_for_status()
#         data = response.json()
        
#         #Checks if subscription is active
#         if not data.get('active', False):
#             print(f"Subscription is not active.")
#             return False
        

#         #Checks if expiration is out on subscription.
#         expiration_date = data.get('subscription_end', "")
#         if expiration_date:
#             from datetime import datetime
#             exp_date = datetime.strptime(expiration_date, "%Y-%m-%d")
#             if exp_date < datetime.now():
#                 logging.error("Subscription expired!")
#                 print(f"Error subscription expired.")
         
#                 return False

#         return True

#     except requests.exceptions.RequestException as e:
#         logging.error(f"Subscription validation error: {str(e)}")
#         return False



def validate_key_locally(key_code):
    decrypted_key = load_key()
    if decrypted_key and decrypted_key == key_code:
        logging.info("Local validation successful.")
        return True
    else:
        logging.warning("Local validation failed.")
        return False





def validate_key(key_code):
    stored_key = load_key()
    if stored_key:
        if validate_key_locally(stored_key):
            return True
        
    return validate_key_with_Server(key_code)


