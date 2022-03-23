from rest_framework import mixins, viewsets
from users.permissions import AdminPermission

from .permissions import ReadOnly


class CreateListDestroyModelViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = (AdminPermission | ReadOnly,)
