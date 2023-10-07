from dataclasses import dataclass
from typing import List

@dataclass
class MailAdress:
	name: str
	domain: str

@dataclass
class Mail:
	sender: MailAdress
	receiver: MailAdress
	subject: str
	body: str
	
@dataclass
class MailAccount:
	name: str
	inbox: List[Mail]
	outbox: List[Mail]

@dataclass
class MailServer:
	domain: str
	accounts: List[MailAccount]
	
def show_mail_address(addr: MailAdress):
	print(addr.name,'@',addr.domain,end='')
def show_mail(mail: Mail)
def show_mail_account
def show_mail_server