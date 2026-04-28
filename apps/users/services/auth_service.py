from django.contrib.auth import get_user_model

User = get_user_model()


class AuthService:

    @staticmethod
    def create_user(serializer):
        return serializer.save()

    @staticmethod
    def activate_user(user):
        user.account_status = User.Status.ACTIVE   
        user.email_verified = True
        user.save(update_fields=["account_status", "email_verified"])