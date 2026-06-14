from dataclasses import dataclass
from ._base import Base


@dataclass(frozen=True)
class SmtpConfig(Base):
    host: str
    port: int
    username: str
    password: str
    use_tls: bool
    from_address: str

    def validate(self) -> Base.DTOValidation:
        return self._aggregate([
            (self._is_not_blank(self.host), f"invalid smtp.host: {self.host!r}"),
            (self._is_port(self.port), f"invalid smtp.port: {self.port!r}"),
            (self._is_not_blank(self.username), f"invalid smtp.username: {self.username!r}"),
            (self._is_non_empty(self.password), "invalid smtp.password"),
            (self._is_bool(self.use_tls), f"invalid smtp.use_tls: {self.use_tls!r}"),
            (self._is_email(self.from_address), f"invalid smtp.from_address: {self.from_address!r}"),
        ])


@dataclass(frozen=True)
class TimingConfig(Base):
    __CHECK_INTERVAL_RANGE = 1, (24 * 60 * 60)
    __CHECK_TIMEOUT_RANGE = 1, 60
    __NOTIFICATION_INTERVAL_RANGE = 1, (24 * 60 * 60)

    check_interval_in_seconds: int
    check_timeout_in_seconds: int
    notification_interval_in_seconds: int

    def validate(self) -> Base.DTOValidation:
        return self._aggregate([
            self.__validate_one(
                "check_interval_in_seconds",
                self.check_interval_in_seconds,
                self.__CHECK_INTERVAL_RANGE
            ),
            self.__validate_one(
                "check_timeout_in_seconds",
                self.check_timeout_in_seconds,
                self.__CHECK_TIMEOUT_RANGE
            ),
            self.__validate_one(
                "notification_interval_in_seconds",
                self.notification_interval_in_seconds,
                self.__NOTIFICATION_INTERVAL_RANGE
            ),
        ])

    def __validate_one(self, name: str, value: int, value_range: tuple) -> Base.DTOValidation:
        minimum, maximum = value_range
        return (
            self._is_int_in_range(value, minimum, maximum),
            f"invalid timing.{name} (expected {minimum}..{maximum}): {value!r}",
        )


@dataclass(frozen=True)
class ConcurrencyConfig(Base):
    __CHECK_WORKERS_RANGE = (1, 64)

    check_workers: int

    def validate(self) -> Base.DTOValidation:
        return self._aggregate([
            self.__validate_one(
                "check_workers",
                self.check_workers,
                self.__CHECK_WORKERS_RANGE
            ),
        ])

    def __validate_one(self, name: str, value: int, value_range: tuple) -> Base.DTOValidation:
        minimum, maximum = value_range
        return (
            self._is_int_in_range(value, minimum, maximum),
            f"invalid concurrency.{name} (expected {minimum}..{maximum}): {value!r}",
        )


@dataclass(frozen=True)
class PathsConfig(Base):
    servers_config_file: str
    user_info_file: str
    logs_folder: str

    def validate(self) -> Base.DTOValidation:
        return self._aggregate([
            (
                self._is_not_blank(self.servers_config_file),
                f"invalid paths.servers_config_file: {self.servers_config_file!r}",
            ),
            (
                self._is_not_blank(self.user_info_file),
                f"invalid paths.user_info_file: {self.user_info_file!r}",
            ),
            (
                self._is_not_blank(self.logs_folder),
                f"invalid paths.logs_folder: {self.logs_folder!r}",
            ),
        ])


@dataclass(frozen=True)
class MonitorConfig(Base):
    smtp: SmtpConfig
    timing: TimingConfig
    concurrency: ConcurrencyConfig
    paths: PathsConfig

    def validate(self) -> Base.DTOValidation:
        return self._aggregate([
            self.smtp.validate(),
            self.timing.validate(),
            self.concurrency.validate(),
            self.paths.validate(),
        ])
