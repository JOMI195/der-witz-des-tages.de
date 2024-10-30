from django.conf import settings
from .tasks import send_django_mail_with_logo
from djoser.email import (
    ActivationEmail,
    ConfirmationEmail,
    PasswordResetEmail,
    PasswordChangedConfirmationEmail,
    BaseDjoserEmail,
)

# def sendDjoserMail(
#     template_name,
#     context,
# ):
#     context["contact_link"] = (
#         os.environ.get("FRONTEND_BASE_URL") + settings.FRONTEND_CONTACT_URL
#     )

#     message = render_to_string(template_name, context)

#     send_mail(
#         subject=context["subject"],
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         message="",
#         recipient_list=[context["user"].email],
#         html_message=message,
#         fail_silently=False,
#     )


# def sendDjoserMail(template_name, context):

#     context["contact_link"] = (
#         os.environ.get("FRONTEND_BASE_URL") + settings.FRONTEND_CONTACT_URL
#     )
#     context["logo_image_cid"] = "logo_image"

#     html_message = render_to_string(template_name, context)

#     email = EmailMessage(
#         subject=context["subject"],
#         body=html_message,
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         to=[context["user"].email],
#     )
#     email.content_subtype = "html"

#     logo_path = os.path.join(
#         settings.BASE_DIR,
#         "mediafiles",
#         "brand",
#         "witz-des-tages-logo-light-full.png",
#     )
#     with open(logo_path, "rb") as f:
#         logo_image = MIMEImage(f.read())
#         logo_image.add_header("Content-ID", "<logo_image>")
#         email.attach(logo_image)

#     email.send(fail_silently=False)


class DjoserActivationEmail(ActivationEmail):
    template_name = "djoser/activation.html"

    def get_context_data(self):
        context = super().get_context_data()
        context["subject"] = (
            "Willkommen bei Der-Witz-Des-Tages.de! Wir freuen uns, dich an Bord zu haben."
        )
        return context

    def send(self, *args, **kwargs):
        context = self.get_context_data()
        send_django_mail_with_logo(
            template_name=self.template_name,
            context=context,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to_emails=[context["user"].email],
        )


class DjoserConfirmationEmail(ConfirmationEmail):
    template_name = "djoser/confirmation.html"

    def get_context_data(self):
        context = super().get_context_data()
        context["subject"] = (
            "Dein Konto ist jetzt aktiv. Wir freuen uns auf deine Witze!"
        )
        return context

    def send(self, *args, **kwargs):
        context = self.get_context_data()
        send_django_mail_with_logo(
            template_name=self.template_name,
            context=context,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to_emails=[context["user"].email],
        )


class DjoserPasswordResetEmail(PasswordResetEmail):
    template_name = "djoser/password_reset.html"

    def get_context_data(self):
        context = super().get_context_data()
        context["subject"] = (
            "Keine Sorge, wir sind für dich da. Setze dein Passwort zurück, um wieder Zugriff zu erhalten."
        )
        return context

    def send(self, *args, **kwargs):
        context = self.get_context_data()
        send_django_mail_with_logo(
            template_name=self.template_name,
            context=context,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to_emails=[context["user"].email],
        )


class DjoserPasswordChangedConfirmationEmail(PasswordChangedConfirmationEmail):
    template_name = "djoser/password_changed_confirmation.html"

    def get_context_data(self):
        context = super().get_context_data()
        context["subject"] = (
            "Dein Passwort wurde erfolgreich aktualisiert. Dein Konto ist jetzt sicherer!"
        )
        return context

    def send(self, *args, **kwargs):
        context = self.get_context_data()
        send_django_mail_with_logo(
            template_name=self.template_name,
            context=context,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to_emails=[context["user"].email],
        )


class DjoserUserDeletedEmail(BaseDjoserEmail):
    template_name = "djoser/user_deleted.html"

    def get_context_data(self):
        context = super().get_context_data()
        context["subject"] = "Dein Konto wurde gelöscht – Alles Gute und bis bald! 👋"
        return context

    def send(self, *args, **kwargs):
        context = self.get_context_data()
        send_django_mail_with_logo(
            template_name=self.template_name,
            context=context,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to_emails=[context["user"].email],
        )
