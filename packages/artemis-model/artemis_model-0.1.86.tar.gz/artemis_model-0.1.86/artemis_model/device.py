import enum
import uuid
from datetime import datetime

from sqlalchemy import JSON, UUID, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy

from artemis_model.base import CustomSyncBase, CustomBase, TimeStampMixin


class DeviceControlMode(enum.Enum):
    PLAYER = "player"
    CONTROL = "control"
    

class DeviceMixin(TimeStampMixin):
    """
    Represents a Jukebox device that can be controlled by multiple users.
    """
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    device_id: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)  # e.g., "Living Room Jukebox"
    control_mode: Mapped[DeviceControlMode] = mapped_column(Enum(DeviceControlMode), nullable=True)
    last_seen: Mapped[datetime | None] = mapped_column(nullable=True)
    version: Mapped[int] = mapped_column(default=0)
    device_specs: Mapped[JSON] = mapped_column(JSON, nullable=True) 

    @declared_attr
    def device_user_assoc(cls) -> Mapped[list["DeviceUserAssoc"]]:
        return relationship(cascade="all, delete-orphan")

    @declared_attr
    def user_ids(cls) -> Mapped[list["UserAccount"] | None]:
        return association_proxy(
            "device_user_assoc",
            "user",
            creator=lambda u: DeviceUserAssoc(user_id=u),
        )

    @declared_attr
    def users(cls) -> Mapped[list["UserAccount"]]:
        return relationship(
            secondary="device_user_assoc", 
            viewonly=True
        )


class DeviceSync(CustomSyncBase, DeviceMixin):
    pass


class Device(CustomBase, DeviceMixin):
    pass


class DeviceUserAssocMixin(TimeStampMixin):
    """
    Association table for many-to-many relationship between UserAccount and Device.
    """

    device_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("device.id"), primary_key=True, nullable=False
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user_account.id"), primary_key=True, nullable=False
    )


class DeviceUserAssocSync(CustomSyncBase, DeviceUserAssocMixin):
    pass


class DeviceUserAssoc(CustomBase, DeviceUserAssocMixin):
    pass
