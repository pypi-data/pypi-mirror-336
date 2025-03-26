'''
    SMTP client module
'''

import smtplib
import ssl
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email.mime.image import MIMEImage
from villog.log import Logger

class MailMan:
    '''
        SMTP client class
    '''
    __slots__: list[str] = ["smtp_server",
                            "smtp_login",
                            "smtp_port",
                            "smtp_password",
                            "name",
                            "do_logs",
                            "logger"]

    def __init__(self,
                 smtp_server: str,
                 smtp_login: str,
                 smtp_port: int,
                 smtp_password: str,
                 name: str,
                 do_logs: bool = True,
                 logger: Logger | None = None) -> None:
        '''
            SMTP client class

            Args:
                smtp_server (str): SMTP server
                smtp_login (str): SMTP login
                smtp_port (int): SMTP port
                smtp_password (str): SMTP password
                name (str): Name
                do_logs (bool): Do logs
                logger (Logger): Logger
        '''
        self.smtp_server: str = smtp_server
        self.smtp_login: str = smtp_login
        self.smtp_port: str = smtp_port
        self.smtp_password: str = smtp_password
        self.name: str = name
        self.do_logs: bool = do_logs
        self.logger: Logger | None = logger if logger or do_logs else (Logger() if do_logs else None) # pylint: disable=line-too-long


    def __str__(self) -> str:
        return f"{self.smtp_login}@{self.smtp_server}:{self.smtp_port}"


    def __log(self,
              content: str) -> None:
        '''Log content'''
        if self.do_logs:
            self.logger.log(content)
        else:
            print(content)

    def send(self,
             subject: str,
             body: str,
             send_to: list[str],
             files: list[str] | None = None,
             images: list[str] | None = None) -> None:
        '''
            Send e-mail

            Args:
                subject (str): Subject
                body (str): Body
                send_to (list[str]): Send to e-mail addresses
                files (list[str]): Files path
                images (list[str]): Images path
        '''
        self.__log(f"Sending mail {subject}")
        assert isinstance(send_to, list)
        msg: MIMEMultipart = MIMEMultipart()
        msg["From"] = f'{self.name} <{self.smtp_login}>'
        msg["To"] = COMMASPACE.join(send_to)
        msg["Date"] = formatdate(localtime = True)
        msg["Subject"] = subject
        context: ssl.SSLContext = ssl.create_default_context()

        msg.attach(MIMEText(body,
                            "html"))

        if images:
            for image in images:
                with open(image[0],
                          "rb") as file:
                    img: MIMEImage = MIMEImage(file.read())
                    img.add_header('Content-ID', "<" + image[1] + ">")
                    msg.attach(img)

        for f in files or []:
            with open(f, "rb") as file:
                part: MIMEApplication = MIMEApplication(
                    file.read(),
                    Name=basename(f)
                )
            part['Content-Disposition'] = f'attachment; filename="{basename(f)}"'
            msg.attach(part)
        smtp: smtplib.SMTP_SSL = smtplib.SMTP_SSL(self.smtp_server,
                                self.smtp_port,
                                context = context)
        smtp.login(self.smtp_login,
                   self.smtp_password)
        smtp.sendmail(self.smtp_login, 
                      send_to, msg.as_string())
        self.__log(f"Mail sent to {send_to}")
        smtp.close()
