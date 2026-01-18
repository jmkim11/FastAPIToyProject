from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship, func, Column, AutoString
from pydantic import EmailStr, AwareDatetime
from sqlalchemy import UniqueConstraint
from sqlalchemy_utc import UtcDateTime
from typing import TYPE_CHECKING
import random
import string
from pydantic import model_validator

if TYPE_CHECKING:
    from appserver.apps.calendar.models import Calendar

class User(SQLModel, table=True):
    __tablename__ = "users"
    __table_args = {
        UniqueConstraint("email", name = "uq_email"),
    }

    # 파이썬은 자료형 각주에서 자료형을 문자열로 표기하면 해당 자료형을 지연 평가하는데, 이를 파이썬에서는 문자열 각주 또는 전방 참조라고 한다.
    # 순환 참조를 해결하거나 아직 정의되지 않은 자료형을 참조할 때 사용하는 방식이다.
    oauth_accounts: list["OAuthAccount"] = Relationship(back_populates="user")
    calendar: "Calendar" = Relationship(
        back_populates="host",
        sa_relationship_kwargs={ "uselist": False, "single_parent": True, "lazy":"joined" },
    )

    bookings: list["Booking"] = Relationship(back_populates="guest")
    
    id: int = Field(default=None, primary_key=True)
    username: str = Field(min_length = 4, max_length=40, description="사용자 계정 ID")
    email: EmailStr = Field(unique=True, min_length = 4, max_length=128, description="사용자 이메일")
    display_name: str = Field(min_length=4, max_length=40, description="사용자 표시 이름")
    hashed_password: str = Field(min_length=8, max_length=128, description="사용자 비밀번호")
    is_host: bool = Field(default=False, description="사용자가 호스트인지 여부")
    created_at: AwareDatetime = Field(
        default=None,
        nullable=False,
        sa_type=UtcDateTime,
        sa_column_kwargs={
            "server_default": func.now(),
        },
    )

    updated_at: AwareDatetime = Field(
        default=None,
        nullable=False,
        sa_type=UtcDateTime,
        sa_column_kwargs={
            "server_default": func.now(),
            "onupdate": lambda: datetime.now(timezone.utc),
        },
    )

#    @model_validator(mode="before")
#    @classmethod
#    def generate_display_name(cls, data: dict):
#        if not data.get("display_name"):
#            data["display_name"] = "".join(random.choices(string.ascii_letters +
#                                            string.digits, k=8))
#                                                                                                                                                        return data


class OAuthAccount(SQLModel, table=True):
    __tablename__ = "oauth_accounts"
    __table_args__= (
        UniqueConstraint(
            "provider",
            "provider_account_id",
            name="uq_provider_provider_account_id",
        ),
    )

    id: int = Field(default = None, primary_key=True)

    provider: str = Field(max_length=10, description="OAuth 제공자")
    provider_account_id: str = Field(max_length=128, description="OAuth 제공자 계정 ID")

    user_id: int = Field(foreign_key="users.id")
    user: User = Relationship(back_populates="oauth_accounts")

    created_at: AwareDatetime = Field(
        default=None,
        nullable=False,
        sa_type=UtcDateTime,
        sa_column_kwargs={
        "server_default": func.now(),
        },
    )

    updated_at: AwareDatetime = Field(
        default=None,
        nullable=False,
        sa_type=UtcDateTime,
        sa_column_kwargs={
            "server_default": func.now(),
            "onupdate": lambda: datetime.now(timezone.utc),
        },
    )
