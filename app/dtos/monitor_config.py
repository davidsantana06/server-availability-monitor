import re
from dataclasses import dataclass

from app.types import DtoValidation


_EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@dataclass(frozen=True)
class SmtpConfig:
    host: str
    port: int
    username: str
    password: str
    use_tls: bool
    from_address: str

    def __is_host_valid(self) -> bool:
        return isinstance(self.host, str) and len(self.host.strip()) > 0

    def __is_port_valid(self) -> bool:
        return isinstance(self.port, int) and not isinstance(self.port, bool) and 1 <= self.port <= 65535

    def __is_username_valid(self) -> bool:
        return isinstance(self.username, str) and len(self.username.strip()) > 0

    def __is_password_valid(self) -> bool:
        return isinstance(self.password, str) and len(self.password) > 0

    def __is_use_tls_valid(self) -> bool:
        return isinstance(self.use_tls, bool)

    def __is_from_address_valid(self) -> bool:
        return isinstance(self.from_address, str) and _EMAIL_REGEX.match(self.from_address) is not None

    def validate(self) -> DtoValidation:
        errors = []
        if not self.__is_host_valid():
            errors.append(f"invalid smtp.host: {self.host!r}")
        if not self.__is_port_valid():
            errors.append(f"invalid smtp.port: {self.port!r}")
        if not self.__is_username_valid():
            errors.append(f"invalid smtp.username: {self.username!r}")
        if not self.__is_password_valid():
            errors.append("invalid smtp.password")
        if not self.__is_use_tls_valid():
            errors.append(f"invalid smtp.use_tls: {self.use_tls!r}")
        if not self.__is_from_address_valid():
            errors.append(f"invalid smtp.from_address: {self.from_address!r}")
        return (not errors, "; ".join(errors) or None)


@dataclass(frozen=True)
class TimingConfig:
    check_interval_in_seconds: int
    check_timeout_in_seconds: int
    notification_interval_in_seconds: int

    def __is_check_interval_in_seconds_valid(self) -> bool:
        return isinstance(self.check_interval_in_seconds, int) and not isinstance(self.check_interval_in_seconds, bool) and self.check_interval_in_seconds > 0

    def __is_check_timeout_in_seconds_valid(self) -> bool:
        return isinstance(self.check_timeout_in_seconds, int) and not isinstance(self.check_timeout_in_seconds, bool) and self.check_timeout_in_seconds > 0

    def __is_notification_interval_in_seconds_valid(self) -> bool:
        return isinstance(self.notification_interval_in_seconds, int) and not isinstance(self.notification_interval_in_seconds, bool) and self.notification_interval_in_seconds > 0

    def validate(self) -> DtoValidation:
        errors = []
        if not self.__is_check_interval_in_seconds_valid():
            errors.append(f"invalid timing.check_interval_in_seconds: {self.check_interval_in_seconds!r}")
        if not self.__is_check_timeout_in_seconds_valid():
            errors.append(f"invalid timing.check_timeout_in_seconds: {self.check_timeout_in_seconds!r}")
        if not self.__is_notification_interval_in_seconds_valid():
            errors.append(f"invalid timing.notification_interval_in_seconds: {self.notification_interval_in_seconds!r}")
        return (not errors, "; ".join(errors) or None)


@dataclass(frozen=True)
class PathsConfig:
    servers_config_file: str
    user_info_file: str
    logs_folder: str

    def __is_servers_config_file_valid(self) -> bool:
        return isinstance(self.servers_config_file, str) and len(self.servers_config_file.strip()) > 0

    def __is_user_info_file_valid(self) -> bool:
        return isinstance(self.user_info_file, str) and len(self.user_info_file.strip()) > 0

    def __is_logs_folder_valid(self) -> bool:
        return isinstance(self.logs_folder, str) and len(self.logs_folder.strip()) > 0

    def validate(self) -> DtoValidation:
        errors = []
        if not self.__is_servers_config_file_valid():
            errors.append(f"invalid paths.servers_config_file: {self.servers_config_file!r}")
        if not self.__is_user_info_file_valid():
            errors.append(f"invalid paths.user_info_file: {self.user_info_file!r}")
        if not self.__is_logs_folder_valid():
            errors.append(f"invalid paths.logs_folder: {self.logs_folder!r}")
        return (not errors, "; ".join(errors) or None)


@dataclass(frozen=True)
class MonitorConfig:
    smtp: SmtpConfig
    timing: TimingConfig
    paths: PathsConfig

    def validate(self) -> DtoValidation:
        errors = []
        for _, error in (
            self.smtp.validate(),
            self.timing.validate(),
            self.paths.validate(),
        ):
            if error:
                errors.append(error)
        return (not errors, "; ".join(errors) or None)
