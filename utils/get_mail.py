import imaplib
import os
import email
import json
from typing import Any
from pathlib import Path
import glob
from zipfile import ZipFile
import getpass
import keyring

from utils.get_xml import get_xml
from email.message import EmailMessage
from utils.get_pdf_info import get_pdf
from utils.send_to_trash import send_to_trash


def check_password(service: str, user: str, save=False) -> str:
    credentials = keyring.get_credential(service, user)
    if credentials is None and save is True:
        keyring.set_password(service, user, getpass.getpass())
    return str(keyring.get_password(service, user))


class get_mail:
    csv: dict[Any, Any]
    fN_pdf: list
    fN_xml: list
    fN_pdf_path = list
    fN_xml_path = list
    fN_name = list
    files = list
    filearray = list

    def __init__(self, path: Path, email_user: str, month_search: str, year_search: int, service: str):
        self.mail = None
        self.subject = ''
        self.path = path
        self.month_search = month_search
        self.year_search = year_search
        self.csv = dict()
        self.list_to_trash = list()
        self.file = str()
        self.filePath = str()
        # self.fileName = str()
        self.check_xml = str()
        self.check_pdf = str()
        self.fN_pdf = list()
        self.fN_xml = list()
        self.fN_pdf_path = list()
        self.fN_xml_path = list()
        self.fN_name = list()
        self.files = list()
        self.filearray = list()
        email_pass = check_password(service=service, user=email_user, save=True)  # Save should be a button in IDE
        mail_server = email_user.split('@')[-1]
        self.login(user=email_user, password=email_pass, server=mail_server)
        typ, data = self.check_date(self.month_search, self.mail, self.year_search)
        self.read_data_from_mail(data=data)
        # self.double_check()

    def login(self, user: str, password: str, server: str) -> None:
        self.mail = imaplib.IMAP4_SSL(f'imap.{server}')
        self.mail.login(user, password)
        self.mail.select('Inbox')

    @staticmethod
    def check_date(month_search: str, mail: object, year: int):
        if '01' in month_search:
            print('JAN')
            typ, data = mail.search(None, f'(SINCE "01-Jan-{year}" BEFORE "31-Jan-{year}")')

        elif '02' in month_search:
            print('FEB')
            typ, data = mail.search(None, f'(SINCE "01-Feb-{year}" BEFORE "01-Mar-{year}")')

        elif '03' in month_search:
            print('MAR')
            typ, data = mail.search(None, f'(SINCE "01-Mar-{year}" BEFORE "01-Apr-{year}")')

        elif '04' in month_search:
            print('APR')
            typ, data = mail.search(None, f'(SINCE "01-Apr-{year}" BEFORE "01-Jun-{year}")')

        elif '05' in month_search:
            print('MAY')
            typ, data = mail.search(None, f'(SINCE "01-May-{year}" BEFORE "01-Jun-{year}")')

        elif '06' in month_search:
            print('JUN')
            typ, data = mail.search(None, f'(SINCE "01-Jun-{year}" BEFORE "01-Jul-{year}")')

        elif '07' in month_search:
            print('JUL')
            typ, data = mail.search(None, f'(SINCE "01-Jul-{year}" BEFORE "01-Aug-{year}")')

        elif '08' in month_search:
            print('AUG')
            typ, data = mail.search(None, f'(SINCE "01-Aug-{year}" BEFORE "01-Sep-{year}")')

        elif '09' in month_search:
            print('SEP')
            typ, data = mail.search(None, f'(SINCE "01-Sep-{year}" BEFORE "01-Oct-{year}")')

        elif '10' in month_search:
            print('OCT')
            typ, data = mail.search(None, f'(SINCE "01-Oct-{year}" BEFORE "01-Nov-{year}")')

        elif '11' in month_search:
            print('NOV')
            typ, data = mail.search(None, f'(SINCE "01-Nov-{year}" BEFORE "01-Dec-{year}")')

        elif '12' in month_search:
            print('DEC')
            typ, data = mail.search(None, f'(SINCE "01-Dec-{year}" BEFORE "01-Jan-{year + 1}")')
        else:
            raise Exception
        return typ, data

    def read_data_from_mail(self, data) -> None:
        for num in data[0].split():
            typ, data = self.mail.fetch(num, '(RFC822)')
            # noinspection PyUnresolvedReferences
            raw_email = data[0][1]  # converts byte literal to string removing b''
            self.raw_email_encoding = json.detect_encoding(raw_email)
            self.email_message = email.message_from_bytes(raw_email, _class=EmailMessage)  # downloading attachments
            self.read_mail()
            if self.filePath is not None:
                if '.xml' in str(self.filePath):
                    try:
                        self.mail_check()
                    except AttributeError:
                        pass
                elif '.XML' in str(self.filePath):
                    try:
                        self.mail_check()
                    except AttributeError:
                        pass

    def read_mail(self):
        for part in self.email_message.walk():
            if self.email_message.is_attachment():
                email_message = self.email_message.decode(self.raw_email_encoding)
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            self.fileName = part.get_filename()
            self.files.append(self.fileName)
            if ('xml' or 'pdf' in self.fileName) and self.fileName is not None:
                # self.filePath = os.path.join(str(self.path), self.fileName)
                self.filePath = Path(self.path / self.fileName)
                if '.xml' in str(self.filePath):
                    self.check_xml = self.filePath
                if '.pdf' in str(self.filePath):
                    self.check_pdf = self.filePath
                else:
                    pass
                if not os.path.isfile(self.filePath):
                    try:
                        self.fp = open(self.filePath, 'wb')
                        self.fp.write(part.get_payload(decode=True))
                        self.fp.close()
                    except FileNotFoundError:
                        self.filePath = ''
        self.manage_mail()

    def manage_mail(self):
        if self.filePath != '':
            if '.xml' in str(self.filePath):
                try:
                    self.mail_check()
                except AttributeError:
                    pass
            elif '.XML' in str(self.filePath):
                try:
                    self.mail_check()
                except AttributeError:
                    pass
            elif '.pdf' in str(self.filePath):
                pass
            elif '.zip' in str(self.filePath):
                self.unzip_file()

    def unzip_file(self):
        with ZipFile(str(self.filePath), 'r') as zfile:
            zfile.extractall(path=str(self.path))
        zfile.close()

    def mail_check(self):
        check_xml_loc = self.check_xml
        print(check_xml_loc)  # For debugging purposes
        try:
            with open(check_xml_loc, 'r', encoding='utf-8') as file:
                my_xml = file.read()
                self.csv = self.csv
                self.list_to_trash = self.list_to_trash
                if os.stat(check_xml_loc).st_size <= 2:
                    print(f"EXCEPTION OCCURRED IN {check_xml_loc}")
                    send_to_trash(Path(check_xml_loc))
                else:
                    self.file = get_xml(file_path=self.filePath, xml=my_xml, csv=self.csv,
                                        list_to_trash=self.list_to_trash,
                                        month=self.month_search, year=self.year_search)

        except FileNotFoundError:
            print("File not found")

    def pdf_check(self, a):
        check_pdf_loc = self.check_pdf
        if a == 0:
            self.drop_names = []
        else:
            self.drop_names = self.drop_names
        self.my_pdf = get_pdf(check_pdf_loc, drop_names=self.drop_names)

    def logout(self, exit_flag: bool = True):
        if exit_flag:
            self.mail.logout()
            self.mail.close()

    def double_check(self):
        for f in glob.glob(f"{self.path}/*xml"):
            try:
                with open(f, 'r', encoding='utf-8') as df:
                    self.csv = self.csv
                    self.list_to_trash = self.list_to_trash
                    my_xml = df.read()
                    print(my_xml)
                    try:
                        self.file = get_xml(file_path=f, xml=my_xml, csv=self.csv,
                                            list_to_trash=self.list_to_trash,
                                            month=self.month_search, year=self.year_search)
                    except OSError:
                        print(OSError)
            except Exception as e:
                print(e)
