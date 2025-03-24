from django.views import View
from rest_framework.request import Request

from .is_authenticated import IsAuthenticated


class IsCreator(IsAuthenticated):
    def has_object_permission(
        self,
        request: Request,
        view: View,  # noqa: ARG002
        obj,  # noqa: ANN001
    ) -> bool:
        return obj.creator_id == request.user.id
