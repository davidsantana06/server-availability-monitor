import logging
import smtplib
from email.message import EmailMessage

from app.dtos import SmtpConfig, UserInfo


logger = logging.getLogger(__name__)


def send(
    smtp_config: SmtpConfig,
    user_infos: list[UserInfo],
    subject: str,
    body: str,
) -> None:
    valid_recipients = [u.email for u in user_infos if u.validate()[0]]
    if not valid_recipients:
        logger.warning("no valid recipients, skipping email: %s", subject)
        return

    msg = EmailMessage()
    msg["From"] = smtp_config.from_address
    msg["To"] = ", ".join(valid_recipients)
    msg["Subject"] = subject
    msg.set_content(body)

    try:
        with smtplib.SMTP(smtp_config.host, smtp_config.port) as smtp:
            if smtp_config.use_tls:
                smtp.starttls()
            smtp.login(smtp_config.username, smtp_config.password)
            smtp.send_message(msg)
        logger.info("email sent to %s subject=%r", valid_recipients, subject)
    except Exception as error:
        logger.error("failed to send email subject=%r: %s", subject, error)
        raise
