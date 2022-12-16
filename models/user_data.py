from __future__ import annotations
import typing

from aredis_om import JsonModel, Field, NotFoundError

from models.task import Task


class UserData(JsonModel):
    user_id: int = Field(index=True)
    tasks: typing.List[Task] = []

    @classmethod
    async def get_by_user_id(cls, user_id: int) -> typing.Optional[UserData]:
        try:
            return await UserData.find(UserData.user_id == user_id).first()
        except NotFoundError:
            return None

    @classmethod
    async def get_or_make_new(cls, user_id: int) -> UserData:
        user_data = await UserData.get_by_user_id(user_id)
        if user_data is not None:
            return user_data

        user_data = UserData(user_id=user_id)
        await user_data.save()
        return user_data
