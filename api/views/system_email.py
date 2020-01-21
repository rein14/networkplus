from django.conf import settings

import smtplib
from email.mime.text import MIMEText


class ParadeEmail():

    def __int__(self):
        pass

    def send_email(self,subject,to_address,from_address,message):

        try:
            #
            # print(subject)
            # print(to_address)
            # print(from_address)
            # print(message)

            sender = from_address
            recipient = to_address
            message =  message

            msg = MIMEText(message, 'html')
            msg['Subject'] = subject
            msg['From'] = sender
            msg['To'] = recipient

            server = smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT)
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.sendmail(sender, [recipient], msg.as_string())
            server.quit()
            # END confirmation email
            return True
        except:
            return False


