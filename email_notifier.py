from notifier import Notifier
import smtplib


class EmailNotifier(Notifier):
    """
    Responsible for notifying the user via email
    """
    MESSAGE = """\
Subject: New Log

New log had been registered
check out the website or the application."""

    def __init__(self, sender, receiver, smtp_server, password):
        """

        :param sender:  the sender's email
        :param receiver: the receiver's email
        :param smtp_server: smtp server to send through
        :param password: password for the sender's account
        :param message: message to display at the mail
        """
        self._server = smtplib.SMTP_SSL(smtp_server)
        self._server.login(sender, password)

        self._sender = sender
        self._receiver = receiver

    def notify(self, log_id):
        self._server.sendmail(self._sender, self._receiver, EmailNotifier.MESSAGE)
