from rest_framework import viewsets, status
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from socials_sharing.tasks import share_on_socials_instagram


class SocialsSharingViewSet(viewsets.ModelViewSet):
    @extend_schema(
        methods=["POST"],
        parameters=[
            {
                "name": "platforms",
                "required": False,
                "type": str,
                "description": "Platform to share on ('instagram')",
            }
        ],
        responses={202: {"description": "Sharing on socials initiated"}},
    )
    @action(
        detail=False,
        methods=["post"],
        url_path="share_on_socials",
        permission_classes=[IsAdminUser],
    )
    def share_on_socials_endpoint_function(self, request, *args, **kwargs):
        platform = request.data.get("platforms", None)

        if platform == "instagram":
            share_on_socials_instagram.delay()
        else:
            return Response(
                {"detail": "Invalid platform specified. Please use 'instagram'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"detail": "Sharing on socials initiated"}, status=status.HTTP_202_ACCEPTED
        )
