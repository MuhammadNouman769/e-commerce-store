from django.contrib.auth import get_user_model

User = get_user_model()


class UserService:

    @staticmethod
    def get_user_by_email(email):
        return User.objects.filter(email=email).first()