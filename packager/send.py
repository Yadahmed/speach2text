# sherakany software


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


def send_email(sender_email, sender_password, recipient_emails, subject, message, attachment_path):
    # Create the email message object
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ', '.join(recipient_emails)
    msg['Subject'] = subject

    # Attach the message body
    msg.attach(MIMEText(message, 'plain'))

    # Read the attachment file
    with open(attachment_path, 'rb') as attachment_file:
        attachment = MIMEApplication(attachment_file.read())

    # Set the filename of the attachment
    attachment.add_header('Content-Disposition',
                          'attachment', filename=attachment_path)

    # Attach the file to the email message
    msg.attach(attachment)

    # Connect to the SMTP server
    # Change the server and port accordingly
    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_server.starttls()

    try:
        # Login to your email account
        smtp_server.login(sender_email, sender_password)

        # Send the email
        smtp_server.send_message(msg)
        print("Email sent successfully!")

    except Exception as e:
        print("An error occurred while sending the email:", str(e))

    finally:
        # Close the connection to the SMTP server
        smtp_server.quit()


# Usage example
sender_email = "lanyax15@gmail.com"
sender_password = "hexpioirjsgpwyhs"
recipient_emails = ["lk21266@auis.edu.krd",]
subject = "Sample Email with Attachment"
message = "Hello,\n\nPlease find the attached file.\n\nRegards,\nSender"
attachment_path = "C:\\Users\\lanya\\Desktop\\Hproject\\test.txt"

send_email(sender_email, sender_password, recipient_emails,
           subject, message, attachment_path)
