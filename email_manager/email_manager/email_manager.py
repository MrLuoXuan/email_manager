__author__ = 'Luoxuan'
# coding: UTF-8

import types
import base64

from email.utils import COMMASPACE, formatdate


class EmailManager(object):
    def __init__(self, email_message, email_sender):
        self.sender = email_sender
        self.message = email_message

    def send_mail(self, from_addr, recv_addr, cc_addr=None, bcc_addr=None, title=''):
        self.message.msg['From'] = from_addr
        if type(title) == types.UnicodeType:
            self.message.msg['Subject'] = '=?UTF-8?B?%s?=' % (base64.b64encode(title.encode('utf-8')))
        else:
            self.message.msg['Subject'] = '=?UTF-8?B?%s?=' % (base64.b64encode(title))
        if type(recv_addr) in (types.TupleType, types.ListType):
            self.message.msg['To'] = COMMASPACE.join(recv_addr)
        else:
            self.message.msg['To'] = recv_addr
        self.message.msg['Date'] = formatdate(localtime=True)
        if cc_addr:
            self.message.msg['Cc'] = cc_addr
        if bcc_addr:
            self.message.msg['Bcc'] = bcc_addr
        self.sender.send_email(from_addr, recv_addr, self.message.msg.as_string())


if __name__ == '__main__':
    from email_config import EmailConfig
    from email_sender import EmailSender
    from email_message import WithFileMessage

    sender = EmailSender()
    sender.set_server_with_config(EmailConfig)
    msg = WithFileMessage()
    html = u"<html> 妞妞: <img src='cid:image1'/> </html>"
    msg.add_html_part(html)
    msg.add_image_part('<image1>', None, 'D:\\Downloads\\111.jpg')
    msg.add_file_part('pic.jpg', None, path='D:\\Downloads\\111.jpg')
    manager = EmailManager(msg, sender)
    manager.send_mail('luoxuan@buestc.com', 'luoxuan@buestc.com', title='Beautiful Girl!')