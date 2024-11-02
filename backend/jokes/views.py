from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from django.core.files.storage import default_storage
from jokes.joke_of_the_day.joke_of_the_day import get_latest_joke_of_the_day
from jokes.tasks import create_shareable_image
from config.throttles import BurstRateThrottle, SustainedRateThrottle

from .models import Joke, JokeOfTheDay
from .serializers import (
    JokeRetrieveSerializer,
    JokeCreateSerializer,
    SubmittedJokeCreateSerializer,
    SubmittedJokeRetrieveSerializer,
)
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated


class JokePagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = "page_size"
    max_page_size = 100


class JokeViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "head", "options"]
    queryset = Joke.objects.all().order_by("-created_at")
    pagination_class = JokePagination
    throttle_classes = [BurstRateThrottle, SustainedRateThrottle]

    def get_serializer_class(self):
        if self.action == "list":
            return JokeRetrieveSerializer
        if self.action == "retrieve":
            return JokeRetrieveSerializer
        elif self.action == "create":
            return JokeCreateSerializer
        return self.serializer_class

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsAdminUser]
        # elif self.action == "list":
        #     self.permission_classes = [AllowAny]
        # elif self.action == "retrieve":
        #     self.permission_classes = [AllowAny]
        return super().get_permissions()

    @extend_schema(
        methods=["POST"],
        request=JokeCreateSerializer,
        responses={201: JokeRetrieveSerializer},
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        element = serializer.create(serializer.validated_data)
        serializer = JokeRetrieveSerializer(element)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # @extend_schema(
    #     methods=["GET"],
    #     responses={200: JokeRetrieveSerializer(many=True)},
    # )
    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     paginator = self.pagination_class()
    #     page = paginator.paginate_queryset(queryset, request)
    #     serializer = self.get_serializer(page, many=True)
    #     return paginator.get_paginated_response(serializer.data)

    # @extend_schema(
    #     methods=["GET"],
    #     responses={200: JokeRetrieveSerializer},
    # )
    # def retrieve(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     element = get_object_or_404(queryset, pk=self.kwargs["pk"])
    #     serializer = JokeRetrieveSerializer(element)
    #     return Response(serializer.data)

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

    # @extend_schema(
    #     methods=["GET"],
    #     responses={200: JokeRetrieveSerializer(many=True)},
    # )
    # @action(
    #     detail=False,
    #     methods=["get"],
    #     url_path="jokes-with-pictures",
    #     permission_classes=[AllowAny],
    # )
    # def jokes_with_pictures(self, request, *args, **kwargs):
    #     jokes_with_pics = Joke.objects.filter(joke_picture__isnull=False).order_by(
    #         "-created_at"
    #     )
    #     paginator = self.pagination_class()
    #     page = paginator.paginate_queryset(jokes_with_pics, request)
    #     serializer = JokeRetrieveSerializer(page, many=True)
    #     return paginator.get_paginated_response(serializer.data)

    @extend_schema(
        methods=["GET"],
        responses={200: JokeRetrieveSerializer()},
    )
    @action(
        detail=False,
        methods=["get"],
        url_path="latest-joke-of-the-day",
        permission_classes=[AllowAny],
    )
    def latest_joke_of_the_day(self, request, *args, **kwargs):
        latest_newsletter = get_latest_joke_of_the_day()

        if latest_newsletter is None:
            return Response(
                {"detail": "No joke of the day found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = JokeRetrieveSerializer(latest_newsletter.joke)
        return Response(serializer.data)

    @extend_schema(
        methods=["POST"],
        request=SubmittedJokeCreateSerializer,
        responses={201: SubmittedJokeRetrieveSerializer},
    )
    @action(
        detail=False,
        methods=["post"],
        url_path="submit-joke",
        permission_classes=[IsAuthenticated],
    )
    def submit_joke(self, request, *args, **kwargs):
        serializer = SubmittedJokeCreateSerializer(
            data=request.data,
            context={
                "created_by": request.user,
            },
        )
        serializer.is_valid(raise_exception=True)
        element = serializer.save(created_by=request.user)
        serializer = SubmittedJokeRetrieveSerializer(element)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        methods=["POST"],
        responses={202: {"description": "Screenshot task initiated"}},
    )
    @action(
        detail=False,
        methods=["post"],
        url_path="create_shareable_image",
        permission_classes=[IsAdminUser],
    )
    def take_screenshot(self, request, *args, **kwargs):
        create_shareable_image.delay()

        return Response(
            {"detail": "Screenshot task initiated."}, status=status.HTTP_202_ACCEPTED
        )
