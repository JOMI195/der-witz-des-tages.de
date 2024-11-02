from rest_framework import viewsets, status
from config.throttles import BurstRateThrottle, SustainedRateThrottle
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser

from .models import NewsletterReciever
from .serializers import NewsletterRecieverSerializer
from .email import (
    send_newsletter_reciever_activation_email,
    send_newsletter_reciever_confirmation_email,
)


class NewsletterRecieverViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "head", "options"]
    queryset = NewsletterReciever.objects.all()
    serializer_class = NewsletterRecieverSerializer
    throttle_classes = [BurstRateThrottle, SustainedRateThrottle]

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    @extend_schema(
        methods=["POST"],
        request=NewsletterRecieverSerializer,
        responses={201: None},
    )
    def create(self, request, *args, **kwargs):
        email = request.data.get("email")
        if NewsletterReciever.objects.filter(email=email).exists():
            reciever = NewsletterReciever.objects.get(email=email)

            try:
                send_newsletter_reciever_activation_email(reciever)
            except:
                return Response(
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    data={"error": "Failed to send activation email"},
                )

            return Response(
                status=status.HTTP_201_CREATED, data={"reciever": "success"}
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reciever = serializer.save(is_active=False)

        try:
            send_newsletter_reciever_activation_email(reciever)
        except:
            reciever.delete()
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data={"error": "Failed to send activation email"},
            )

        return Response(status=status.HTTP_201_CREATED, data={"reciever": "success"})

    @extend_schema(exclude=True)
    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @extend_schema(exclude=True)
    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @extend_schema(exclude=True)
    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @extend_schema(exclude=True)
    def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @extend_schema(exclude=True)
    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @extend_schema(
        methods=["POST"],
        request=OpenApiParameter(
            name="activation_token",
            description="Token used for activation",
            type=str,
            required=True,
        ),
        responses={
            200: OpenApiParameter(
                name="message",
                description="Successful activation message",
                type=str,
            ),
            400: OpenApiParameter(
                name="error",
                description="Error message for invalid token or allready activated",
                type=str,
            ),
        },
    )
    @action(
        detail=False,
        methods=["post"],
        url_path="activate",
        permission_classes=[AllowAny],
    )
    def activate(self, request):
        activation_token = request.data.get("activation_token")

        if not activation_token:
            return Response(
                {"error": "Activation token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            reciever = NewsletterReciever.objects.get(
                activation_token=activation_token, is_active=False
            )
            reciever.is_active = True
            reciever.save()

            send_newsletter_reciever_confirmation_email(reciever)
            return Response(
                {"message": "Your subscription has been activated successfully."},
                status=status.HTTP_200_OK,
            )
        except NewsletterReciever.DoesNotExist:
            return Response(
                {"error": "Invalid activation token or allready activated."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @extend_schema(
        methods=["POST"],
        request=OpenApiParameter(
            name="unsubscribe_token",
            description="Token used for unsubscription",
            type=str,
            required=True,
        ),
        responses={
            200: OpenApiParameter(
                name="message",
                description="Successful unsubscription message",
                type=str,
            ),
            400: OpenApiParameter(
                name="error", description="Error message for invalid token", type=str
            ),
        },
    )
    @action(
        detail=False,
        methods=["post"],
        url_path="unsubscribe",
        permission_classes=[AllowAny],
    )
    def unsubscribe(self, request):
        unsubscribe_token = request.data.get("unsubscribe_token")

        if not unsubscribe_token:
            return Response(
                {"error": "Unsubscribe token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            reciever = NewsletterReciever.objects.get(
                unsubscribe_token=unsubscribe_token
            )
            reciever.delete()
            return Response(
                {"message": "You have been unsubscribed successfully."},
                status=status.HTTP_200_OK,
            )
        except NewsletterReciever.DoesNotExist:
            return Response(
                {"error": "Invalid unsubscribe token."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class JokeNewsletterViewSet(viewsets.ModelViewSet):
    def get_permissions(self):
        self.permission_classes = [IsAdminUser]
        return super().get_permissions()
