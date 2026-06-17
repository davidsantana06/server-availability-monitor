from app.dtos import ServersPool, SmtpConfig, UsersInfo
from app.services import email_service


def _format_server_list(server_configs: list[ServersPool]) -> str:
    return "\n".join(
        f"  - {s.hostname} ({s.host}:{s.port})" for s in server_configs
    )


def notify_offline(
    new_offline: list[ServersPool],
    user_infos: list[UsersInfo],
    smtp_config: SmtpConfig,
) -> None:
    def build_subject() -> str:
        return f"[ALERT] {len(new_offline)} server(s) went offline"

    def build_body() -> str:
        return "The following servers are now offline:\n\n" + _format_server_list(new_offline)

    email_service.send(smtp_config, user_infos, build_subject(), build_body())


def notify_recovery(
    recovered: list[ServersPool],
    still_offline: list[ServersPool],
    user_infos: list[UsersInfo],
    smtp_config: SmtpConfig,
) -> None:
    def build_subject() -> str:
        return f"[RECOVERY] {len(recovered)} server(s) back online"

    def build_body() -> str:
        body = "The following servers are back online:\n\n" + _format_server_list(recovered)
        if still_offline:
            body += "\n\nServers still offline:\n\n" + _format_server_list(still_offline)
        return body

    email_service.send(smtp_config, user_infos, build_subject(), build_body())


def notify_reminder(
    offline: list[ServersPool],
    user_infos: list[UsersInfo],
    smtp_config: SmtpConfig,
) -> None:
    def build_subject() -> str:
        return f"[REMINDER] {len(offline)} server(s) still offline"

    def build_body() -> str:
        return "The following servers are still offline:\n\n" + _format_server_list(offline)

    email_service.send(smtp_config, user_infos, build_subject(), build_body())
