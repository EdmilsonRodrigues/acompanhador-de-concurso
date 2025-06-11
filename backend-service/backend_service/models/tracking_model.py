from sqlmodel import Field, SQLModel


class TrackingBase(SQLModel):
    category: str = Field()
    state: str = Field()


class Tracking(TrackingBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key='user.id')


class TrackingPublic(TrackingBase):
    id: int


class TrackingCreate(TrackingBase): ...
