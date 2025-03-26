from dataclasses import dataclass
from typing import TYPE_CHECKING, Generic, Optional, Type, TypeVar, cast

from LOGS.Auxiliary import Tools
from LOGS.Entity.SerializeableContent import SerializeableClass
from LOGS.Interfaces.IEntityInterface import IEntityInterface

if TYPE_CHECKING:
    pass


@dataclass
class IPermissionedEntityRequest:
    includePermissions: Optional[bool] = None


class IPermissionModel:
    edit: Optional[bool] = None


class GenericPermission(IPermissionModel, SerializeableClass):
    edit: Optional[bool] = False


_PERMISSION = TypeVar("_PERMISSION", bound=IPermissionModel)


class IPermissionedEntity(Generic[_PERMISSION], IEntityInterface):
    _permissionType: Optional[Type[_PERMISSION]] = None

    _permissions: Optional[_PERMISSION] = None

    @property
    def permissions(self) -> Optional[_PERMISSION]:
        return self._permissions

    @permissions.setter
    def permissions(self, value):
        if not self._permissionType:
            raise NotImplementedError("Permission type must be set")

        self._permissions = Tools.checkAndConvert(
            value,
            cast(Type[_PERMISSION], self._permissionType),
            "permissions",
            allowNone=True,
        )


class GenericPermissionEntity(IPermissionedEntity[GenericPermission]):
    _permissionType: Type[GenericPermission] = GenericPermission
