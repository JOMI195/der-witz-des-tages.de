from rest_framework import viewsets, status
from config.throttles import BurstRateThrottle, SustainedRateThrottle
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from workflows.tasks import (
    joke_of_the_day_email_only_workflow_specific,
    joke_of_the_day_full_workflow,
    joke_of_the_day_full_workflow_specific,
)


class WorkflowsViewSet(viewsets.ModelViewSet):
    http_method_names = ["post", "head", "options"]
    throttle_classes = [BurstRateThrottle, SustainedRateThrottle]

    @extend_schema(
        methods=["POST"],
        parameters=[
            OpenApiParameter(
                name="workflow_type",
                description="Type of workflow to trigger",
                type=str,
                enum=["full", "email_only_specific", "full_specific"],
            ),
            OpenApiParameter(
                name="recipient_emails",
                description="List of recipient email addresses (for specific workflows)",
                type=str,
            ),
        ],
        responses={
            200: OpenApiParameter(
                name="message",
                description="Joke of the day workflow triggered successfully",
                type=str,
            ),
            500: OpenApiParameter(
                name="error",
                description="Trigger of Joke of the day workflow failed",
                type=str,
            ),
        },
    )
    @action(
        detail=False,
        methods=["post"],
        url_path="trigger-workflows",
        permission_classes=[IsAdminUser],
    )
    def trigger_joke_of_the_day_workflow(self, request):
        workflow_type = request.data.get("workflow_type", "").lower()
        recipient_emails = request.data.get("recipient_emails", [])

        try:
            if workflow_type == "full":
                joke_of_the_day_full_workflow.delay()
            elif workflow_type == "email_only_specific":
                joke_of_the_day_email_only_workflow_specific.delay(recipient_emails)
            elif workflow_type == "full_specific":
                joke_of_the_day_full_workflow_specific.delay(recipient_emails)
            else:
                return Response(
                    {
                        "error": "Invalid workflow type. Choose 'full', 'email_only_specific', or 'full_specific'."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            return Response(
                {"message": "Joke of the day workflow triggered successfully"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": "Trigger of Joke of the day workflow failed"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
