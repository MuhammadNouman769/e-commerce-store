# services/auth_service.py

class AuthService:

    @staticmethod
    def create_user(serializer):
        return serializer.save()

    @staticmethod
    def activate_user(user):
        user.account_status = "active"
        user.email_verified = True
        user.save()