from django.core.mail import send_mail
from django.conf import settings


def send_email(subject, message, recipient_list):
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            fail_silently=False,
        )
        return True, "Email sent"
    except Exception as e:
        return False, str(e)


def send_otp_email(email, otp):
    subject = "OTP Verification"
    message = f"Your OTP is {otp}"

    return send_email(subject, message, [email])