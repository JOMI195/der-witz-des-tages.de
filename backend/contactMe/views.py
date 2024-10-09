from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from config.throttles import SustainedRateThrottle
from config.throttles import BurstRateThrottle
from .serializers import ContactMeSerializer
from django.core.mail import send_mail
from drf_spectacular.utils import extend_schema


class ContactMeView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [BurstRateThrottle, SustainedRateThrottle]

    @extend_schema(
        methods=["POST"],
        request=ContactMeSerializer,
        responses={200: "Email sent successfully.", 400: "Validation error"},
    )
    def post(self, request, *args, **kwargs):
        serializer = ContactMeSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data["name"]
            subject = serializer.validated_data["subject"]
            email = serializer.validated_data["email"]
            message = serializer.validated_data["message"]

            send_mail(
                subject=f"New Contact from {email}",
                message=f"From: {name} <{email}>\n\nSubject: {subject}\n\nMessage: {message}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[
                    settings.DEFAULT_FROM_EMAIL,
                ],
            )

            return Response(
                {"message": "Email sent successfully."}, status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(exclude=True)
    def get(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @extend_schema(exclude=True)
    def put(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @extend_schema(exclude=True)
    def delete(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
