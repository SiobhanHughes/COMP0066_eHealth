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
        server.login("COMP0066eHealth@gmail.com", "!U0Thithe&81")
        server.sendmail(sender_email, receiver_email, send_message)
