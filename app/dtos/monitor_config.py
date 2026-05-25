import re
from dataclasses import dataclass

from ._base import Base


_EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@dataclass(frozen=True)
class SmtpConfig(Base):
    host: str
    port: int
    username: str
    password: str
    use_tls: bool
    from_address: str

    def __is_host_valid(self) -> bool:
        return isinstance(self.host, str) and len(self.host.strip()) > 0

    def __is_port_valid(self) -> bool:
        return (
            isinstance(self.port, int)
            and not isinstance(self.port, bool)
            and 1 <= self.port <= 65535
        )

    def __is_username_valid(self) -> bool:
        return isinstance(self.username, str) and len(self.username.strip()) > 0

    def __is_password_valid(self) -> bool:
        return isinstance(self.password, str) and len(self.password) > 0

    def __is_use_tls_valid(self) -> bool:
        return isinstance(self.use_tls, bool)

    def __is_from_address_valid(self) -> bool:
        return (
            isinstance(self.from_address, str)
            and _EMAIL_REGEX.match(self.from_address) is not None
        )

    def validate(self) -> Base.DTOValidation:
        return self._aggregate([
            (self.__is_host_valid(), f"invalid smtp.host: {self.host!r}"),
            (self.__is_port_valid(), f"invalid smtp.port: {self.port!r}"),
            (self.__is_username_valid(), f"invalid smtp.username: {self.username!r}"),
            (self.__is_password_valid(), "invalid smtp.password"),
            (self.__is_use_tls_valid(), f"invalid smtp.use_tls: {self.use_tls!r}"),
            (
                self.__is_from_address_valid(),
                f"invalid smtp.from_address: {self.from_address!r}",
            ),
        ])


@dataclass(frozen=True)
class TimingConfig(Base):
    check_interval_in_seconds: int
    check_timeout_in_seconds: int
    notification_interval_in_seconds: int

    def __is_check_interval_in_seconds_valid(self) -> bool:
        return (
            isinstance(self.check_interval_in_seconds, int)
            and not isinstance(self.check_interval_in_seconds, bool)
            and self.check_interval_in_seconds > 0
        )

    def __is_check_timeout_in_seconds_valid(self) -> bool:
        return (
            isinstance(self.check_timeout_in_seconds, int)
            and not isinstance(self.check_timeout_in_seconds, bool)
            and self.check_timeout_in_seconds > 0
        )

    def __is_notification_interval_in_seconds_valid(self) -> bool:
        return (
            isinstance(self.notification_interval_in_seconds, int)
            and not isinstance(self.notification_interval_in_seconds, bool)
            and self.notification_interval_in_seconds > 0
        )

    def validate(self) -> Base.DTOValidation:
        return self._aggregate([
            (
                self.__is_check_interval_in_seconds_valid(),
                f"invalid timing.check_interval_in_seconds: {self.check_interval_in_seconds!r}",
            ),
            (
                self.__is_check_timeout_in_seconds_valid(),
                f"invalid timing.check_timeout_in_seconds: {self.check_timeout_in_seconds!r}",
            ),
            (
                self.__is_notification_interval_in_seconds_valid(),
                f"invalid timing.notification_interval_in_seconds: {self.notification_interval_in_seconds!r}",
            ),
        ])


@dataclass(frozen=True)
class PathsConfig(Base):
    servers_config_file: str
    user_info_file: str
    logs_folder: str

    def __is_servers_config_file_valid(self) -> bool:
        return (
            isinstance(self.servers_config_file, str)
            and len(self.servers_config_file.strip()) > 0
        )

    def __is_user_info_file_valid(self) -> bool:
        return isinstance(self.user_info_file, str) and len(self.user_info_file.strip()) > 0

    def __is_logs_folder_valid(self) -> bool:
        return isinstance(self.logs_folder, str) and len(self.logs_folder.strip()) > 0

    def validate(self) -> Base.DTOValidation:
        return self._aggregate([
            (
                self.__is_servers_config_file_valid(),
                f"invalid paths.servers_config_file: {self.servers_config_file!r}",
            ),
            (
                self.__is_user_info_file_valid(),
                f"invalid paths.user_info_file: {self.user_info_file!r}",
            ),
            (
                self.__is_logs_folder_valid(),
                f"invalid paths.logs_folder: {self.logs_folder!r}",
            ),
        ])


@dataclass(frozen=True)
class MonitorConfig(Base):
    smtp: SmtpConfig
    timing: TimingConfig
    paths: PathsConfig

    def validate(self) -> Base.DTOValidation:
        return self._aggregate([
            self.smtp.validate(),
            self.timing.validate(),
            self.paths.validate(),
        ])
