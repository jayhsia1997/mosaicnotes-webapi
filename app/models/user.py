"""
Model of the user table
"""
from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.libs.consts.enums import Gender
from app.libs.database.orm import ModelBase
from .mixins import AuditMixin, DeletedMixin, RemarkMixin, DescriptionMixin, AuditCreatedAtMixin, AuditUpdatedAtMixin


class User(ModelBase, RemarkMixin, DeletedMixin, AuditMixin):
    """User Model"""
    __tablename__ = "user"
    __table_args__ = {"schema": "public"}
    email = Column(String(64), nullable=False, unique=True, comment="Email, unique identifier")
    password_hash = Column(String(256), comment="Password hash")
    salt = Column(String(64), comment="Salt for password hash")


class UserProfile(ModelBase, DeletedMixin, AuditMixin, DescriptionMixin):
    """User Profile Model"""
    __tablename__ = "user_profile"
    __table_args__ = {"schema": "public"}
    user_id = Column(String(64), nullable=False, unique=True, comment="User ID")
    display_name = Column(String(64), comment="Display name")
    gender = Column(Integer, default=Gender.UNKNOWN.value, comment="Refer to Gender enum")


class UserSession(ModelBase, AuditCreatedAtMixin, AuditUpdatedAtMixin):
    """User Session Model"""
    __tablename__ = "user_session"
    __table_args__ = {"schema": "public"}
    user_id = Column(UUID, ForeignKey(User.id, ondelete="CASCADE"), nullable=False, comment="User ID", index=True)
    data = Column(JSONB, comment="Session data")
    expired_at = Column(TIMESTAMP, comment="Session expiration time")
    ip_address = Column(String(64), comment="User IP address")
    user_agent = Column(String(256), comment="User agent")
