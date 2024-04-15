import logging
from dataclasses import dataclass
from typing import Optional

from environs import Env
from sqlalchemy import URL


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str
    port: int = 5432

    def construct_sqlalchemy_url(self, driver="asyncpg", host=None, port=None) -> URL:
        if not host:
            host = self.host
        if not port:
            port = self.port
        uri = URL.create(
            drivername=f"postgresql+{driver}",
            username=self.user,
            password=self.password,
            host=host,
            port=port,
            database=self.database,
        )
        return uri.render_as_string(hide_password=False)


@dataclass
class RedisConfig:
    redis_pass: Optional[str]
    redis_port: Optional[int]
    redis_host: Optional[str]

    def dsn(self) -> str:
        if self.redis_pass:
            return f"redis://:{self.redis_pass}@{self.redis_host}:{self.redis_port}/0"
        else:
            return f"redis://{self.redis_host}:{self.redis_port}/0"


@dataclass
class UserConfig:
    phone_number: str
    api_id: int
    api_hash: str
    password: Optional[str] = None


@dataclass
class Config:
    db: DbConfig
    user: UserConfig
    redis: RedisConfig | None = None
    DEBUG: bool = False


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        db=DbConfig(
            host=env.str("DB_HOST"),
            user=env.str("POSTGRES_USER"),
            password=env.str("POSTGRES_PASSWORD"),
            database=env.str("POSTGRES_DB"),
        ),
        redis=RedisConfig(
            redis_pass=env.str("REDIS_PASSWORD"),
            redis_port=env.int("REDIS_PORT"),
            redis_host=env.str("REDIS_HOST"),
        ),
        user=UserConfig(
            phone_number=env.str("PHONE_NUMBER"),
            api_id=env.int("API_ID"),
            api_hash=env.str("API_HASH"),
        ),
    )
