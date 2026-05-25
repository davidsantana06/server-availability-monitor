from app.dtos import ServerConfig, SmtpConfig, UserInfo
from app.services import email_service, log_service


logger = log_service.get_instance(__name__)


def _format_server_list(server_configs: list[ServerConfig]) -> str:
    return "\n".join(
        f"  - {s.hostname} ({s.host}:{s.port})" for s in server_configs
    )


def notify_offline(
    new_offline: list[ServerConfig],
    user_infos: list[UserInfo],
    smtp_config: SmtpConfig,
) -> None:
    def _subject() -> str:
        return f"[ALERT] {len(new_offline)} server(s) went offline"

    def _body() -> str:
        return "The following servers are now offline:\n\n" + _format_server_list(new_offline)

    email_service.send(smtp_config, user_infos, _subject(), _body())


def notify_recovery(
    recovered: list[ServerConfig],
    still_offline: list[ServerConfig],
    user_infos: list[UserInfo],
    smtp_config: SmtpConfig,
) -> None:
    def _subject() -> str:
        return f"[RECOVERY] {len(recovered)} server(s) back online"

    def _body() -> str:
        body = "The following servers are back online:\n\n" + _format_server_list(recovered)
        if still_offline:
            body += "\n\nServers still offline:\n\n" + _format_server_list(still_offline)
        return body

    email_service.send(smtp_config, user_infos, _subject(), _body())


def notify_reminder(
    offline: list[ServerConfig],
    user_infos: list[UserInfo],
    smtp_config: SmtpConfig,
) -> None:
    def _subject() -> str:
        return f"[REMINDER] {len(offline)} server(s) still offline"

    def _body() -> str:
        return "The following servers are still offline:\n\n" + _format_server_list(offline)

    email_service.send(smtp_config, user_infos, _subject(), _body())
