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
    check_interval_in_seconds: int
    check_timeout_in_seconds: int
    notification_interval_in_seconds: int

    def validate(self) -> Base.DTOValidation:
        return self._aggregate([
            (
                self._is_positive_int(self.check_interval_in_seconds),
                f"invalid timing.check_interval_in_seconds: {self.check_interval_in_seconds!r}",
            ),
            (
                self._is_positive_int(self.check_timeout_in_seconds),
                f"invalid timing.check_timeout_in_seconds: {self.check_timeout_in_seconds!r}",
            ),
            (
                self._is_positive_int(self.notification_interval_in_seconds),
                f"invalid timing.notification_interval_in_seconds: {self.notification_interval_in_seconds!r}",
            ),
        ])


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
    paths: PathsConfig

    def validate(self) -> Base.DTOValidation:
        return self._aggregate([
            self.smtp.validate(),
            self.timing.validate(),
            self.paths.validate(),
        ])
