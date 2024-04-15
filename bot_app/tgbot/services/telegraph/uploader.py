import abc
import secrets
from io import BytesIO
from typing import Optional

import aiohttp
from aiogram import Bot
from aiogram.types import PhotoSize
from pydantic import Field, BaseModel, validator

BASE_TELEGRAPH_API_LINK = "https://telegra.ph/{endpoint}"


class UploadedFile(BaseModel):
    link: str = Field(..., alias="src")

    @validator("link")
    def link_validator(cls, value: str):
        return BASE_TELEGRAPH_API_LINK.format(endpoint=value)


class FileUploader(abc.ABC):

    async def upload_photo(self, bot: Bot, photo: PhotoSize) -> UploadedFile:
        raise NotImplementedError

    async def close(self) -> None:
        raise NotImplementedError


class TelegraphService(FileUploader):
    def __init__(self) -> None:
        self._session: Optional[aiohttp.ClientSession] = None

    async def upload_photo(self, bot: Bot, photo: PhotoSize) -> UploadedFile:
        form = aiohttp.FormData(quote_fields=False)

        downloaded_photo = await bot.download(photo, destination=BytesIO())
        form.add_field(secrets.token_urlsafe(8), downloaded_photo)

        session = await self.get_session()
        response = await session.post(
            BASE_TELEGRAPH_API_LINK.format(endpoint="upload"), data=form
        )
        if not response.ok:
            raise Exception(
                "Something went wrong, response from telegraph is not successful. "
                f"Response: {response}"
            )
        json_response = await response.json()
        if isinstance(json_response, dict) and json_response.get("error"):
            raise Exception(
                "Something went wrong, response from telegraph is not successful. "
                f"Response: {json_response}"
            )
        return [UploadedFile.parse_obj(obj) for obj in json_response][0]

    async def get_session(self) -> aiohttp.ClientSession:
        if self._session is None:
            new_session = aiohttp.ClientSession()
            self._session = new_session
        return self._session

    async def close(self) -> None:
        if self._session is None:
            return None
        await self._session.close()
