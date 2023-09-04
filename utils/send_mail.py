import smtplib
import win32com.client as win32
from typing import Union, Optional

def send_mail_SMTP(message: str, attachment, sender: str, receiver: Union[Optional[str, list]]) -> None:
    message = (f"From: From Turbocompressor <{sender}>\n"
               f"    To: To {receiver} <t{receiver}>\n"
               "    Subject: SMTP email example\n"
               "\n"
               "\n"
               "    This is a test message.\n"
               "    ")
    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail(sender, receiver, message)
        print("Successfully sent email")
    except smtplib.SMTPException:
        pass

def send_mail_win32():
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = 'To address'
    mail.Subject = 'Message subject'
    mail.Body = 'Message body'
    mail.HTMLBody = '<h2>HTML Message body</h2>'  # this field is optional

    # To attach a file to the email (optional):
    attachment = "Path to the attachment"
    mail.Attachments.Add(attachment)

    mail.Send()