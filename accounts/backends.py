from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomerEmailOrPhoneBackend(BaseBackend):
    """
    Authenticate a customer using email or phone number + password
    """

    def authenticate(self, request, email=None, phone=None, password=None, **kwargs):
        user = None
        # Try to find user by email
        if email:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None

        # If not found by email, try phone number
        if not user and phone:
            try:
                user = User.objects.get(customer_profile__contact_no=phone)
            except User.DoesNotExist:
                return None

        # Check password and ensure it's a customer
        if user and user.check_password(password) and user.is_customer:
            return user

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
