__author__ = 'Luoxuan'
# coding: UTF-8

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from email.mime.image import MIMEImage


class EmailMessage(object):
    def __init__(self):
        self.msg = None


class PureTextMessage(EmailMessage):
    def __init__(self, text, charset='utf-8'):
        self.msg = MIMEText(_text=text, _subtype='plain', _charset=charset)


class HtmlTextMessage(EmailMessage):
    def __init__(self, text, charset='utf-8'):
        self.msg = MIMEText(_text=text, _subtype='html', _charset=charset)


class WithFileMessage(EmailMessage):
    def __init__(self, part_type='related'):
        self.msg = MIMEMultipart(part_type)

    def add_file_part(self, file_name=u"未命名", data=None, file_type='application/octet-stream', path=None):
        if '/' not in file_type:
            raise Exception(message='file_type params error format!')
        main_type, sub_type = file_type.split('/', 1)
        if path and not data:
            fp = open(path, 'rb')
            data = fp.read()
            fp.close()
        part = MIMEBase(main_type, sub_type)
        part.set_payload(data)
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % file_name)
        self.msg.attach(part)

    def add_pure_part(self, text, charset='utf-8'):
        part = MIMEText(_text=text, _subtype='plain', _charset=charset)
        self.msg.attach(part)

    def add_html_part(self, text, charset='utf-8'):
        part = MIMEText(_text=text, _subtype='html', _charset=charset)
        self.msg.attach(part)

    def add_image_part(self, image_id, image_data, path=None):
        if path and not image_data:
            fp = open(path, 'rb')
            image_data = fp.read()
            fp.close()

        part = MIMEImage(_imagedata=image_data)
        part.add_header('Content-ID', image_id)
        self.msg.attach(part)
