import smtplib
from email.message import EmailMessage


# Creditials
# login with google app password since less secure app of google discontinue fom may 30 2022
sender = 'sendmail259@gmail.com'
#password = '123456789hello'
password='vdqnykmqrbymzimk'

def sendmail(emailid,token):
    receiver = emailid
    try:
        # creating email format:
        message = EmailMessage()
        message['Subject'] = "Password Reset"
        message['From'] = sender
        message['To'] = receiver
        body = f'<h1>hi, this is your requested Reset Password link:</h1><a href="http://127.0.0.1:8000/auth/resetPassword/{token}">Click here</a>'

        # no need subtype for plain text
        message.set_content(body, subtype='html')

        # creating smtp object
        server = smtplib.SMTP('smtp.gmail.com', 587)
        # tts-transfer layer security improved version of ssl
        server.starttls()
        
        server.login(sender, password)
        # sending mail to target
        server.send_message(message)
        # quiting session
        server.quit()

        
        return True
    except:
        
        print("Error: unable to send email")
        return False
