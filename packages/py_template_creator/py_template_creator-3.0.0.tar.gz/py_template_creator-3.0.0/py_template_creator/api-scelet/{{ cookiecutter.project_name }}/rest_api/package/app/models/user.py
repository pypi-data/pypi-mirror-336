from typing import Optional
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils.types.password import PasswordType
from sqlalchemy_utils import EmailType
from .base import Base, IdMixin, CreatedMixin
from sqlalchemy_utils import force_auto_coercion

import logging

force_auto_coercion()
logger = logging.getLogger(__name__)


class UsersModel(IdMixin, CreatedMixin, Base):
    __tablename__ = "table_users"

    display_name: Mapped[str]
    email: Mapped[str] = mapped_column(EmailType, unique=True)
    phone: Mapped[str] = mapped_column(unique=True)
    password: Mapped[Optional[str]] = mapped_column(
        PasswordType(schemes=["bcrypt"]), unique=False, default=None
    )
    is_email_verified: Mapped[bool] = mapped_column(default=False)
    is_phone_verified: Mapped[bool] = mapped_column(default=False)
    image: Mapped[str] = mapped_column(String(200), default="")
    is_superuser: Mapped[bool] = mapped_column(default=False)
