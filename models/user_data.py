import typing

from aredis_om import JsonModel, Field

from models.task import Task


class UserData(JsonModel):
    user_id: int = Field(index=True)
    tasks: typing.List[Task] = []
