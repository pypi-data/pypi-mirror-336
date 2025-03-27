import sys
from email.message import EmailMessage
from enum import Enum, auto
from logging import Logger
from smtplib import SMTP
from typing import Any, Final

from .file_pomes import Mimetype
from .env_pomes import APP_PREFIX, env_get_str, env_get_int


class EmailParam(Enum):
    """
    Parameters for connecting to email servers.
    """
    ACCOUNT = auto()
    PWD: auto()
    PORT: auto()
    HOST: auto()
    SECURITY: auto()

    def __str__(self) -> str:  # noqa: D105
        return self.name


EMAIL_SERVER: Final[dict[EmailParam, Any]] = {
    EmailParam.HOST: env_get_str(key=f"{APP_PREFIX}_EMAIL_SERVER"),
    EmailParam.PORT: env_get_int(key=f"{APP_PREFIX}_EMAIL_PORT"),
    EmailParam.ACCOUNT: env_get_str(key=f"{APP_PREFIX}_EMAIL_ACCOUNT"),
    EmailParam.PWD: env_get_str(key=f"{APP_PREFIX}_EMAIL_PWD"),
    EmailParam.SECURITY: env_get_str(key=f"{APP_PREFIX}_EMAIL_SECURITY")
}


def email_send(errors: list[str] | None,
               user_email: str,
               subject: str,
               content: str,
               content_type: Mimetype = Mimetype.TEXT,
               logger: Logger = None) -> None:
    """
    Send email to *user_email*, with *subject* as the email subject, and *content* as the email message.

    :param errors: incidental error messages
    :param user_email: the address to send the email to
    :param subject: the email subject
    :param content: the email message
    :param content_type: the mimetype of the content (defaults to *text/plain*)
    :param logger: optional logger
    """
    # import needed function
    from .exception_pomes import exc_format

    # build the email object
    email_msg = EmailMessage()
    email_msg["From"] = EMAIL_SERVER.get(EmailParam.ACCOUNT)
    email_msg["To"] = user_email
    email_msg["Subject"] = subject
    if content_type == Mimetype.HTML:
        email_msg.set_content("Your browser does not support HTML.")
        email_msg.add_alternative(content,
                                  subtype="html")
    else:
        email_msg.set_content(content)

    # send the message
    try:
        # instanciate the email server, login and send the email
        with SMTP(host=EMAIL_SERVER.get(EmailParam.HOST),
                  port=EMAIL_SERVER.get(EmailParam.PORT)) as server:
            if EMAIL_SERVER.get(EmailParam.SECURITY) == "tls":
                server.starttls()
            server.login(user=EMAIL_SERVER.get(EmailParam.ACCOUNT),
                         password=EMAIL_SERVER.get(EmailParam.PWD))
            server.send_message(msg=email_msg)
            if logger:
                logger.debug(msg=f"Sent email '{subject}' to '{user_email}'")
    except Exception as e:
        # the operatin raised an exception
        exc_err: str = exc_format(exc=e,
                                  exc_info=sys.exc_info())
        err_msg: str = f"Error sending the email: {exc_err}"
        if logger:
            logger.error(msg=err_msg)
        if isinstance(errors, list):
            errors.append(err_msg)
