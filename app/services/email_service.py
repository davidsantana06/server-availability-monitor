import smtplib
from email.message import EmailMessage

from app.dtos import SmtpConfig, UserInfo
from app.services import log_service


_SMTP_TIMEOUT_IN_SECONDS = 10


def send(
    smtp_config: SmtpConfig,
    user_infos: list[UserInfo],
    subject: str,
    body: str,
) -> None:
    valid_recipients = [u.email for u in user_infos if u.validate()[0]]
    if not valid_recipients:
        log_service.emit_warning("no valid recipients, skipping email: %s", subject)
        return

    msg = EmailMessage()
    msg["From"] = smtp_config.from_address
    msg["To"] = ", ".join(valid_recipients)
    msg["Subject"] = subject
    msg.set_content(body)

    try:
        with smtplib.SMTP(smtp_config.host, smtp_config.port, timeout=_SMTP_TIMEOUT_IN_SECONDS) as smtp:
            if smtp_config.use_tls:
                smtp.starttls()
            smtp.login(smtp_config.username, smtp_config.password)
            smtp.send_message(msg)
        log_service.emit_info("email sent to %s subject=%r", valid_recipients, subject)
    except Exception as error:
        log_service.emit_error("failed to send email subject=%r: %s", subject, error)
        raise
