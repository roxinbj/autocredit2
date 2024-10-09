import serial
import time

def send_sms(phone_number, message):
    try:
        ser.write(b'AT+CMGF=1\r')  # Set SMS mode to text
        time.sleep(2)
        
        ser.write(b'AT+CMGS="' + phone_number.encode() + b'"\r')
        time.sleep(2)
        
        ser.write(message.encode() + b"\r")
        time.sleep(2)
        
        ser.write(b"\x1A")  # CTRL+Z to send the message
        time.sleep(3)  # Allow time for SMS to send
        print(f"SMS {message} sent to {phone_number}")
        
    except Exception as e:
        print(f"Error sending SMS: {e}")

def read_sms():
    try:
        ser.write(b'AT+CMGF=1\r')  # Set SMS mode to text
        time.sleep(2)
        
        ser.write(b'AT+CMGL="ALL"\r')  # Read all messages
        time.sleep(3)
        
        response = ser.read(ser.inWaiting()).decode('utf-8', errors='ignore')
        print("SMS Response: " + response)
        return response
    
    except Exception as e:
        print(f"Error reading SMS: {e}")
        return ""

def delete_all_sms():
    try:
        ser.write(b'AT+CMGDA="DEL ALL"\r')  # Delete all SMS
        time.sleep(2)
        print("All SMS Deleted")
        
    except Exception as e:
        print(f"Error deleting SMS: {e}")


def check_if_x_exists_in_sms(x):
    response = read_sms()
    if x in response:
        return True
    else:
        return False

def confirmation_successfull():
    confirmation_counter = 0
    while confirmation_counter < 4:
        print(f"Confirmation Counter: {confirmation_counter}")
        # If we received a message success - done
        if check_if_x_exists_in_sms("You have successfully transferred"):
            print(f"Confirmation SMS found")
            return True
        # If we received a message with pending, somethug went wrong
        elif check_if_x_exists_in_sms("no pending"):
            return False;
        # If we received neither or, wait for another 5 seconds and check again
        else:
            confirmation_counter += 1
            time.sleep(5)
        
    return False

def wait_for_confirmation(confirmation_text, timeout_sec=300):
    start_time = time.time()
    while time.time() - start_time < timeout_sec:
        response = read_sms()
        print("response sms " + response)
        
        if confirmation_text in response:
            return True
        else: 
            return False
        
        time.sleep(5)  # Wait for 5 seconds before checking again
    
    return False  # Timeout reached without finding confirmation

def upload_credit_to(phone_number, try_x_times):
    counter = 0
    while counter < try_x_times:
        print("-------------------counter " + str(counter) + "--------------")
        # Delete all SMS messages before starting
        delete_all_sms()

        # Step 1: Send the "2MB#" followed by the phone number to 13800
        message = "2MB#" + str(phone_number)
        send_sms("13800", message)
        time.sleep(5)
    
        # Step 2: Send "Yes" to confirm if the first confirmation message is received
        send_sms("13800", "Yes")
        time.sleep(5)
    
        # Step 3: Wait for the final confirmation SMS
        if confirmation_successfull():
            return True
        else:
            counter += 1
           
    return False
        


# Initialize the serial connection to SIM900
try:
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=5)
    time.sleep(2)  # Allow time for the serial connection to initialize
    
    if upload_credit_to("0813488652",5):
        print("Successfully uploaded credit to 0813488652")
    else: 
        print("SMS to Bjorn")
    
except Exception as e:
    print(f"Error: {e}")

finally:
    if ser.is_open:
        ser.close()  # Ensure the serial connection is properly closed
