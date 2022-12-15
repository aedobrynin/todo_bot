from aredis_om import EmbeddedJsonModel


class Task(EmbeddedJsonModel):
    description: str
    done: bool
