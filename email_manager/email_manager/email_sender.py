__author__ = 'Luoxuan'
# coding: UTF-8

import smtplib


class EmailSender(object):
    def __init__(self):
        self.server_addr = None
        self.server_port = None
        self.login_user = None
        self.login_passwd = None
        self.use_ssl = None
        self.using_debug = None

    def set_server_with_config(self, config):
        self.server_addr = config.server_addr
        self.server_port = config.server_port
        self.login_user = config.login_user_name
        self.login_passwd = config.login_user_passwd
        self.use_ssl = config.using_ssl
        self.using_debug = config.using_debug

    def set_server_with_info(self, server_addr, server_port, login_user, login_passwd,\
                             use_ssl=False, using_debug=False):
        self.server_addr = server_addr
        self.server_port = server_port
        self.login_user = login_user
        self.login_passwd = login_passwd
        self.use_ssl = use_ssl
        self.using_debug = using_debug

    def _check_none(self):
        if self.server_addr is None or self.use_ssl is None or self.login_passwd is None or\
                self.login_user is None or self.server_port is None:
            return False
        return True

    def test_login(self):
        if not self._check_none():
            return False, "Params Error"
        smtp = smtplib.SMTP()
        try:
            if self.using_debug:
                smtp.set_debuglevel(1)
            smtp.connect(self.server_addr, self.server_port)
            if self.use_ssl:
                smtp.starttls()
            smtp.login(self.login_user, self.login_passwd)
            smtp.quit()
        except smtplib.SMTPConnectError, e:
            return False, "Connection Error: %s" % e.message
        except smtplib.SMTPAuthenticationError, e:
            return False, "Auth Error: %s" % e.message
        except Exception, e:
            return False, "Unknown Error: %s" % e.message
        return True, "success"

    def send_email(self, from_addr, to_addrs, msg):
        if not self._check_none():
            return False, "Params Error"
        smtp = smtplib.SMTP()
        try:
            if self.using_debug:
                smtp.set_debuglevel(1)
            smtp.connect(self.server_addr, self.server_port)
            if self.use_ssl:
                smtp.starttls()
            smtp.login(self.login_user, self.login_passwd)
            smtp.sendmail(from_addr, to_addrs, msg)
            smtp.quit()
        except smtplib.SMTPDataError, e:
            return False, "Data Error: %s" % e.message
        except smtplib.SMTPConnectError, e:
            return False, "Connection Error: %s" % e.message
        except smtplib.SMTPAuthenticationError, e:
            return False, "Auth Error: %s" % e.message
        return True, "success"

if __name__ == '__main__':
    sender = EmailSender()
    import email_config
    sender.set_server_with_config(email_config)
    sender.test_login()

