from typing import Optional

from pydantic import BaseSettings


class Config(BaseSettings):
    api_id: int
    api_hash: str
    phone_number: str
    github_url: str = "https://github.com/WhiteMemory99/telecharm-userbot"

    class Config:
        allow_mutation = False
        env_file = ".env"


conf = Config()
