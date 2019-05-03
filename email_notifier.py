from notifier import Notifier
import smtplib


class EmailNotifier(Notifier):
    """
    Responsible for notifying the user via email
    """

    def __init__(self, sender, receiver, smtp_server, password, message):
        """

        :param sender:  the sender's email
        :param receiver: the receiver's email
        :param smtp_server: smtp server to send through
        :param password: password for the sender's account
        :param message: message to display at the mail
        """
        self._server = smtplib.SMTP(smtp_server)
        self._server.login(sender, password)

        self._sender = sender
        self._receiver = receiver
        self._message = message

    def notify(self, log_id):
        self._server.sendmail(self._sender, self._receiver, self._message)
