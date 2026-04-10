from django.core.mail import send_mail


def send_otp_email(email, otp):
    send_mail(
        "OTP Verification",
        f"Your OTP is {otp}",
        "noreply@system.com",
        [email],
    )