# email feature adapted from:
# https://realpython.com/python-send-email/

import smtplib
import ssl

def send_email(receive, message):
    sender_email = "COMP0066eHealth@gmail.com"
    receiver_email = receive
    send_message = message

    port = 465  # For SSL
    #password = input("Type your password and press enter: ")

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("COMP0066eHealth@gmail.com", "eHealthtest")
        server.sendmail(sender_email, receiver_email, send_message)
        
if __name__ == '__main__':
    receive = "COMP0066eHealth@gmail.com"
    message = """
    Re: eHealth

    This message is sent from Python."""
            
    send_email(receive, message)
    