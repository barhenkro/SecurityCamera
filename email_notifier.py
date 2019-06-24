from notifier import Notifier
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from databases import log_database_instance, face_database_instance
import os


class EmailNotifier(Notifier):
    """
    Responsible for notifying the user via email
    """
    PLAIN_TEXT = """{name} was seen at {date}
    for more information, check the website
    """

    HTML_TEXT = """\
<html>
  <body>
  <p>{name} was seen at {date}</p>
  <img src="cid:0"><img>
  <p>for more information, check the website<p>
  </body>
</html>
"""

    def __init__(self, sender, receivers, smtp_server, password):
        """

        :param sender:  the sender's email
        :param receiver: the receiver's email
        :param smtp_server: smtp server to send through
        :param password: password for the sender's account
        """
        self._server = smtplib.SMTP_SSL(smtp_server)
        self._server.login(sender, password)

        self._sender = sender
        self._receivers = receivers

    def notify(self, log_id):
        # getting data about the log
        log = log_database_instance[log_id]
        date = log.time_string
        image_path = os.path.join('static', log.image_path)
        name = face_database_instance[log.face_id].name

        if name is None:
            name = "Unrecognized face"

        # creating image part
        with open(image_path, 'rb') as file_handler:
            image_part = MIMEImage(file_handler.read())

        image_part.add_header('Content-Disposition', 'attachment', filename='face.jpg')
        image_part.add_header('X-Attachment-Id', '0')
        image_part.add_header('Content-ID', '<0>')

        # Create the plain-text and HTML version of your message
        text = EmailNotifier.PLAIN_TEXT.format(name=name, date=date)
        html = EmailNotifier.HTML_TEXT.format(name=name, date=date)
        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        message = MIMEMultipart("alternative")
        message["Subject"] = "New Log"
        message["From"] = self._sender
        message["To"] = ",".join(self._receivers)
        message.attach(part1)
        message.attach(part2)
        message.attach(image_part)

        self._server.sendmail(self._sender, self._receivers, message.as_string())
